import os
import subprocess

import requests 
def read_file(file_path):
    if not os.path.exists(file_path):   # Check if the file exists
       return f"Error: the file '{file_path}' does not exist."
    with open(file_path, 'r') as file:  # Open the file in read mode
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