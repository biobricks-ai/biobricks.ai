import flask
import sqlite3
import boto
import json

import datastore.datastore as ds
import datastore.user_event as user_event

from datastore.user import User

app = flask.Flask(__name__, template_folder="templates")

def authorized(token):
  return User.get_token_user(token) is not None

def resource_size(path):
  s3 = boto.connect_s3()
  bk = s3.get_bucket('ins-dvc')
  lk = bk.lookup(f"insdvc/{path}")
  s3.close()
  return lk.size

def log_request(request, path):
  user = User.get_token_user(request.headers.get('BBToken'))
  size = resource_size(path)
  event = json.dumps({"path":path,"units":"bytes","size":size})
  user_event.create_user_event(user.uid, 'get_object', event)  

@app.route('/<path:path>', methods=['GET', 'POST'])
def all_routes(path):
  
  if not authorized(flask.request.headers.get('BBToken')):
    return flask.Response('invalid token', 401)

  log_request(flask.request, path)
  
  # TODO s3 should actually authenticate on token
  return flask.redirect(f'https://ins-dvc.s3.amazonaws.com/insdvc/{path}')
  
