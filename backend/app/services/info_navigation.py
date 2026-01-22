"""
Navigation service for retrieving unit/course/exercise structures.

This module provides functions to fetch lightweight navigation data
for the dashboard, unit views and side navigation panel in exerise-run.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.db.models import CourseModel, UnitModel
from app.schemas.schemas import UnitSummary, UnitNav, CourseNav, ExerciseNav


def get_all_units(user_id: int, db: Session) -> list[UnitSummary]:
    """
    Get a summary of all units for the dashboard.

    """
    units = db.query(UnitModel).order_by(UnitModel.id).all()
    if not units:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No units found"
        )

    summary_list: list[UnitSummary] = []

    for unit in units:
        summary_list.append(UnitSummary(
            id=unit.id,
            name=unit.name,
            description=unit.description,
            visibility=unit.visibility,
            difficulty=unit.difficulty,
            author_id=unit.author_id
        ))
    print(summary_list)

    return summary_list


def get_unit_structure(unit_id: int, user_id: int, db: Session) -> UnitNav:
    """
    Retrieve the full structure of a unit with all courses and exercises.
    """
    unit = (
        db.query(UnitModel)
        .options(selectinload(UnitModel.courses).selectinload(CourseModel.exercises))
        .filter(UnitModel.id == unit_id)
        .first()
    )

    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )

    courses_nav_list: list[CourseNav] = []

    for course in unit.courses:
        exercises_nav_list: list[ExerciseNav] = []

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