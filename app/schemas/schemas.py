from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# Enums. Will automaticaly reject a valeur not in an Enum and better readability

class Language(str, Enum):
    C = "c"

class Extension(str, Enum):
    C = "c"
    H = "h" 

class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"

# The composition of an exercise 

class FileCreate(BaseModel):
    name: str # "main"
    content: str # code complete with the markers or without depending of the case
    extension: Extension # "c or java"
    is_main: bool = False
    editable: bool = False
    position: int

class TestCaseCreate(BaseModel):
    argv: str  # "5 10" or "5,7,8,9"
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
    course_id: int
    name: str
    description: str
    visibility: Visibility
    language: Language
    difficulty: int = Field(..., ge=1, le=5) # Automatic validation between [1,5]
    position: int

    # The files 
    files: List[FileCreate]

    # The tests 
    tests: List[TestCaseCreate]

    # The hints
    hints: List[HintCreate]


# 

class CompileRequest(BaseModel):
    files: List[FileCreate]
    language: Language

class TestRunRequest(BaseModel):
    files: List[FileCreate]
    language: Language
    argv: str 

