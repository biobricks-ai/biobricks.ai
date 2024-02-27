
class Repo():
    
    def __init__(self, repo_id, name, description, url, owner_id, objects):
        self.repo_id = repo_id
        self.name = name
        self.description = description
        self.url = url
        self.owner_id = owner_id    
        
    @staticmethod
    def from_org_repo(org, repo):
        return Repo(repo['id'], repo['name'], repo['description'], repo['html_url'], repo['owner']['id'], repo)