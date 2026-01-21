import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.schemas import (
    ExerciseFullCreate, FileCreate, TestCaseCreate, HintCreate,
    Exercise, Test, Hint
)
from app.db.models import ExerciseModel, ExerciseFileModel, ExerciseMarkerModel, TestCaseModel, HintModel, CourseModel

from app.utils.parsing import extract_teacher_markers_from_code, reconstruct_file_with_markers

def prepare_files_and_markers(files_data: list[FileCreate]) -> list[ExerciseFileModel]:
    """Prepare the sqlAlchemy object ExerciseFileModel and ExerciseMarkerModel without saving them"""
    exercise_files = []
    for file_data in files_data:
        try:
            parsed_result = extract_teacher_markers_from_code(file_data.content, file_data.extension)
        except ValueError as e:
            # Call our "extract_teacher_markers_from_code" which will separate the content of the markers from the file
            raise ValueError(f"Erreur de syntaxe dans le fichier '{file_data.name}': {str(e)}")

        new_file = ExerciseFileModel(
            name=file_data.name,
            extension=file_data.extension,
            is_main=file_data.is_main,
            editable=file_data.editable,
            position=file_data.position,
            template_without_marker=parsed_result.template
        )
        for marker in parsed_result.markers:
            new_file.markers.append(ExerciseMarkerModel(
                marker_id=marker.id,
                solution_content=marker.content
            ))
        exercise_files.append(new_file)
    return exercise_files

def prepare_tests(tests_data: list[TestCaseCreate]) -> list[TestCaseModel]:
    return [TestCaseModel(**test.model_dump()) for test in tests_data]

def prepare_hints(hints_data: list[HintCreate]) -> list[HintModel]:
    return [HintModel(**hint.model_dump()) for hint in hints_data]


def create_exercise(exercise_data: ExerciseFullCreate, db: Session):
    """
    Receive the complete data of an exercice when the teacher valid and exercice
    """
    try:
        
        # Check if the course exist before creating the new cexercise
        course_exists = db.query(CourseModel).filter(CourseModel.id == exercise_data.course_id).first()
        
        if not course_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Le cours avec l'id {exercise_data.course_id} n'existe pas."
            )

            
        # Creation of the ExerciseModel Object
        exercise_info = exercise_data.model_dump(exclude={"files", "tests", "hints"})
        new_exercise = ExerciseModel(**exercise_info)

        # Prepare and attach the children ExerciseFIleMOdel, TestCaseModel and HintModel to the ExerciseModel Object 
        if exercise_data.files:
            new_exercise.files.extend(prepare_files_and_markers(exercise_data.files))
        
        if exercise_data.tests:
            new_exercise.tests.extend(prepare_tests(exercise_data.tests))

        if exercise_data.hints:
            new_exercise.hints.extend(prepare_hints(exercise_data.hints))

        # Communication with the db
        db.add(new_exercise)
        db.commit() # COmmit the change
        db.refresh(new_exercise) # Get the id of the new exercise

        return {
            "status": True,
            "message": f"L'exercice '{new_exercise.name}' a bien été créé.",
            "data": {
                "id": new_exercise.id
            }
        }

    
    except ValueError as e:
        #In case of an parsing error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )

    except SQLAlchemyError as e:
        # Error when communicating with the db
        print(str(e))
        db.rollback() # clean the session, no need to do other thing because we didn't commit yet
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'enregistrement en base de données : {str(e)}"
        )

    except Exception as e:
        #Error I didn't take into account
        print(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur inattendue est survenue : {str(e)}"
        )





def get_exercise_for_update(exercise_id: int, db: Session):
    """
    Get full exercise with reconstructed files (with <complete> markers) for teacher editing
    """
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"L'exercice avec l'id {exercise_id} n'existe pas."
        )

    # Reconstruct files with <complete> markers
    files = []
    for file in exercise.files:
        reconstructed_content = reconstruct_file_with_markers(
            file.template_without_marker,
            file.markers,
            file.extension
        )
        files.append(FileCreate(
            name=file.name,
            content=reconstructed_content,
            extension=file.extension,
            is_main=file.is_main,
            editable=file.editable,
            position=file.position
        ))

    # Convert tests to schema
    tests = [
        Test(
            id=t.id,
            argv=t.argv or "",
            expected_output=t.expected_output,
            comment=t.comment or "",
            position=t.position
        ) for t in exercise.tests
    ]

    # Convert hints to schema
    hints = [
        Hint(
            id=h.id,
            body=h.body,
            unlock_after_attempts=h.unlock_after_attempts,
            position=h.position
        ) for h in exercise.hints
    ]

    print(files, tests, hints)

    return Exercise(
        id=exercise.id,
        course_id=exercise.course_id,
        name=exercise.name,
        description=exercise.description,
        visibility=exercise.visibility,
        language=exercise.language,
        difficulty=exercise.difficulty,
        position=exercise.position,
        files=files,
        tests=tests,
        hints=hints
    )


def update_exercise(exercise_data: Exercise, db: Session):
    """
    Full update of an exercise: replaces files, tests, and hints entirely
    """
    try:
        exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_data.id).first()

        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"L'exercice avec l'id {exercise_data.id} n'existe pas."
            )

        # Update basic info
        exercise.name = exercise_data.name
        exercise.description = exercise_data.description
        exercise.difficulty = exercise_data.difficulty
        exercise.visibility = exercise_data.visibility
        exercise.language = exercise_data.language

        # Delete old files, tests, hints (cascade will handle children)
        for file in exercise.files:
            db.delete(file)
        for test in exercise.tests:
            db.delete(test)
        for hint in exercise.hints:
            db.delete(hint)

        # Clear the lists
        exercise.files.clear()
        exercise.tests.clear()
        exercise.hints.clear()

        # Add new files, tests, hints
        if exercise_data.files:
            exercise.files.extend(prepare_files_and_markers(exercise_data.files))

        if exercise_data.tests:
            exercise.tests.extend(prepare_tests(exercise_data.tests))

        if exercise_data.hints:
            exercise.hints.extend(prepare_hints(exercise_data.hints))

        db.commit()
        db.refresh(exercise)

        return {
            "status": True,
            "message": f"L'exercice '{exercise.name}' a bien ete mis a jour.",
            "data": {
                "id": exercise.id
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except SQLAlchemyError as e:
        print(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise a jour en base de donnees : {str(e)}"
        )

    except Exception as e:
        print(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur inattendue est survenue : {str(e)}"
        )

