from app.schemas.schemas import ExerciseFullCreate, FileCreate, TestCaseCreate, HintCreate
from app.utils.parsing import extract_teacher_markers_from_code

DB_EXERCISES = {}
DB_FILES = {}
DB_MARKERS = {}
DB_TEST = {}
DB_HINT = {}


def db_create_exercise(exercise_data: ExerciseFullCreate) -> int:
    # model_dump() convert the schema ExerciceFullCreate into a dict and excluse the keys files, tests and hints
    ex_dict = exercise_data.model_dump(exclude={"files", "tests", "hints"})
    
    new_id = len(DB_EXERCISES)
    DB_EXERCISES[new_id] = ex_dict
    return new_id

def db_create_files_and_markers(exercise_id: int, files: list[FileCreate]):
    for file in files:
        try:
            # Call our "extract_teacher_markers_from_code" which will separate the content of the markers from the file
            parsed_result = extract_teacher_markers_from_code(file.content, file.extension)
        except ValueError as e:
            raise ValueError(f"Probléme dans le fichier {file.name} : {e}")

        # File saved 
        file_id = len(DB_FILES)
        DB_FILES[file_id] = {
            "exercise_id": exercise_id,
            "name": file.name,
            "extension": file.extension,
            "editable": file.editable, 
            "template_without_marker": parsed_result.template, 
            "is_main": file.is_main,
            "position": file.position
        }

        # Save the markers of this file
        for marker in parsed_result.markers:
            marker_id = len(DB_MARKERS)
            DB_MARKERS[marker_id] = {
                "exercise_file_id": file_id,
                "marker_id": marker.id,
                "solution_content": marker.content
            }

def db_create_test(exercise_id: int, tests: list[TestCaseCreate]):
    for test in tests:
        test_id = len(DB_TEST)
        # On convertit l'objet Pydantic en dict
        data = test.model_dump()
        # On ajoute la clé étrangère
        data["exercise_id"] = exercise_id
        
        DB_TEST[test_id] = data

def db_create_hint(exercise_id: int, hints: list[HintCreate]):
    for hint in hints:
            hint_id = len(DB_HINT)
            data = hint.model_dump()
            data["exercise_id"] = exercise_id
            
            DB_HINT[hint_id] = data


# For later when the bdd are ON
def db_rollback_exercise(exercise_id: int):
    """
    Clean the BDD if something went wrong
    """


async def create_exercise_beta(exercise_data: ExerciseFullCreate):
    """
    Receive the complete data of an exercice when the teacher valid and exercice
    """
    try:
        # Exercice information treatment 
        ex_id = db_create_exercise(exercise_data)

        # Files and markers treatment
        if exercise_data.files:
            db_create_files_and_markers(ex_id, exercise_data.files)

        # Test treatment
        if exercise_data.tests:
            db_create_test(ex_id, exercise_data.tests)

        # Hint treatment
        if exercise_data.hints:
            db_create_hint(ex_id, exercise_data.hints)


        print("DB_Exercices", DB_EXERCISES)
        print("DB_Files", DB_FILES)
        print("DB_Markers", DB_MARKERS)
        print("DB_TEST", DB_TEST)
        print("DB_HINT", DB_HINT)

        return {
            "status": True, 
            "message": f"Exercise {exercise_data.name} a bien été crée"
        }
    
    except ValueError as e:
        #In case of an error (Parsing error here), delete all the exercise already created

        db_rollback_exercise(ex_id)
        return {
            "status": False,
            "message": str(e)
        }
    
    except Exception as e:
        #Error I didn't take into account
        
        db_rollback_exercise(ex_id)
        return {
            "status": False,
            "message": str(e)
        }



        



