

COMMENT_SYMBOLS = {
    "c":  r"//", "h" : r"//", "java" : r"//", "py" : "#"
}

# Configuration for each supported language
COMPILER_CONFIG: dict[str, dict] = {
    "c": {
        "compiler_cmd": ["gcc", "{input_files}", "-o", "app"],
        "run_cmd": ["./app"],
        "extension": "c",
        "main_name": "main"
    },
    "python": {
        "compiler_cmd": ["python3", "-m", "py_compile", "main.py"],
        "run_cmd": ["python3", "main.py"],
        "extension": "py",
        "main_name": "main"
    },
    "java": {
        "compiler_cmd": ["javac", "{input_files}"],
        "run_cmd": ["java", "Main"],
        "extension": "java",
        "main_name": "Main"
    }
}