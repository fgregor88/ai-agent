# functions/get_files_info.py
import os

def get_files_info(working_directory, directory="."):
    try:
        # Create the full path and get absolute paths for comparison
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_abs = os.path.abspath(working_directory)
        
        # Check if the requested directory is within the working directory
        if not full_path.startswith(working_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a directory
        if not os.path.exists(full_path):
            return f'Error: "{directory}" does not exist'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        # Get directory contents and build the result string
        contents = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            try:
                size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                contents.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')
            except OSError as e:
                contents.append(f'- {item}: Error accessing file info')
        
        # Sort directories first, then files, both alphabetically
        contents.sort(key=lambda x: (not x.endswith('is_dir=True)'), x.lower()))
        
        return '\n'.join(contents)
    
    except Exception as e:
        return f'Error: {str(e)}'
