import datastore.datastore as ds
from datastore.user import User

def get_token_user(token):
  print(f"token is {token}")
  row = ds.find('SELECT * FROM user WHERE token = (?)',(token,))
  return User.from_row(row)