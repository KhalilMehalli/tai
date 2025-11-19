from fastapi import FastAPI
from app.schemas.schemas import ExerciseFullCreate
from app.services.create_exercise import create_exercise_beta

app = FastAPI()

@app.post("/exercises")
async def create_exercise_endpoint(exercise_data: ExerciseFullCreate):
    """
    Route call after the teacher use the button 'VALIDER'.
    """

    result = await create_exercise_beta(exercise_data)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result


@app.get("/")
def root():
    return {"message": "Hello World"}