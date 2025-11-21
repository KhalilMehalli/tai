from fastapi import FastAPI
from app.schemas.schemas import ExerciseFullCreate, TestRunRequest, CompileRequest
from app.services.create_exercise import create_exercise_beta
from app.services.compiler import compile_and_run_logic, compile_logic


app = FastAPI()

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
    """ Route call after the teacher compile his code to test it """
    result = await compile_logic(request.files, request.language) 
    return result


@app.get("/")
def root():
    return {"message": "Hello World"}
