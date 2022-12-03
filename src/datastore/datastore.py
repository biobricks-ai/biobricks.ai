import sqlite3
import os
import pathlib
from dotenv import load_dotenv, find_dotenv

dbpath = os.environ.get("SQLITE_PATH")

def initdb():
  if os.path.exists(dbpath): 
    print(f"db already exists at {pathlib.Path(dbpath).absolute()}")
    return None
  
  pathlib.Path(dbpath).parent.mkdir(parents=True, exist_ok=True)

  for file in os.listdir("flyway"):
    with open(os.path.join("flyway", file), 'r') as sql_file:
      execute(sql_file.read())

  
def find(query,param = None):
  res = None
  try:
    con = sqlite3.connect(dbpath)
    con.row_factory = sqlite3.Row # enables dictlike returns
    cur = con.cursor()
    cur = cur.execute(query) if param is None else cur.execute(query,param)
    res = cur.fetchone()
  except Exception as e:
    print("error executing query") # TODO actually log this.
    print(query)
    print(e)
  finally:
    cur.close()
    con.close()    
    return res

def execute(query,param=None):
  try:
    con = sqlite3.connect(dbpath)
    if param is None: 
      con.execute(query)
    else:
      con.execute(query,param)
    con.commit()
  except Exception as e:
    print("error executing query") # TODO actually log this.
    print(query)
    print(e)
  finally:
    con.close()
    return "done"
