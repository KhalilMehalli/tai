from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload, joinedload
from typing import List
from datetime import datetime

from app.db.models import ExerciseModel, ExerciseFileModel, TestCaseModel, HintModel, CourseModel, UnitModel, SubmissionHistoryModel, SubmissionMarkerModel, SubmissionResultModel, ExerciseProgressModel
from app.schemas.schemas import UnitSummary, UnitNav, CourseNav, ExerciseNav
from app.core.enums import Visibility



def get_all_units(user_id : int, db: Session):

    # For now, return all the unit because I don't have assign unit to user
    units = db.query(UnitModel).order_by(UnitModel.id).all()
    if not units:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Modules introuvables (bizzare)"
        )
    
    summary_list : List[UnitSummary] = []

    for unit in units:
        summary_list.append(UnitSummary(
            id=unit.id,
            name=unit.name,
            description=unit.description,
            visibility=unit.visibility,
            difficulty=unit.difficulty,
            author_id=unit.author_id
            )
        )
    print(summary_list)
            
    return summary_list    


def get_unit_structure(unit_id : int, user_id : int, db: Session ):
    """Retrieve all the children (course, exercise) of an unit"""

    unit = (
        db.query(UnitModel)
        .options(selectinload(UnitModel.courses).selectinload(CourseModel.exercises))
        .filter(UnitModel.id == unit_id)
        .first()
    )

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module introuvable"
        )


    if unit.visibility == Visibility.PRIVATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Module privé"
        )
    
    courses_nav_list : List[CourseNav] = []

    for course in unit.courses:
        exercises_nav_list : ExerciseNav = []

        for exercise in course.exercises:
            
            exercises_nav_list.append(ExerciseNav(
                id=exercise.id,
                name=exercise.name,
                description=exercise.description,
                position=exercise.position,
                visibility=exercise.visibility,
                difficulty=exercise.difficulty,
                author_id=unit.author_id
            ))

        courses_nav_list.append(CourseNav(
            id=course.id,
            name=course.name,
            description=course.description,
            position=course.position,
            visibility=course.visibility,
            difficulty=course.difficulty, 
            author_id=unit.author_id,
            exercises=exercises_nav_list 
        ))


    return UnitNav(
        id=unit.id,
        name=unit.name,
        description=unit.description,
        visibility=unit.visibility,
        difficulty=unit.difficulty, 
        author_id=unit.author_id,
        courses=courses_nav_list
    )