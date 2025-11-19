import re
from typing import List, Tuple
from dataclasses import dataclass

# dataclass allow to create a class quickly without writting the __init__, etc..
@dataclass
class MarkerData:
    id: str # <complete id=...>
    content: str

@dataclass
class ParsedResult:
    template: str # code complete without the content of the marker, 
    #the content inside the markers and the markers has been remplace by 
    markers: List[MarkerData]


COMMENT_SYMBOLS = {
    "c":  r"//", "h" : r"//"
}


def extract_markers_from_code(full_content: str, extension : str) -> ParsedResult:
    """
    Parses the raw code to separate the template from the markers and his content.
    """

    comment = COMMENT_SYMBOLS.get(extension)
    
    # Regex explanation:
    # {comment}<complete id="(?P<id>.*?)"> Start when he find a marker and capture the name of the id 
    # \s* spaces 
    #  (?P<content>.*?) -> Tell that after a marker, the content need to be store under the name content 
    # {comment}</complete> -> End when he find the closing marker 
    # re.DOTALL allows the dot (.) to match newlines (essential for multi-line code)

    pattern = rf'{comment}\s*<complete id="(?P<id>.*?)">(?P<content>.*?){comment}\s*</complete>'

    markers_found: List[MarkerData] = []
    
    def replacement_logic(match):
        # Extract data from the regex groups
        m_id = match.group("id")
        content = match.group("content")

        # Security Check, if a teacher write a marker inside a marker : error 
        if "<complete" in content:
             # We use standard ValueError for simplicity
             raise ValueError(f"Error in marker '{m_id}': Nested <complete> tag found. Please check your closing tags.")
        
        # Store the marker and his content 
        markers_found.append(MarkerData(id=m_id, content=content))

        return f"{comment} TODO: {m_id}" 

    # re.sub runs the replacement_logic function for every match found
    template_content = re.sub(pattern, replacement_logic, full_content, flags=re.DOTALL)
    
    return ParsedResult(template=template_content, markers=markers_found)



if __name__ == "__main__":

    c_code = """
        #include <stdio.h>

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

    try: 
        result = extract_markers_from_code(c_code_with_error,"c")

        print("Template of the code wothout the markers\n", result.template)

        print("Content of the markers + id \n")
        for m in result.markers:
                    print(f"ID: {m.id}")
                    print(f"Content: {m.content}") 


    except ValueError as e:
        print(e)