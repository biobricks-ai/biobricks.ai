import tqdm
import pandas as pd
import base64
import requests
import os
import yaml
import dotenv
import sqlite3
import pathlib

dotenv.load_dotenv()        
ghtok = os.environ.get('GITHUB_TOKEN')
bbtok = os.environ.get('BIOBRICKS_TEST_TOKEN')

# BUILD SQLITE DB ===========================================================================================
if pathlib.Path('biobricks.db').exists(): os.remove('biobricks.db')

# BUILD REPOS TABLE ========================================================================================= 
with sqlite3.connect('biobricks.db') as conn:
    conn.execute('''CREATE TABLE repo
                (repo_id INTEGER PRIMARY KEY, name TEXT, owner TEXT, updated_at TEXT, html_url TEXT, metajson TEXT, size INTEGER)''')
    conn.execute('''CREATE INDEX idx_repos_name_owner ON repo (name, owner)''')

# POPULATE REPOS TABLE ======================================================================================
def store_repo(repo):
    with sqlite3.connect('biobricks.db') as conn:
        conn.execute("INSERT INTO repo (name, owner, updated_at, html_url, metajson) VALUES (?, ?, ?, ?, ?)", 
                (repo['name'], repo['owner']['login'], repo['updated_at'], repo['html_url'], str(repo)))

url = f"https://api.github.com/orgs/biobricks-ai/repos"  
while url:
    response = requests.get(url, headers={"Authorization":f"token {ghtok}", "Accept":"application/vnd.github.v3+json"})
    response.raise_for_status()
    url = response.links.get('next', {}).get('url', None)
    for repo in response.json():
        print(repo['name'])
        store_repo(repo)
    
# BUILD OUTS TABLE =======================================================================================
with sqlite3.connect('biobricks.db') as conn:
    conn.execute("DROP TABLE IF EXISTS object")
    conn.execute('''CREATE TABLE object
                (object_id INTEGER PRIMARY KEY, repo_id INTEGER, path TEXT, md5 TEXT, size INTEGER, nfiles INTEGER, extension TEXT,
                FOREIGN KEY (repo_id) REFERENCES repos(repo_id))''')
    conn.execute('''CREATE INDEX idx_object_repo_id ON object (repo_id)''')
    conn.execute('''CREATE UNIQUE INDEX idx_object_repo_id_path ON object (repo_id, path)''')

# POPULATE OBJECTS TABLE ====================================================================================
def get_dvc_lock(owner,name):
    api_url = f"https://api.github.com/repos/{owner}/{name}/contents/dvc.lock"
    hdr = {"Authorization":f"token {ghtok}", "Accept":"application/vnd.github.v3+json"}
    response = requests.get(api_url, headers=hdr)
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
        response.raise_for_status()

def _get_out_size(md5):
    url = f"https://dvc.biobricks.ai/files/md5/{md5[:2]}/{md5[2:]}"
    return int(requests.head(url, headers={'BBToken': bbtok}).headers['Content-Length'])

def _download_outdir(md5):    
    url = f"https://dvc.biobricks.ai/files/md5/{md5[:2]}/{md5[2:]}"
    return requests.get(url, headers={'BBToken': bbtok}).json()

def store_out(repo_id, out):
    # TODO load out size
    extension = out['path'].split('.')[-1] if '.' in out['path'] else ''
    with sqlite3.connect('biobricks.db') as conn:
        conn.execute("INSERT INTO object (repo_id, path, extension, md5, size, nfiles) VALUES (?, ?, ?, ?, ?, ?)", 
                (repo_id, out['path'], extension, out.get('md5', ''), out.get('size', 0), out.get('nfiles', 0)))
    
    if out.get('nfiles', 0) > 0:
        try:
            subouts = _download_outdir(out['md5'])
            for subout in subouts:
                subout['path'] = out['path'] + subout['relpath'] if out['path'][-1] == '/' else out['path'] + '/' + subout['relpath']
                # subout['size'] = _get_out_size(subout['md5'])
                store_out(repo_id, subout)
        except Exception:
            pass
    
with sqlite3.connect('biobricks.db') as conn:
    repos = conn.execute("SELECT repo_id, name, owner FROM repo").fetchall()
    
for i in tqdm.tqdm(range(len(repos))):
    (repo_id, name, owner) = repos[i]
    dvc_lock = get_dvc_lock(owner,name)
    if dvc_lock is None: continue
    stages = [ stage_data for _, stage_data in dvc_lock.get('stages', {}).items()]
    # deps = [ dep for stage in stages for dep in stage.get('deps', []) ]
    outs = [ out for stage in stages for out in stage.get('outs', []) ]
    for out in outs:
        try:
            store_out(repo_id, out)
        except Exception:
            continue

# UPDATE REPO SIZES ====================================================================================
with sqlite3.connect('biobricks.db') as conn:
    repos = conn.execute("SELECT repo_id, name, owner FROM repo").fetchall()
    
for i in tqdm.tqdm(range(len(repos))):
    (repo_id, name, owner) = repos[i]
    with sqlite3.connect('biobricks.db') as conn:
        size = conn.execute("SELECT SUM(size) FROM object WHERE repo_id=(?)", (repo_id,)).fetchone()[0]
        conn.execute("UPDATE repo SET size=(?) WHERE repo_id=(?)", (size, repo_id))
        
# CREATE TAGS TABLE ====================================================================================
with sqlite3.connect('biobricks.db') as conn:
    conn.execute("DROP TABLE IF EXISTS tag")
    conn.execute('''CREATE TABLE tag
                (tag_id INTEGER PRIMARY KEY, repo_id INTEGER, tag TEXT, FOREIGN KEY (repo_id) REFERENCES repos(repo_id))''')
    conn.execute('''CREATE INDEX idx_tag_repo_id ON tag (repo_id)''')
    conn.execute('''CREATE UNIQUE INDEX idx_tag_repo_id_tag ON tag (repo_id, tag)''')

with sqlite3.connect('biobricks.db') as conn:
    repos = conn.execute("SELECT repo_id, name, owner FROM repo").fetchall()
    
for i in tqdm.tqdm(range(len(repos))):
    (repo_id, name, owner) = repos[i]
    with sqlite3.connect('biobricks.db') as conn:
        q = "SELECT DISTINCT extension FROM object WHERE repo_id = ? AND (path LIKE 'brick/%' OR path LIKE 'data/%')"
        tags = conn.execute(q, (repo_id,)).fetchall()
        for tag in tags:
            conn.execute("INSERT INTO tag (repo_id, tag) VALUES (?, ?)", (repo_id, tag[0]))

df = pd.read_sql("SELECT * FROM object", sqlite3.connect('biobricks.db'))
df[df['extension']=='brick']
df = pd.read_sql("SELECT * FROM tag", sqlite3.connect('biobricks.db'))