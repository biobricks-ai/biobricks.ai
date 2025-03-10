import sqlite3
import os
import pathlib

dbpath = os.environ.get("SQLITE_PATH")

def initdb():
  if os.path.exists(dbpath): 
    print(f"db already exists at {pathlib.Path(dbpath).absolute()}")
    return None
  
  pathlib.Path(dbpath).parent.mkdir(parents=True, exist_ok=True)

  # list files in flyway directory alphabetically
  migrations = sorted(os.listdir("flyway"))
  for migration in migrations:
    with open(f"flyway/{migration}") as f:
      execute(f.read())

  
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
