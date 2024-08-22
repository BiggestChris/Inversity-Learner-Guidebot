import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

# https://github.com/BiggestChris/Companies-House-Unlock

def extract_github_details(link):
    try:
        if link.find("github.com/") == -1:
            raise ValueError
        else:
            start = link.find("github.com/") + 11
            owner = link[start:link.find("/", start)]
            if link.find("/", start + len(owner) + 1) != -1:
                raise ValueError
            else:
                if link.find(".", start + len(owner) + 1) == -1:
                    repo = link[(start + len(owner) + 1):]
                else:
                    repo = link[(start + len(owner) + 1):link.find(".", start + len(owner) + 1)]
            print('Owner: ', owner)
            print('Repo: ', repo)
            return (owner, repo)
    except:
        raise ValueError

# TODO: Add error handling to GitHub API Call
def fetch_github_repo_contents(owner, repo, path=""):
    # GitHub API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    # Send a GET request to the GitHub API
    response = requests.get(url)
    
    if response.status_code == 200:
        contents = response.json()
        files = []
        
        for item in contents:
            if item['type'] == 'file':
                # Get the content of each file
                file_content = requests.get(item['download_url']).text
                files.append({'path': item['path'], 'content': file_content})
        
        return files
    
    else:
        raise Exception(f"Failed to fetch repository contents: {response.status_code}")
    
# TODO: Add error handling to below in case file path doesn't exist etc.
# Function to read the text file and feed it into ChatGPT
def read_text_file(file_path):
    try:
        # Read the content of the text file
        with open(file_path, 'r') as file:
            file_content = file.read()

        return file_content
    
    except:
        raise ValueError