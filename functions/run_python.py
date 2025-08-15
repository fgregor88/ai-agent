import os
import subprocess
from pathlib import Path
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_abs = os.path.abspath(working_directory)
        
        if not full_path.startswith(working_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ['python', full_path] + args,
                cwd=working_directory,
                timeout=30,
                capture_output=True,
                text=True
            )
        except subprocess.TimeoutExpired:
            return 'Error: Process timed out after 30 seconds'

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return '\n'.join(output) if output else "No output produced."
    
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory. Returns the script's output, errors, or execution status. Ensures the file is within the permitted directory and has a .py extension.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file (e.g., 'scripts/example.py'). Must be inside the working directory and end with .py.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of command-line arguments to pass to the Python script (e.g., ['--verbose', 'input.txt']). Optional.",
                items=types.Schema(type=types.Type.STRING),  # Each argument must be a string
            ),
        },
        required=["file_path"],  # Only file_path is mandatory; args is optional
    ),
)