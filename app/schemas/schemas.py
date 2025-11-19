from pydantic import BaseModel, Field
from typing import List


# The composition of an exercise 

class FileCreate(BaseModel):
    name: str              # "main"
    content: str           # code complete with the markers 
    extension: str         # ".c or .java"
    is_main: bool = False
    editable: bool = False
    position: int

class TestCaseCreate(BaseModel):
    argv: str              # "5 10" or "5,7,8,9"
    expected_output: str   
    comment: str = ""
    position: int


class HintCreate(BaseModel):
    body: str
    unlock_after_attempts: int
    position: int


# What the front will send when the teacher finish completely an exercise

class ExerciseFullCreate(BaseModel):
    #  General informations 
    name: str
    description: str
    language: Language
    difficulty: int = Field(..., ge=1, le=5) # Automatic validation between [1,5]
    visibility: Visibility = Visibility.PRIVATE
    course_id: int
    position: int

    # The files 
    files: List[FileCreate]

    # The tests 
    tests: List[TestCaseCreate]

    # The hints
    hints: List[HintCreate]