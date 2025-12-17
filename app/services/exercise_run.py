from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload, joinedload
from typing import List
from datetime import datetime

from app.db.models import ExerciseModel, ExerciseFileModel, TestCaseModel, HintModel, CourseModel, UnitModel, SubmissionHistoryModel, SubmissionMarkerModel, SubmissionResultModel, ExerciseProgressModel
from app.schemas.schemas import ExerciseFull, File, Test, Hint, StudentSubmissionPayload, TestResult
from app.core.enums import Visibility, SubmissionStatus, ProgressStatus, Language, TestStatus

from app.utils.parsing import extract_student_solutions, inject_markers_into_template, MarkerData
from app.services.compiler import compile_and_run_logics

def format_files_for_student(sql_files: List[ExerciseFileModel]) -> List[File]:
    """Transforms the files received from the DB (ExerciseFileModel) into Pydantic types (File)."""
    formatted_files = []
    
    for f in sql_files:
        # The student don't receive the main
        if f.is_main:
            continue

        formatted_files.append(
            File(
                id=f.id,
                name=f.name,
                content=f.template_without_marker, 
                extension=f.extension,
                is_main=f.is_main,
                editable=f.editable,
                position=f.position
            )
        )

    return formatted_files

def format_tests_for_student(sql_tests: List[TestCaseModel]) -> List[Test]:
    """Transforms the tests received from the DB (TestCaseModel) into Pydantic types (Test)."""
    formatted_tests = []
    for t in sql_tests:
        formatted_tests.append(
            Test(
                id=t.id,
                argv=t.argv,
                expected_output=t.expected_output,
                comment=t.comment or "",
                position=t.position
            )
        )
    return formatted_tests


def format_hints_for_student(sql_hints: List[HintModel]) -> List[Hint]:
    """Transforms the hints received from the DB (HintModel) into Pydantic types (Hint)."""
    formatted_hints = []
    for h in sql_hints:
        formatted_hints.append(
            Hint(
                id=h.id,
                body=h.body,
                unlock_after_attempts=h.unlock_after_attempts,
                position=h.position
            )
        )
    return formatted_hints

def get_exercise_for_student(unit_id: int, course_id: int, exercise_id: int, db: Session): 
    """
    Retrieves a complete exercise for a student, verifying visibility.
    """

    # .options(selectinload(...)) loads the kids of Exercise (files, hint, tests) in the same requestfor better performance
    exercise = (
        db.query(ExerciseModel)
        .join(CourseModel) # join with course_id
        .join(UnitModel)   # join with unit_id
        .filter(
            UnitModel.id == unit_id,
            CourseModel.id == course_id,
            ExerciseModel.id == exercise_id, 
        ) # Find the good exercise and check if it's public
        .options(
            #selectinload better for one to many relationship 
            selectinload(ExerciseModel.files),
            selectinload(ExerciseModel.tests),
            selectinload(ExerciseModel.hints),

            #joinedload better for many to one relationship
            joinedload(ExerciseModel.course).joinedload(CourseModel.unit)
        )
        .first()
    )


    if not exercise:
        print("pas trouvé")
        # If the exercise don't exist 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice introuvable (Module {unit_id}, Cours {course_id}, Exo {exercise_id})"
        )

    if exercise.visibility == Visibility.PRIVATE or exercise.course.visibility == Visibility.PRIVATE or exercise.course.unit.visibility == Visibility.PRIVATE:
        # If is private
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Exercice, Cours ou Module privé (Module {unit_id}, Cours {course_id}, Exo {exercise_id})"
        )

    
    exercise_detail = ExerciseFull(
        id=exercise.id, 
        course_id=exercise.course_id,
        name=exercise.name,
        description=exercise.description,
        visibility=exercise.visibility,
        language=exercise.language,
        difficulty=exercise.difficulty,
        position=exercise.position,
        
        files= format_files_for_student(exercise.files),
        tests= format_tests_for_student(exercise.tests),
        hints= format_hints_for_student(exercise.hints)
    )

    print("ok")
    
    return {
        "status" : True, 
        "message" : "Exercice trouvé.",
        "data": exercise_detail.model_dump()
    }




