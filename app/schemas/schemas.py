from pydantic import BaseModel, Field
from typing import List
from app.core.enums import Extension, Language, Visibility


# The composition of an exercise 

class FileCreate(BaseModel):
    name: str # "main"
    content: str # code complete with the markers or without depending of the case
    extension: Extension # "c or java"
    is_main: bool 
    editable: bool 
    position: int

class File(FileCreate):
    id: int

class TestCaseCreate(BaseModel):
    argv: str  # "5 10" or "5,7,8,9"
    expected_output: str   
    comment: str = ""
    position: int

class Test(TestCaseCreate):
    id: int

class HintCreate(BaseModel):
    body: str
    unlock_after_attempts: int
    position: int

class Hint(HintCreate):
    id: int

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
    files: List[File]

    # The tests 
    tests: List[Test]

    # The hints
    hints: List[Hint]

class Exercise(ExerciseFullCreate):
    id: int

# Type for teacher

class CompileRequest(BaseModel):
    files: List[FileCreate]
    language: Language

class TestRunRequest(CompileRequest):
    argv: str 


# Type for student

class CodeRequest(BaseModel):
    files: List[File]
    language: Language

