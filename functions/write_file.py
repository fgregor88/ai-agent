# functions/write_file.py
import os

def write_file(working_directory, file_path, content):
    try:
        # Create the full path and get absolute paths for comparison
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_abs = os.path.abspath(working_directory)
        
        # Check if the requested file is within the working directory
        if not full_path.startswith(working_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write the file content
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {str(e)}'