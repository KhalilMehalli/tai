from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload, joinedload
from typing import List, Tuple
from datetime import datetime

from app.db.models import ExerciseModel, ExerciseFileModel, TestCaseModel, HintModel, CourseModel, UnitModel, SubmissionHistoryModel, SubmissionMarkerModel, SubmissionResultModel, ExerciseProgressModel
from app.schemas.schemas import ExerciseFull, File, Test, Hint, StudentSubmissionPayload, TestResult
from app.core.enums import Visibility, SubmissionStatus, ProgressStatus, Language, TestStatus

from app.utils.parsing import extract_student_solutions, inject_markers_into_template, MarkerData
from app.services.compiler import compile_and_run_logics

# ---------------- Shared helper for both get_exercise_for_student and test_student_code function -----#
def get_secure_exercise_or_404(db: Session, exercise_id: int) -> ExerciseModel:
    """
    Fetches the exercise with all necessary relationships loaded.
    Raises 404 if not found or 403 if private (and user has no access).
    """

    exercise = (
        db.query(ExerciseModel)
        .options(
            # selectinload loads the kids of Exercise (files, hint, tests) in the same requestfor better performance
            selectinload(ExerciseModel.files),
            selectinload(ExerciseModel.tests),
            selectinload(ExerciseModel.hints),

            #joinedload better for many to one relationship
            joinedload(ExerciseModel.course).joinedload(CourseModel.unit)
        )
        .filter(ExerciseModel.id == exercise_id)
        .first()
    )

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice introuvable"
        )

    is_private = (
        exercise.visibility == Visibility.PRIVATE or 
        exercise.course.visibility == Visibility.PRIVATE or 
        exercise.course.unit.visibility == Visibility.PRIVATE
    )

    if is_private:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Exercice, Cours ou Module privé"
        )

    return exercise


# ------------ Helper for get_exercise_for_student function --------------------- #

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

    
    exercise = get_secure_exercise_or_404(db, exercise_id)

    
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


# ------------ Helper for test_student_code function --------------------- #

def initialize_submission_history(db: Session, user_id: int, exercise_id: int) -> SubmissionHistoryModel:
    """Creates a pending submission entry and returns its ID."""
    submission = SubmissionHistoryModel(
        user_id=user_id,
        exercise_id=exercise_id,
        status=SubmissionStatus.PENDING 
    )
    db.add(submission)
    # Flush sends the SQL to generate the ID but keeps the transaction open
    # Unlike commit which write data permanently, flush allows us to still use db.rollback
    # if an error occurs later.
    
    db.flush() 
    return submission

def update_student_progress(db: Session, user_id: int, exercise_id: int, is_success: bool):
    """Updates or creates the progress entry for the student."""

    progress = db.query(ExerciseProgressModel).filter_by(
        user_id=user_id, 
        exercise_id=exercise_id
    ).first()

    if not progress:
        progress = ExerciseProgressModel(
            user_id=user_id, 
            exercise_id=exercise_id,
            status=ProgressStatus.IN_PROGRESS, 
            attempts_count=0
        )
        db.add(progress)
    
    progress.attempts_count += 1
    progress.last_activity = datetime.now()

    if is_success:
        progress.status = ProgressStatus.VALIDATED

def process_and_save_markers(db: Session, submission_id: int, payload_files: List[File]) -> List[MarkerData]:
    """Extracts student markers and saves them to the DB."""
    all_markers: List[MarkerData] = []

    for student_file in payload_files:
        markers = extract_student_solutions(student_file.content, student_file.extension)
        all_markers.extend(markers)

        for m in markers:
            db.add(SubmissionMarkerModel(
                submission_id=submission_id,
                exercise_file_id=student_file.id,
                marker_id=m.id,
                content=m.content
            ))
    return all_markers

