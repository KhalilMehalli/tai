from fastapi import FastAPI, Depends
from app.schemas.schemas import (
    ExerciseFullCreate, TestRunRequest, CompileRequest, StudentSubmissionPayload, CourseCreate,
    UnitCreate, UnitUpdate, CourseUpdate, Exercise
)
from app.services.create_exercise import create_exercise, get_exercise_for_update, update_exercise
from app.services.compiler import compile_and_run_logic, compile_logic
from app.services.exercise_run import get_exercise_for_student, test_student_code
from app.services.InfoNaviagtion import get_all_units, get_unit_structure
from app.services.unit_update import (
    create_course, delete_course, delete_exercise,
    create_unit, update_unit, delete_unit, update_course
)

#from app.tests.all_db import get_all_db_c
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import get_db #, engine
from sqlalchemy.orm import Session 
from app.db import models 

# Create all the table if it's the first time c
#models.Base.metadata.create_all(bind=engine) used before alembic, now it's alembic which will configure the db

app = FastAPI()


origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:4200", 
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoints related to a unit 

@app.post("/create-unit")
def create_unit_endpoint(unit_data: UnitCreate, db: Session = Depends(get_db)):
    """Create a new unit"""
    result = create_unit(unit_data, db)
    return result

@app.put("/unit/{unit_id}")
def update_unit_endpoint(unit_id: int, update_data: UnitUpdate, db: Session = Depends(get_db)):
    """Update an existing unit"""
    result = update_unit(unit_id, update_data, db)
    return result


@app.delete("/unit/{unit_id}")
def delete_unit_endpoint(unit_id: int, db: Session = Depends(get_db)):
    """Delete a unit and all its children"""
    result = delete_unit(unit_id, db)
    return result

# Endpoints related to a course 

@app.post("/create-course")
def create_course_endpoint(course_data: CourseCreate, db: Session = Depends(get_db)):
    print(course_data)
    """ Route call after the teacher create a course"""
    result = create_course(course_data, db) 
    return result

@app.delete("/course/{course_id}")
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db)): 
    """ Route call when a teacher delete a course"""
    result = delete_course(course_id, db) 
    return result

@app.put("/course/{course_id}")
def update_course_endpoint(course_id: int, update_data: CourseUpdate, db: Session = Depends(get_db)):
    """Update an existing course"""
    result = update_course(course_id, update_data, db)
    return result

# Endpoints related to an exercise
  
@app.post("/exercises")
def create_exercise_endpoint(exercise_data: ExerciseFullCreate, db : Session = Depends(get_db)):
    """ Route call after the teacher use the button 'VALIDER'. """
    print(exercise_data)
    result = create_exercise(exercise_data, db)
    return result

@app.delete("/exercise/{exercise_id}")
def delete_exercise_endpoint(exercise_id: int, db: Session = Depends(get_db)):
    """ Route call when a teacher delete a exercise"""
    result = delete_exercise(exercise_id, db)
    return result

@app.get("/update/exercise/{exercise_id}")
def get_exercise_for_teacher_endpoint(exercise_id: int, db: Session = Depends(get_db)):
    """Get full exercise with reconstructed files for teacher editing"""
    result = get_exercise_for_update(exercise_id, db)
    return result


@app.put("/exercise/{exercise_id}")
def update_exercise_endpoint(exercise_data: Exercise, db: Session = Depends(get_db)):
    """Full update of an exercise (files, tests, hints)"""
    print(exercise_data)
    result = update_exercise(exercise_data, db)
    return result


# Endpoint use in the creation of a new exercise 

@app.post("/run_test")
async def test_exercise_endpoint(request: TestRunRequest):
    """ Route call after the teacher when to test one of his test """
    result = await compile_and_run_logic(request.files,request.language,request.argv)
    return result

@app.post("/compilation")
async def compilation_teacher_code_endpoint(request: CompileRequest):
    print(request)
    """ Route call after the teacher compile his code to test it """
    result = await compile_logic(request.files, request.language) 
    return result





# Student doing an exercise

@app.get("/student/unit/{unit_id}/course/{course_id}/exercise/{exercise_id}")
def get_exercise_student_endpoint(unit_id : int, course_id: int,  exercise_id: int, db : Session = Depends(get_db)):
    """ Route call when a student want to do an exercise"""
    exercise = get_exercise_for_student(unit_id, course_id, exercise_id, db)  
    return exercise


@app.post("/student/unit/{unit_id}/course/{course_id}/exercise/{exercise_id}")
async def test_student_code_endpoint(exercise_id : int, payload: StudentSubmissionPayload,  db : Session = Depends(get_db)):
    """ Route call when a student want to test his solution for an exercise"""
    results = await test_student_code(db, exercise_id, payload)
    return results

# Ligth information of unit, course and exercise for navigation


@app.get("/units")
def get_all_ligth_units_informations(user_id : int, db: Session = Depends(get_db)):
    """Send a summary of all the unit the user can do. For the dashbord"""
    results = get_all_units(user_id, db)
    return results

@app.get("/unit/{unit_id}/courses")
def get_all_ligth_unit_informations(unit_id : int, user_id : int, db: Session = Depends(get_db)):
    """Send the information of all the course and exercise in a unit. """
    print("test")
    results = get_unit_structure(unit_id, user_id, db)
    return results



"""
# Test
@app.get("/tests/db")
def get_all_db_content():

    exercises = get_all_db_c()
        
    return exercises
"""

@app.get("/")
def root():
    return {"message": "Hello World"}
