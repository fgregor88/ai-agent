import os
import subprocess
from pathlib import Path

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