def reconstruct_files_for_compilation(exercise_files: List[ExerciseFileModel], student_markers: List[MarkerData]) -> List[File]:
    """Merges student markers into teacher templates."""
    files_to_compile: List[File] = []

    for tf in exercise_files:
        if tf.is_main or not tf.editable:
            # Main and non editable files don't have markers (normally), keep original content.
            final_content = tf.template_without_marker
        else:
            # Inject student code into the template.
            final_content = inject_markers_into_template(
                tf.template_without_marker, 
                student_markers, 
                tf.extension
            )
        
        # Filling all fields of File for compilation isn't optimal, I know. Temporary solution (If I don't forget).
        files_to_compile.append(File(
            id=tf.id,
            name=tf.name,
            content=final_content,
            extension=tf.extension,
            is_main=tf.is_main,
            editable=tf.editable,
            position=tf.position
        ))
    
    return files_to_compile

def grade_submisison(db: Session, submission_id: int, exec_results: List[dict], tests: List[TestCaseModel]) -> Tuple[bool, List[TestResult]]:
    """
    Compares execution results with expected outputs, saves results to DB, 
    and returns global success status + list of users output for frontend.
    """
    test_responses_list : List[TestResult] = []
    global_success = True

    for i, result in enumerate(exec_results):
        test_case = tests[i]
        
        print("test result", result)
        # Data cleaning and extraction
        student_output = (result["data"]["stdout"] or "").strip()
        expected_output = (test_case.expected_output or "").strip()
        error_log = result["data"]["stderr"]
        exit_code = result["data"]["exit_code"]

        # Verdict Logic
        is_success = (exit_code == 0) and (student_output == expected_output)
        
        if not is_success:
            global_success = False

        # Save to DB
        db.add(SubmissionResultModel(
            submission_id=submission_id,
            test_case_id=test_case.id,
            status=SubmissionStatus.SUCCESS if is_success else SubmissionStatus.FAILURE,
            actual_output=student_output,
            error_log=error_log
        ))

        # Prepare Frontend Response
        test_responses_list.append(TestResult(
            id=test_case.id,
            status=TestStatus.SUCCESS if is_success else TestStatus.FAILURE,
            actual_output=student_output,
            error_log=error_log
        ))
    
    return global_success, test_responses_list

async def test_student_code(db: Session, exercise_id: int, payload: StudentSubmissionPayload):
    """
    Pipeline for testing student code.
    Steps: Security(Exercise exist and exercise not private) -> Init submission_history -> Parse/Save student solution 
    -> Reconstruct files -> Compile/Run -> Grade/Saving the answer of the student.
    """

    # Security (Outside try/except because it return a HTTPExceptions for error)
    exercise = get_secure_exercise_or_404(db, exercise_id)

    try: 
        #Initialization 
        submission = initialize_submission_history(db, payload.user_id, exercise_id)
        submission_id = submission.id

        # Parsing and save the student solution
        all_student_markers: List[MarkerData] = process_and_save_markers(db, submission_id, payload.files)

        # Reconstruction files (student markers + teacher template)
        # We use exercise.files directly (loaded via selectinload)
        print("Student  Markers ", all_student_markers)
        teacher_files : List[ExerciseFileModel] = exercise.files
        files_to_compile : List[File] = reconstruct_files_for_compilation(teacher_files, all_student_markers)
        
        # Compilation 
        print("File rebuilt ", files_to_compile)
        # sort the tests to ensure the test are in the right order
        sorted_tests : List[TestCaseModel] = sorted(exercise.tests, key=lambda t: t.position)
        argvs : List[str] = [t.argv if t.argv else "" for t in sorted_tests]

        # Compile and execute all the test
        exec_results = await compile_and_run_logics(
                    files_to_compile, 
                    payload.language, 
                    argvs
                )

        # Check for compilation failure
        # compile_and_run_logics return a dictionnary if the compilation didn't work {status, message, data}
        if isinstance(exec_results, dict) and not exec_results.get("status", True):
             submission.status = SubmissionStatus.FAILURE
             db.commit()    
             print("Error compile", exec_results)
             return exec_results # returns the error dict directly
        
        print("Result ", exec_results)

        # Grading 
        global_success, test_responses_list = grade_submisison(db, submission_id, exec_results, sorted_tests)
        
        # Ubdate the status of the submission
        submission.status = SubmissionStatus.SUCCESS if global_success else SubmissionStatus.FAILURE

        # Update the progression for this exercice, if it don't exist, create it 
        update_student_progress(db, payload.user_id, exercise_id, global_success)

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
