from bbportal import login_manager as LM
from bbportal import login_routes as login
from bbportal.external_services.stripe import BBStripe

import datastore.datastore as ds

import werkzeug.middleware.proxy_fix as middleware
import flask, flask_login
import os, json

from .model.repo import Repo, Object

print('starting app')
ds.initdb()

app = flask.Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ['BBPORTAL_FLASK_SECRET_KEY']
app.config['SERVER_NAME'] = os.environ['BBPORTAL_FLASK_SERVER_NAME']
app.config['LOGIN_VIEW'] = 'login'

app.wsgi_app = middleware.ProxyFix(app.wsgi_app)

LM.init(app)

# INDEX =======================================================================================================
@app.route('/', methods=['GET'])
def index():
  return flask.render_template('index.html')

@app.route('/search', methods=['GET'])  # Change here
def search():
    query = flask.request.args.get('query', '')  # Access query parameter
    find_all = flask.request.args.get('find_all', False) if query != '' else True
    
    tags = flask.request.args.get('tags', '').split(',')
    tags = [] if tags == [''] else tags
    
    start = int(flask.request.args.get('start', 1))
    current_page = (start -1)//10+1
    
    repodf, num_results = Repo.find_repos(query, find_all, start, tags)
    return flask.render_template('search.html', query=query, current_page=current_page, num_results=num_results, repos=repodf)

# BRICK =======================================================================================================
@app.route('/<org>/<reponame>', methods=['GET'])
def brick(org, reponame):
  repo = Repo.get_repo(org, reponame)
  objects = Object.get_repo_objects(repo) if repo else []
  return flask.render_template('brick.html', repo=repo, objects=objects)

# ACCOUNT MANAGEMENT ==========================================================================================
@app.route('/account', methods=['GET'])
@LM.login_required
def account():
  return flask.render_template('account.html')

# Login and Registration ======================================================================================
app.route('/register', methods=['GET','POST'])(login.register)
app.route('/verification/<token>', methods=['GET','POST'])(login.validate_user_from_email)
app.route('/login', methods=['GET','POST'])(login.login)
app.route('/logout', methods=['GET'])(login.logout)

app.route('/forgot_password', methods=['GET','POST'])(login.forgot_password)
app.route('/reset_password/<token>', methods=['GET','POST'])(login.reset_password)

# STRIPE ======================================================================================================
@app.route('/pricing', methods=['GET'])
@LM.login_required
def pricing():
  return flask.render_template('pricing.html')

@app.route('/billing', methods=['GET'])
@LM.login_required
def customer_portal():
  customer_id = flask_login.current_user.stripe_customer_id
  session = BBStripe.create_customer_portal_session(customer_id,flask.url_for("index",_external=True))
  return flask.redirect(session.url)

@app.route('/create-checkout-session', methods=['POST'])
@LM.login_required
def create_checkout_session():
  customer_id = flask_login.current_user.stripe_customer_id
  success,cancel = (flask.url_for("index",_external=True),flask.url_for("index",_external=True))
  session = BBStripe.create_checkout_session(customer_id,success,cancel)
  return flask.redirect(session.url, code=303)

# TOKEN =======================================================================================================
@app.route('/token', methods=['GET'])
@LM.login_required
def token():
  token = flask_login.current_user.token
  return f"your token is below. please do not share it with anyone <br><b>{token}</b>"

@app.route('/token/is_valid', methods=['GET'])
def validate_token():
  token = flask.request.args.get('token')
  token_exists = ds.find('SELECT token from user WHERE token=(?)',(token,))
  return json.dumps(token_exists is not None)