async def test_student_code(db: Session, exercise_id: int, payload: StudentSubmissionPayload):

    exercise = (
        db.query(ExerciseModel)
        .options(
            # Do the loading of the files and tests now to not do it later
            selectinload(ExerciseModel.files),
            selectinload(ExerciseModel.tests),

            # To check the visibility of this exercise
            joinedload(ExerciseModel.course).joinedload(CourseModel.unit)
        )
        .filter(ExerciseModel.id == exercise_id)
        .first()
    )

    # Security 

    if not exercise:
        print("pas trouvé")
        # If the exercise don't exist 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice introuvable"
        )

    if exercise.visibility == Visibility.PRIVATE or exercise.course.visibility == Visibility.PRIVATE or exercise.course.unit.visibility == Visibility.PRIVATE:
        # If is private
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Exercice, Cours ou Module privé"
        )


    # Initialization 

    # Creating a new line for this submission
    submission = SubmissionHistoryModel(
            user_id=payload.user_id,
            exercise_id=exercise_id,
            status=SubmissionStatus.PENDING 
        )
    db.add(submission)

    # Flush it to have the id of the submission
    # Flush is different to commit, commit write the data in hard but flush not, 
    # Flush send the request, but the data is not written permenatly yet, I can stil use db.rollback
    try:
        db.flush() 
        submission_id = submission.id
    except Exception as e:
        print(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur inattendue est survenue : {str(e)}"
        )
    
    # Treatement 
    try: 
        # Parsing and save the student solution

        all_student_markers: List[MarkerData] = []

        for student_file in payload.files:
            # 'extract_student_solutions' return all the markers in this file
            markers = extract_student_solutions(student_file.content, student_file.extension)
            
            all_student_markers.extend(markers)

            # Save in the db
            for m in markers:
                db.add(SubmissionMarkerModel(
                    submission_id=submission_id,
                    exercise_file_id=student_file.id,
                    marker_id=m.id,
                    content=m.content
                ))

        # Reconstruction files (student markers + teacher template)

        print("Student  Markers ", all_student_markers)
        teacher_files : List[ExerciseFileModel] = exercise.files

        files_to_compile : List[File] = []

        for tf in teacher_files:
            if tf.is_main or not tf.editable:
                # Main and no editable file don't have markers (normally), don't need to check them
                final_content = tf.template_without_marker
            else:
                # Inject student code
                final_content = inject_markers_into_template(
                    tf.template_without_marker, 
                    all_student_markers, 
                    tf.extension
                )
            
            # Complete all the champ for the compilation is not optimal, I know. Temporary solution.
            reconstructed_file = File(
                id=tf.id,
                name=tf.name,
                content=final_content,
                extension=tf.extension,
                is_main=tf.is_main,
                editable=tf.editable,
                position=tf.position
            )

            files_to_compile.append(reconstructed_file)
        
        # Compilation 

        print("File rebuilt ", files_to_compile)

        tests : List[TestCaseModel] = exercise.tests

        argvs : List[str] = [t.argv if t.argv else "" for t in tests]

        # Compile and execute all the test
        exec_results = await compile_and_run_logics(
                    files_to_compile, 
                    payload.language, 
                    argvs
                )
        

        # Check if the program compile
        # compile_and_run_logics return a dictionnary if the compilation didn't work {status, message, data}
        if isinstance(exec_results, dict) and not exec_results.get("status", True):
             # The student fail this submission
             submission.status = SubmissionStatus.FAILURE
             # Commit the data
             db.commit() 
             
             return exec_results
        
        # Grading 

        print("Result ", exec_results)

        test_responses_list = []
        global_success = True
    
        # Loop in all the results 
        for i, result in enumerate(exec_results):
            test_case = tests[i]
            
            # Strip the output to compare them 
            student_output = (result["data"]["stdout"] or "").strip()
            expected_output = (test_case.expected_output or "").strip()
            error_log = result["data"]["stderr"]
            exit_code = result["data"]["exit_code"]

            # Vérification : Exit code 0 ET sortie identique
            is_success = (exit_code == 0) and (student_output == expected_output)
            
            if not is_success:
                global_success = False

            # Save the result in the db 
            db.add(SubmissionResultModel(
                submission_id=submission_id,
                test_case_id=test_case.id,
                status=SubmissionStatus.SUCCESS if is_success else SubmissionStatus.FAILURE,
                actual_output=student_output,
                error_log=error_log
            ))

            # Creating the respond for the front
            test_responses_list.append(TestResult(
                id= test_case.id,
                status= TestStatus.SUCCESS if is_success else  TestStatus.FAILURE,
                actual_output= student_output,
                error_log = error_log
                
            ))
        
        # Progression and finalisation of the submisison

        # Ubdate the status of the submission
        submission.status = SubmissionStatus.SUCCESS if global_success else SubmissionStatus.FAILURE

        # Update the progression for this exercice, if it don't exist, create it 
        progress = db.query(ExerciseProgressModel).filter_by(
            user_id=payload.user_id, 
            exercise_id=exercise_id
        ).first()

        if not progress:
            progress = ExerciseProgressModel(
                user_id=payload.user_id, 
                exercise_id=exercise_id,
                status=ProgressStatus.IN_PROGRESS,
                attempts_count=0
            )
            db.add(progress)
        
        progress.attempts_count += 1
        progress.last_activity = datetime.now()

        if global_success:
            progress.status = ProgressStatus.VALIDATED

        # Final commit
        db.commit()

        return {
            "status": True,
            "message": "Correction terminée",
            "data": {
                "test_responses" : test_responses_list}
             
        }
        
    except Exception as e:
        db.rollback()
        print(f"error in test_student_code function : {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erreur interne lors de la correction : {str(e)}"
        )
