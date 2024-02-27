import requests
from datetime import datetime, timezone
import humanize  # Make sure to install this package using pip
from functools import lru_cache
from copy import deepcopy
import time

# Define a simple cache to store responses with an expiration time
class SimpleCache:
    def __init__(self, timeout):
        self.timeout = timeout
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = (value, time.time() + self.timeout)

    def get(self, key):
        value, expires = self.cache.get(key, (None, 0))
        if time.time() < expires:
            return value
        else:
            raise KeyError(f"Cache expired for key: {key}")

cache = SimpleCache(timeout=60*60)  # Cache timeout set to 30 seconds

headers = {
    "Authorization": f"token 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",
    "Accept": "application/vnd.github.v3+json",
}

def format_datetime(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return humanize.naturaltime(datetime.now(timezone.utc) - dt)

def _cached_repos():
    try:
        return cache.get("repos")
    except KeyError:
        pass
    
    repos = []
    url = f"https://api.github.com/orgs/biobricks-ai/repos"
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get('next', {}).get('url', None)
    
    cache.set("repos", repos)
    return repos
    
def find_repos():
    repos = _cached_repos()
    
    bricks = []
    for repo in repos:
        brick = deepcopy(repo)
        # Store raw update time for internal use and sorting
        brick['updated_rawtime'] = repo['updated_at']
        # Generate human-readable time on-the-fly for display purposes
        brick['updated_at'] = format_datetime(repo['updated_at'])
        bricks.append(brick)
    
    # sort by updated_rawtime
    bricks = sorted(bricks, key=lambda x: x['updated_rawtime'], reverse=True)
    return bricks

def find_repo(org, repo):
    repos = _cached_repos()
    for r in repos:
        if r['name'] == repo and r['owner']['login'] == org:
            return r
    return None