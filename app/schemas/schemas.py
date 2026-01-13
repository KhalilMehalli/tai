from pydantic import BaseModel, Field
from typing import List
from app.core.enums import Extension, Language, Visibility, TestStatus


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

class TestResult(BaseModel):
    id: int
    status: TestStatus
    actual_output: str
    error_log : str
    


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
    files: List[FileCreate]

    # The tests 
    tests: List[TestCaseCreate]

    # The hints
    hints: List[HintCreate]

 # What the front will receive when a student demand an exercise
class ExerciseFull(BaseModel):
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


# Payload front will send when student test his code

class StudentSubmissionPayload(BaseModel):
    user_id: int
    language: Language
    files: List[File]

# Type for creating link to the units, courses and exercises

# Commun base for exercise, course and unit
class BaseNav(BaseModel):
    id: int
    name: str
    description: str 
    visibility: Visibility
    difficulty: int = Field(..., ge=1, le=5)
    author_id: int

# Ligth information of an exercice (without his files, etc...)
class ExerciseNav(BaseNav):
    position: int
    # Can be good in the futur to add attemps count or other info 

class CourseNav(BaseNav):
    position: int
    exercises: List[ExerciseNav] = []

class UnitNav(BaseNav):
    courses: List[CourseNav] = []

# Ligth information of all the unit a student need to do
class UnitSummary(BaseNav):
    pass


class CreationCourseRequest(BaseModel):
  name: str
  description: str
  difficulty: int
  visibility: Visibility
  unit_id: int
  author_id: int
