from functions import fetch_github_repo_contents
from functionsGPT import comprehend_data

# Example usage
owner = 'BiggestChris'
repo = 'Tax-Intro-V1'
files = fetch_github_repo_contents(owner, repo)

prompt = ''

for file in files:
    prompt += (f"Path: {file['path']}\nContent: {file['content'][:5000]}...\n")

output = comprehend_data(prompt)

print(output)