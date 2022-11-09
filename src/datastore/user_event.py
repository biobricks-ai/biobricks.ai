import datastore.datastore as ds

def create_user_event(uid:int, event:str, jsval:str):
  P = (uid,event,jsval)
  return ds.execute('INSERT INTO user_event (uid,event,jsval) VALUES (?,?,?)',P)