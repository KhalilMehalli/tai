from app.schemas.schemas import ExerciseFullCreate
from app.services.parsing import extract_markers_from_code

DB_EXERCISES = {}
DB_FILES = {}
DB_MARKERS = {}
DB_TEST = {}
DB_HINT = {}

async def create_exercise_beta(exercise_data: ExerciseFullCreate):
    """
    Receive the complete data of an exercice when the teacher valid and exercice
    """
    # Exercice information treatment 
    # .dict() convert the schema ExerciceFullCreate into a dict and excluse the keys files, tests and hints
    ex_info = exercise_data.dict(exclude={"files", "tests", "hints"})
    id_ex = len(DB_EXERCISES)
    DB_EXERCISES[id_ex] = ex_info


    # Files treatment
    for file in exercise_data.files:
        try: 
            # Call our "extract_markers_from_code" which will separate the content of the markers from the file
           parsed_result = extract_markers_from_code(file.content, file.extension) 
        except ValueError as e:
            return {
                "status": False, 
                "message": str(e)
            }


        # Creation of our exercice
        id_file = len(DB_FILES) 
        DB_FILES[id_file] = {
            "exercise_id": id_ex,
            "name": file.name,
            "template_without_marker": parsed_result.template, 
            "is_main": file.is_main,
            "position": file.position
        }


        # Markers treatment 
        for marker in parsed_result.markers:
            marker_id = len(DB_MARKERS) 
            DB_MARKERS[marker_id] = {
                "exercise_file_id": id_file,
                "marker_id": marker.id,
                "solution_content": marker.content
            }

    print("DB_Exercices", DB_EXERCISES)
    print("DB_Files", DB_FILES)
    print("DB_Markers", DB_MARKERS)
    return {
        "status": True, 
        "message": f"Exercise {exercise_data.name} created successfully"
    }



        



