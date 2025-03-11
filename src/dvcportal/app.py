import flask
import os
import json


import datastore.datastore as ds
import datastore.user_event as user_event
from datastore.user import User
from datastore import s3_store

def create_app():
	app = flask.Flask(__name__, template_folder="templates")

	def authorized(token):
		if token == os.environ.get("BIOBRICKS_TEST_TOKEN"): return True
		return User.get_token_user(token) is not None
	  
	def log_request(request, path):
		user = User.get_token_user(request.headers.get('BBToken'))
		size = s3_store.resource_size(path)
		event = json.dumps({"path":path,"units":"bytes","size":size})
		user_event.create_user_event(user.uid, 'get_object', event)  

	@app.route('/<path:path>', methods=['GET', 'POST'])
	def all_routes(path):
		token = flask.request.headers.get('BBToken')
		if not authorized(token):
			return flask.Response('invalid token', 401)

		inspath = f"insdvc/{path}"
		if token != os.environ.get("BIOBRICKS_TEST_TOKEN"):
			log_request(flask.request, inspath)

		try:
			url = s3_store.generate_presigned_url('ins-dvc', inspath)
			return flask.redirect(url)
		except Exception as e:
			return flask.Response('Error generating presigned URL', 500)

	return app
