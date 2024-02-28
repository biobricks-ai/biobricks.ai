import base64
import requests
import os
import yaml
class Objects():
    
    def __init__(self, path, md5, size, nfiles):
        self.path = path
        self.md5 = md5
        self.size = size
        self.nfiles = nfiles

    @staticmethod
    def _get_dvc_lock(owner, repo):
        GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/dvc.lock"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            file_contents_base64 = json_response['content']
            file_contents_bytes = base64.b64decode(file_contents_base64)
            file_contents = file_contents_bytes.decode('utf-8')
            parsed_yaml = yaml.safe_load(file_contents)
            return parsed_yaml
        elif response.status_code == 404:
            return None
        else:
            return f"Error fetching file: {response.status_code} - {response.reason}"
    
    def from_github(owner, repo):
        dvc_lock = Objects._get_dvc_lock(owner, repo)
        if dvc_lock is None:
            return None  # Handle the case where the dvc.lock file could not be fetched

        objects = []
        stages = [ stage_data for _, stage_data in dvc_lock.get('stages', {}).items()]
        for stage in stages:
            outs = [out for out in stage.get('outs', []) if out['path'].startswith('brick/')]
            for out in outs:
                obj = Objects(path=out['path'], md5=out.get('md5', ''), size=out.get('size', 0), nfiles=out.get('nfiles', 0))
                objects.append(obj)
        return objects
        
    

Objects.from_github("biobricks-ai", "ice")