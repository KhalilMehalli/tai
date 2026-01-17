import re
from typing import List
from dataclasses import dataclass

# dataclass allow us to create a class quickly without writting the __init__, etc..
@dataclass
class MarkerData:
    id: str # <complete id=...>
    content: str

@dataclass
class ParsedResult:
    template: str # code complete without the content of the marker. 
    # The content inside the markers and the markers has been remplace by TODOs
    markers: List[MarkerData]


COMMENT_SYMBOLS = {
    "c":  r"//", "h" : r"//", "java" : r"//", "py" : "#"
}


def get_line_indentation(full_content: str, target_index: int) -> str:
    """
    Retrieves the indentation (spaces/tabs) of the line containing the markers.
    Important for language where indentation matters (Python)
    """
    # Search for the last newline before the start
    last_newline = full_content.rfind('\n', 0, target_index)
    
    # We extract 
    #(           // <complete ...>) all this part 
    if last_newline == -1:
        line_prefix = full_content[:target_index] # First line case
    else:
        line_prefix = full_content[last_newline+1 : target_index]
    
    # We only keep spaces 
    #((this part )// <complete ...>)
    indentation = ""
    for char in line_prefix:
        if char.isspace():
            indentation += char
        else:
            break # When we find something other than a space, we break 
            
    return indentation

def extract_teacher_markers_from_code(full_content: str, extension : str):
    """
    Parses the raw code to separate the template from the markers and their content.
    """

    comment = COMMENT_SYMBOLS.get(extension)
    if comment is None:
        # This file cannot have a markers (ex : txt file)
        return ParsedResult(template=full_content, markers=[])
    
    # Regex explanation:
    # {comment}\s*<complete\s*id="(?P<id>.*?)"> Start when it find a marker and capture the name of the id 
    # \s* spaces 
    #  (?P<content>.*?) -> Tell that after a marker, the content needs to be store under the name content 
    # {comment}</complete> -> End when it find the closing marker 


    pattern = rf'{comment}\s*<complete\s*id\s*=\s*(?P<id>.*?)\s*>(?P<content>.*?){comment}\s*</complete>'

    markers_found: List[MarkerData] = []
    
    def replacement_logic(match):
        # Extract data from the regex groups
        m_id = match.group("id").strip()
        content = match.group("content")

        # Security Check, if a teacher writes a marker inside a marker : error 
        if "<complete" in content:
             raise ValueError(f"Erreur dans la balise '{m_id}': une balise imbriquée a été trouvée. Vérifiez votre balise fermante (</complete>)")
        
        # Store the marker and his content 
        markers_found.append(MarkerData(id=m_id, content=content))

        # Retrieve the indentation of the line where the markers was 
        indentation = get_line_indentation(full_content, match.start())

        return f"{comment} TODO: {m_id}\n\n{indentation}{comment} END TODO: {m_id}"

    # re.sub runs the replacement_logic function for every match found
    template_content = re.sub(pattern, replacement_logic, full_content, flags=re.DOTALL)

    print(template_content)
    
    return ParsedResult(template=template_content, markers=markers_found)


def inject_markers_into_template(template_content: str, markers: List[MarkerData], extension: str) -> str:
    """
    Inverse operation of extract_teacher_markers_from_code.
    Inject the code in the markers back into the template.
    """

    comment = COMMENT_SYMBOLS.get(extension)

    # List -> Dict, faster to find the content of the markers with the id
    marker_map = {str(m.id): m.content for m in markers}

    pattern = rf'{comment} TODO: (?P<id>.*)\n\n\s*{comment} END TODO: (?P=id)'

    def replacement_logic(match):
        m_id = match.group("id").strip()
        
        # Inject directly the marker's content at the location of //TODO ... // END TODO
        return marker_map[m_id]

    full_code = re.sub(pattern, replacement_logic, template_content)
    
    return full_code

def extract_student_solutions(full_content: str, extension : str, expected_markers_ids: List[str] = None) -> List[MarkerData]:
    """
    Parses the student code and extract his solutions.
    """

    comment = COMMENT_SYMBOLS.get(extension)
    pattern = rf'{comment} TODO: (?P<id>.*)\n(?P<content>.*?)(?=\n\s*{comment} END TODO: (?P=id))'

    markers_found: List[MarkerData] = []
    # Security to check if all the markers are here
    found_ids = set()

    for match in re.finditer(pattern, full_content, flags=re.DOTALL):
        m_id = match.group("id").strip()
        content = match.group("content")

        markers_found.append(MarkerData(id=m_id, content=content))
        found_ids.add(m_id)

    if expected_markers_ids:
        missing_ids = set(expected_markers_ids) - found_ids

        # If an markers is not found
        if missing_ids:
            raise ValueError(
                f"Les balises suivantes sont manquantes ou altérées : {', '.join(missing_ids)}"
            )

    return markers_found

if __name__ == "__main__":

    c_code = """ //  <complete id = "65">
        #include <stdio.h>
        //  </complete>

        int main() {
            //<complete id="1">
            int a = 5;
            int b = 10;
            //</complete>

            // Normal comment
            printf("Hello");

            //   <complete id="2">
            return 0;
            //   </complete>
        }
    """

    c_code_with_error = """ 
        #include <stdio.h>

        int main() {
            //<complete id="1">
            int a = 5;
            int b = 10;

            //<complete id="3">
            // Normal comment
            printf("Hello");
            //</complete>

            //</complete>

            //   <complete id="2">
            return 0;
            //   </complete>
        }
    """

    c_student_code = """
// TODO: "65"
je sais pas  
// END TODO: "65"

    int main() {
        // TODO: "1"
        salut 
        // END TODO: "1"

        // Normal comment
        printf("Hello");

        // TODO: "2"
            test2
        // END TODO: "2"
    }
    """

    try: 
        print("Original code")
        print(c_code)

        result_extract = extract_teacher_markers_from_code(c_code,"c")

        print("Template of the code wothout the markers\n", result_extract.template)

        print("Content of the markers + id \n")
        for m in result_extract.markers:
                    print(f"ID: {m.id}")
                    print(f"Content: {m.content}") 
        
        result_inject = inject_markers_into_template(result_extract.template,result_extract.markers,"c")

        print("Template of the code with the markers re-injected\n", result_inject)

        print("Student code\n", c_student_code)
        print(extract_student_solutions(c_student_code,"c"))



    except ValueError as e:
        print(e)