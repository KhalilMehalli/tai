from enum import Enum

# Enums. Will automaticaly reject a valeur not in an Enum and better readability

class Language(str, Enum):
    C = "c"

class Extension(str, Enum):
    C = "c"
    H = "h"
    TXT = "txt" 

class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class SubmissionStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"

class ProgressStatus(str,Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    VALIDATED = "validated"

class TestStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"

    