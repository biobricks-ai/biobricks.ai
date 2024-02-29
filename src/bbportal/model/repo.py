import json
from datetime import datetime, timezone
import humanize
import sqlite3
import pandas as pd
import ast

class Object():
    
    def __init__(self, path, md5, size, nfiles=None):
        self.path = path
        self.md5 = md5
        self.size = size
        self.nfiles = nfiles
        self.human_size = humanize.naturalsize(size)
    
    @staticmethod
    def get_repo_objects(repo):
        objects = []
        with sqlite3.connect('biobricks.db') as con:
            con.row_factory = sqlite3.Row
            q = """SELECT object.path, object.md5, object.size osize, object.nfiles FROM repo 
            INNER JOIN object ON repo.repo_id = object.repo_id 
            WHERE repo.name = ? AND repo.owner = ? 
                AND (object.path LIKE 'brick%' OR object.path LIKE 'data%')
                AND object.size > 0
            ORDER BY repo.updated_at DESC"""
            rows = con.execute(q, (repo.name, repo.owner)).fetchall()
            for row in rows:
                if row['nfiles'] > 0:
                    obj = Object(row['path'], row['md5'], row['osize'], row['nfiles'])
                else:
                    obj = Object(row['path'], row['md5'], row['osize'])
                objects.append(obj)
        return objects
    
class Repo():
    
    def __init__(self, name, owner, updated_at, updated_last, html_url, size, metajson, tags=[]):
        self.name = name
        self.owner = owner
        self.updated_at = updated_at
        self.updated_last = updated_last
        self.html_url = html_url
        self.metajson = metajson
        self.size = size
        self.human_size = humanize.naturalsize(self.size)
        self.metajson_dict = ast.literal_eval(metajson)
        self.description = self.metajson_dict.get('description', '')
        self.tags = self.lookup_tags()
    
    def lookup_tags(self):
        with sqlite3.connect('biobricks.db') as con:
            q = "SELECT tag.tag FROM tag INNER JOIN repo ON tag.repo_id = repo.repo_id WHERE repo.name = ? AND repo.owner = ?"
            tags = [ x[0] for x in con.execute(q, (self.name, self.owner)).fetchall() if x[0] != '' ]
        return tags
    
    @staticmethod
    def _repos():
        with sqlite3.connect('biobricks.db') as con:
            q = "SELECT repo.* FROM repo INNER JOIN object ON repo.repo_id = object.repo_id ORDER BY repo.updated_at DESC"
            df = pd.read_sql_query(q, con)
        
        df['updated_at_dt'] = pd.to_datetime(df['updated_at']).dt.tz_convert('UTC')
        df['updated_last'] = df['updated_at_dt'].apply(lambda x: humanize.naturaltime(datetime.now(timezone.utc) - x))
        return df
        
    @staticmethod
    def find_repos(query, find_all=False, start=1, tags=[]):
        # TODO we should also match on objects and code
        tags = [tag.lower() for tag in tags] if tags is not None else []  # Convert input tags to lowercase
        where = f"WHERE LOWER(tag.tag) IN (?)" if tags else ""
        q = f"SELECT DISTINCT repo.* FROM repo INNER JOIN tag ON repo.repo_id = tag.repo_id {where} ORDER BY repo.updated_at DESC"
        
        with sqlite3.connect('biobricks.db') as con:
            reposdf = pd.read_sql_query(q, con, params=tags)
            reposdf['updated_at_dt'] = pd.to_datetime(reposdf['updated_at']).dt.tz_convert('UTC')
            reposdf['updated_last'] = reposdf['updated_at_dt'].apply(lambda x: humanize.naturaltime(datetime.now(timezone.utc) - x))
        
        def is_match(r):
            if find_all: return True
            return any(query.lower() in v.lower() for _, v in r.items() if isinstance(v, str))
        
        matches = reposdf.apply(lambda r: is_match(r), axis=1)    
        matchdf = reposdf[matches]
        matchdf = matchdf.iloc[start-1:start+9]
        
        # transform matches into [Repo]
        repos = []
        for i in range(matchdf.shape[0]):
            row = matchdf.iloc[i]
            repo = Repo(row['name'], row['owner'], row['updated_at'], row['updated_last'], row['html_url'], row['size'], row['metajson'])
            matchdf.at[i, 'repo'] = repo
            repos = repos + [repo]
        
        return repos, matchdf.shape[0]
    
    @staticmethod
    def From_Dict(d):
        updated_last = humanize.naturaltime(datetime.now(timezone.utc) - datetime.strptime(d['updated_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc))
        return Repo(d['name'], d['owner'], d['updated_at'], updated_last, d['html_url'], d['size'], d['metajson'])
    
    @staticmethod
    def get_repo(owner, repo_name):
        with sqlite3.connect('biobricks.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            q = "SELECT DISTINCT repo.* FROM repo INNER JOIN object ON repo.repo_id = object.repo_id WHERE repo.name = ? AND repo.owner = ? ORDER BY repo.updated_at DESC"
            row = cur.execute(q, (repo_name, owner)).fetchone()
            repo = Repo.From_Dict(row) if row else None
        return repo