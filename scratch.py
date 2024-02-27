import requests
import subprocess
import os

# Configuration
GITHUB_ORG = "biobricks-ai"
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
CLONE_DIR = "biobricks_repos"  # Directory where you want to clone the repositories

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_repos(org):
    """Fetch all repositories for a given organization"""
    repos = []
    url = f"https://api.github.com/orgs/{org}/repos"
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get('next', {}).get('url', None)
    return repos

def clone_repo(repo_url):
    """Clone a single repository"""
    subprocess.run(["git", "clone", repo_url], check=True)

def main():
    # Ensure the clone directory exists
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)
    os.chdir(CLONE_DIR)

    # Fetch all repositories
    repos = get_repos(GITHUB_ORG)

    # Clone each repository
    for repo in repos:
        print(f"Cloning {repo['full_name']}...")
        clone_repo(repo['clone_url'])

repos = []
url = f"https://api.github.com/orgs/{org}/repos"
while url:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repos.extend(response.json())
    url = response.links.get('next', {}).get('url', None)


r2 = []
url = f"https://api.github.com/search/repositories?q=org:biobricks-ai"
while url:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    r2.extend(response.json())
    url = response.links.get('next', {}).get('url', None)
