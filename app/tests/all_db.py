from app.services.create_exercise import DB_EXERCISES, DB_FILES, DB_TEST, DB_HINT, DB_MARKERS

def get_all_db_c():

    markers_by_file_id: Dict[int, List[Dict[str, Any]]] = {}
    
    # Attach marks to their files 
    for marker_id, marker_data in DB_MARKERS.items():
        file_id = marker_data['exercise_file_id']
        
        if file_id not in markers_by_file_id:
            markers_by_file_id[file_id] = []
            
        marker_entry = marker_data.copy()
        marker_entry['id'] = marker_id
        markers_by_file_id[file_id].append(marker_entry)

    exercises: List[Dict[str, Any]] = []
    
    for id_exercice, general_info in DB_EXERCISES.items():
        

        exercise_detail = general_info.copy()
        exercise_detail["id"] = id_exercice 

        current_files: List[Dict[str, Any]] = []
        
        for file_id, file_data in DB_FILES.items():
            if file_data['exercise_id'] == id_exercice:
                
                file_entry = file_data.copy()
                file_entry['id'] = file_id
                

                file_entry['markers'] = markers_by_file_id.get(file_id, [])
                
                current_files.append(file_entry)
        
        exercise_detail["files"] = current_files

        # TESTS
        current_tests: List[Dict[str, Any]] = []
        for test_id, test_data in DB_TEST.items():
            if test_data['exercise_id'] == id_exercice:
                test_entry = test_data.copy()
                test_entry['id'] = test_id
                current_tests.append(test_entry)
        
        exercise_detail["tests"] = current_tests

        #  HINTS
        current_hints: List[Dict[str, Any]] = []
        for hint_id, hint_data in DB_HINT.items():
            if hint_data['exercise_id'] == id_exercice:
                hint_entry = hint_data.copy()
                hint_entry['id'] = hint_id
                current_hints.append(hint_entry)

        exercise_detail["hints"] = current_hints


        exercises.append(exercise_detail)
    
    return exercises
