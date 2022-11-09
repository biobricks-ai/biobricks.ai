import flask
import sqlite3
import boto
import json

import datastore.datastore as ds
import datastore.user_link as user_link
import datastore.user_event as user_event

app = flask.Flask(__name__, template_folder="templates")

def resource_size(path):
  s3 = boto.connect_s3()
  bk = s3.get_bucket('ins-dvc')
  lk = bk.lookup(f"insdvc/{path}")
  s3.close()
  return lk.size

def log_request(request, path):
  user = user_link.get_token_user(request.headers.get('BBToken'))
  size = resource_size(path)
  event = json.dumps({"path":path,"units":"bytes","size":size})
  user_event.create_user_event(user.uid, 'get_object', event)  

@app.route('/<path:path>', methods=['GET', 'POST'])
def all_routes(path):
  log_request(flask.request, path)
  return flask.redirect(f'https://ins-dvc.s3.amazonaws.com/insdvc/{path}')
  
