from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.db.models import ExerciseModel, ExerciseFileModel, TestCaseModel, HintModel, CourseModel, UnitModel
from app.schemas.schemas import ExerciseFull, File, Test, Hint
from app.core.enums import Visibility


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
            UnitModel.visibility == Visibility.PUBLIC,
            CourseModel.visibility == Visibility.PUBLIC,
            ExerciseModel.visibility == Visibility.PUBLIC
        ) # Find the good exercise and check if it's public
        .options(
            selectinload(ExerciseModel.files),
            selectinload(ExerciseModel.tests),
            selectinload(ExerciseModel.hints)
        )
        .first()
    )


    if not exercise:
        print("pas trouvé")
        # If the exercise don't exist or is private (It is safer (IMO) to return a 404 (Not Found) rather than a 403 (Forbidden). We don't reveal that a exercise exists at this ID. ) .
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice introuvable (Module {unit_id}, Cours {course_id}, Exo {exercise_id})"
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

'''

def test_student_code_(exercise_id: id, student_files: List[File], language: Language):

    # Get the test for this exercice 
    tests = db_get_exercise_tests(exercise_id)
    print(tests)

    
    all_student_markers: List[MarkerData] = []
    
    for file in student_files:
        try:
            # Extract all the markers from the student files
            extracted = extract_student_solutions(file.content, language)
            all_student_markers.extend(extracted)
        
        finally:
            print(1)


'''