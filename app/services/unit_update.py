from fastapi import  HTTPException, status
from app.db.models import UnitModel, CourseModel, ExerciseModel

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas.schemas import UnitSummary, UnitNav, CourseNav, ExerciseNav, CreationCourseRequest


def create_course(course_data: CreationCourseRequest, db: Session):

    unit = db.query(UnitModel).filter(UnitModel.id == course_data.unit_id).first()
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit not found")
    
    # Find the max value of  position in this unit and increment it
    max_position = db.query(func.max(CourseModel.position))\
    .filter(CourseModel.unit_id == course_data.unit_id)\
    .scalar()

    new_position = (max_position + 1) if max_position is not None else 1

    # Creation of the sqlAlchemy object 
    new_course_db = CourseModel(
        name=course_data.name,
        description=course_data.description,
        unit_id=course_data.unit_id,
        difficulty=course_data.difficulty,
        visibility=course_data.visibility,
        position=new_position
    )

    db.add(new_course_db)
    db.commit()
    db.refresh(new_course_db) 
    
    return CourseNav(
        id=new_course_db.id,
        name=new_course_db.name,
        description=new_course_db.description,
        visibility=new_course_db.visibility,
        difficulty=new_course_db.difficulty,
        position=new_course_db.position,
        author_id=unit.author_id, 
        
        exercises=[]
    )

def delete_course(course_id: int, db: Session):
    # Find the course
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    db.delete(course)
    db.commit()
    
    return None

def delete_exercise(exercise_id: int, db: Session):
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db.delete(exercise)
    db.commit()
    
    return None