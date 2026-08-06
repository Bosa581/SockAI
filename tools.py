import os
import subprocess
from pathlib import Path
import requests

def resolve_path(file_path, workspace_root=None):
    root = Path(workspace_root).resolve() if workspace_root else Path.cwd().resolve()
    path_obj = Path(file_path)

    if path_obj.is_absolute():
        return path_obj if path_obj.exists() else None

    for base in [Path.cwd().resolve(), root]:
        candidate = (base / path_obj).resolve()
        if candidate.exists():
            return candidate

    for match in root.rglob(path_obj.name):
        if match.is_file() and match.name == path_obj.name:
            return match

    return None


def read_file(file_path, workspace_root=None):
    resolved_path = resolve_path(file_path, workspace_root=workspace_root)
    if resolved_path is None:
        return f"Error: the file '{file_path}' does not exist."

    with resolved_path.open("r", encoding="utf-8") as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:  # Open the file in write mode (this will create the file if it doesn't exist or overwrite it if it does)
        return file.write(content)
    
def list_files(folder_path):
    if not os.path.isdir(folder_path): # Check if the provided path is a directory
        return f"Error: the path '{folder_path}' is not a directory."  # Return an error message if it's not a directory
    return os.listdir(folder_path)

def run_code(code):
   result = subprocess.run(["python", "-c", code], capture_output=True, text=True)  # Run the code in a subprocess and capture the output
   if result.returncode == 0:  # Check if the code executed successfully
       return f"Code executed successfully.\nOutput: {result.stdout}"
   else: 
       return f"Error executing code.\nError: {result.stderr}"
   
def fetch_github(url):
    response = requests.get(url)
    if response.status_code == 200:  # Check if the request was successful
        return response.text  # Return the content of the response
    else:
        return f"Error fetching data from Github '{url}'. Status code {response.status_code}."  # Return an error message if the request was not successful