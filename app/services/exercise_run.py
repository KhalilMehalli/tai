from fastapi import HTTPException
from typing import List
from app.services.create_exercise import DB_EXERCISES, DB_FILES, DB_TEST, DB_HINT
from app.schemas.schemas import File, Test, Hint, Exercise, Visibility


def get_exercise_for_student(exercise_id: int):
    """
    Send the exercise to the student 
    """
    exercise = DB_EXERCISES.get(exercise_id)
    if exercise is None:
        raise HTTPException( # I will use HTTPexcepetion now, I need to change a portion of my code...
            status_code=404,
            detail= f"Exercice {exercise_id} n'existe pas"
        )
    
    if exercise["visibility"] == Visibility.PRIVATE:
        raise HTTPException(
            status_code=403,
            detail= "Cette exercice est privé"
        )

    # Files without the main and the markers

    files : List[File] = []

    for file_id, file_data in DB_FILES.items():
        if file_data["exercise_id"] != exercise_id:
            continue

        if file_data.get("is_main", False):
            # We don't send the main (test file) to the student
            continue

        files.append(
            File(
                id=file_id,
                name=file_data["name"],
                content=file_data["template_without_marker"],
                extension=file_data["extension"],
                is_main=file_data["is_main"],
                editable=file_data["editable"],
                position=file_data["position"]
            )
        )


    # Test
    tests: List[Test] = []
    for test_id, test_data in DB_TEST.items():
        if test_data["exercise_id"] != exercise_id:
            continue

        print(test_id)
        tests.append(
            Test(
                id=test_id,
                argv=test_data["argv"],
                expected_output=test_data["expected_output"],
                comment=test_data.get("comment", ""),
                position=test_data["position"],
            )
        )

    # Hint

    hints: List[Hint] = []

    for hint_id, hint_data in DB_HINT.items():
        if hint_data["exercise_id"] != exercise_id:
            continue

        print(hint_id)
        hints.append(
            Hint(
                id=hint_id,
                body=hint_data["body"],
                unlock_after_attempts=hint_data["unlock_after_attempts"],
                position=hint_data["position"],
            )
        )
        
    # General informations
    exercise_detail = Exercise(
        id=exercise_id,
        course_id=exercise["course_id"],
        name=exercise["name"],
        description=exercise["description"],
        visibility=exercise["visibility"],
        language=exercise["language"],
        difficulty=exercise["difficulty"],
        position=exercise["position"],
        files=files,
        tests=tests,
        hints=hints,
    )

    return {
        "status" : True, 
        "message" : "Exercice trouvé.",
        "data": exercise_detail.model_dump()
        

    }


