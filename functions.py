import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()


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









# Function to search for a director in Companies House
def search_director(director_name):
    base_url = 'https://api.company-information.service.gov.uk'
    search_url = f'{base_url}/search/officers?q={director_name}'
    headers = {
        'Authorization': f'Basic {COMPANIES_HOUSE_API_KEY}'
    }

    response = requests.get(search_url, headers=headers, auth=HTTPBasicAuth(COMPANIES_HOUSE_API_KEY, ''))

    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_director_details(officer_id):
    base_url = 'https://api.company-information.service.gov.uk'
    details_url = f'{base_url}/officers/{officer_id}/appointments'
    auth = HTTPBasicAuth(COMPANIES_HOUSE_API_KEY, '')

    response = requests.get(details_url, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_company_details(company_number):
    base_url = 'https://api.company-information.service.gov.uk'
    company_url = f'{base_url}/company/{company_number}'
    auth = HTTPBasicAuth(COMPANIES_HOUSE_API_KEY, '')

    response = requests.get(company_url, auth=auth)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
