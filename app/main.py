from fastapi import FastAPI
from app.schemas.schemas import ExerciseFullCreate, TestRunRequest, CompileRequest, CodeRequest
from app.services.create_exercise import create_exercise_beta
from app.services.compiler import compile_and_run_logic, compile_logic
from app.services.exercise_run import get_exercise_for_student, test_student_code_
from app.tests.all_db import get_all_db_c
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Creation exercise 

@app.post("/exercises")
async def create_exercise_endpoint(exercise_data: ExerciseFullCreate):
    """ Route call after the teacher use the button 'VALIDER'. """
    result = await create_exercise_beta(exercise_data)
    return result


@app.post("/run_test")
async def test_exercise(request: TestRunRequest):
    """ Route call after the teacher when to test one of his test """
    result = await compile_and_run_logic(request.files,request.language,request.argv)
    return result

@app.post("/compilation")
async def compilation_teacher_code(request: CompileRequest):
    print(request)
    """ Route call after the teacher compile his code to test it """
    result = await compile_logic(request.files, request.language) 
    return result


# Student 

@app.get("/student/exercise/{exercise_id}")
def get_exercise_student(exercise_id: int):

    exercise = get_exercise_for_student(exercise_id)  
    return exercise

@app.post("/student/exercise/{exercise_id}/test")
def test_student_code(exercise_id: int, request: CodeRequest):

    test_student_code_(exercise_id, request.files, request.language)
    return

# Test
@app.get("/tests/db")
def get_all_db_content():

    exercises = get_all_db_c()
        
    return exercises


@app.get("/")
def root():
    return {"message": "Hello World"}
