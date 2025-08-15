# functions/get_file_content.py
import os
from functions.config import MAX_FILE_SIZE
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # Create the full path and get absolute paths for comparison
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_abs = os.path.abspath(working_directory)
        
        # Check if the requested file is within the working directory
        if not full_path.startswith(working_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a file
        if not os.path.exists(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file content
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Truncate if necessary
        if len(content) > MAX_FILE_SIZE:
            content = content[:MAX_FILE_SIZE] + f'\n[...File "{file_path}" truncated at {MAX_FILE_SIZE} characters]'
        
        return content
    
    except Exception as e:
        return f'Error: {str(e)}'

schema_get_file_content=types.FunctionDeclaration(
    name="get_file_content",
    description="Gets file content. The content is truncated to MAX_FILE_SIZE which is defined in functions/config.py file. Ensures that the file is inside the working directory for security.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the string. Must be insdie the working directory."
            )
        },
        required=["file_path"]
    )
)