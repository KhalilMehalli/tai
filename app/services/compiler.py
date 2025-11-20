import os
import tempfile
import subprocess
from typing import List
from app.schemas.schemas import FileCreate, Language

COMPILER_CONFIG = {
    "c": {
        "compiler_cmd": ["gcc", "{input_files}", "-o", "app"],
        "run_cmd": ["./app"]
    }
}

def name_extension(file : FileCreate):
    """Function to ensure to combine the filename with his extension."""
    return f"{file.name}.{file.extension}"

def write_files_to_folder(files: List[FileCreate], folder_path : str):
    """ Writes all file objects to the folder_path directory. """
    try:
        for file in files:
            file_path = os.path.join(folder_path, name_extension(file))
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file.content)

        print(f"Files written in folder {folder_path}")
    except Exception as e:
        print(f"Writting error : {e}")
        raise e


def build_compilation_command(config: dict, files: List[FileCreate]):
    """
    Generates the command list for subprocess by replacing placeholders
    like {input_files} with actual file names and filtering headers.
    """
    cmd = []

    for arg in config["compiler_cmd"]:
        if arg == "{input_files}":
            for f in files:
                # Specific filter for C: only compile .c files, skip .h files
                if config["compiler_cmd"][0] == "gcc" and f.extension != "c":
                    continue 
                
                # Add the file name to the command
                cmd.append(name_extension(f)) 
        else:
            # Keep standard arguments (e.g., "-o", "app", etc.)
            cmd.append(arg)
            
    return cmd


def run_compilation(config: dict, files: List[FileCreate], tmp_dir: str):
    """
    Execute the compilation command in the tmp_dir using subprocess.
    """

    # 1. Build the command using the helper function
    cmd = build_compilation_command(config, files)

    try:
        result = subprocess.run(
            cmd, # args we will execute ["gcc", "file1.c", "-o", "app"] -> gcc file1.c -o app
            cwd=tmp_dir, # We go to the tmp_dir
            capture_output=True, 
            text=True
            #timeout=20             
        )

        is_success = (result.returncode == 0)

        return {"status": is_success,
                "message": "Compilation réussie" if is_success else "Échec de la compilation",
                "stdout": result.stdout, # 
                "stderr": result.stderr, # Error and warnings 
                "exit_code": result.returncode
            }

    except Exception as e:
        return {"status": False,
                "message": f"Erreur système interne : {str(e)}",
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1
            }

def run_execution(config: dict, tmp_dir: str, argv: str):
    """
    Executes the compiled code with optional arguments.
    """

    cmd = config["run_cmd"].copy() # .copy() to prevent modifying the global configuration by reference

    if argv:
        # extends : add all the content of the second list on the first list [1,2,3] and not [1, [2,3]]
        # split : parse the string "5 4 8" into a list of char ["5", "4", "8"]
        cmd.extend(argv.split())

    try:
        result = subprocess.run(
            cmd,
            cwd=tmp_dir,
            capture_output=True,
            text=True
            #timeout=2 
        )


        return {
            "status": (result.returncode == 0),
            "message": "Exécution terminée",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    except Exception as e:
        return {
            "status": False,
            "message": f"Erreur d'exécution : {str(e)}",
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }


async def compile_and_run_logic(files: List[FileCreate], language: Language, argv: str):
    """
    Main Pipeline:
    1. Create temporary directory.
    2. Write source files.
    3. Compile code.
    4. Execution .
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        
        # Write the files in this temporary folder
        try :
            write_files_to_folder(files, tmp_dir)
        except Exception as e:
            return {"status": False, "message": str(e)}
        
        # Get the right compiler depending of the language
        config = COMPILER_CONFIG.get(language)
        
        
        # Compilation
        compile_result = run_compilation(config, files, tmp_dir)

        if not compile_result["status"]:
            # Early return if compilation fails
            return compile_result

        print("compilation result: ", compile_result)

        # Execution  
        exec_result = run_execution(config, tmp_dir, argv)
        print("result runner :", exec_result)



        return exec_result
        
    
