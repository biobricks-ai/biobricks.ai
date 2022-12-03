from bbportal import login_manager as LM
from bbportal import login_routes as login
from bbportal.external_services.stripe import BBStripe

import datastore.datastore as ds

import werkzeug.middleware.proxy_fix as middleware
import flask, flask_login
import os, json

print('starting app')
ds.initdb()

app = flask.Flask(__name__, template_folder="templates")
app.secret_key = os.environ['BBPORTAL_FLASK_SECRET_KEY']
app.config['SERVER_NAME'] = os.environ['BBPORTAL_FLASK_SERVER_NAME']
app.wsgi_app = middleware.ProxyFix(app.wsgi_app)

LM.init(app)

# INDEX =======================================================================================================
@app.route('/', methods=['GET'])
def index():
  if flask_login.current_user.is_authenticated:
    return flask.render_template('index.html')
  else:
    return flask.redirect('login')
  

# Login and Registration =======================================================================================
app.route('/register', methods=['GET','POST'])(login.register)
app.route('/verification/<token>', methods=['GET','POST'])(login.validate_user_from_email)
app.route('/login', methods=['GET','POST'])(login.login)
app.route('/logout', methods=['GET'])(login.logout)

app.route('/forgot_password', methods=['GET','POST'])(login.forgot_password)
app.route('/reset_password/<token>', methods=['GET','POST'])(login.reset_password)

# STRIPE =======================================================================================================
@app.route('/customer_portal', methods=['GET'])
@flask_login.login_required
def customer_portal():
  customer_id = flask_login.current_user.stripe_customer_id
  session = BBStripe.create_customer_portal_session(customer_id,flask.url_for("index",_external=True))
  return flask.redirect(session.url)

@app.route('/create-checkout-session', methods=['POST'])
@flask_login.login_required
def create_checkout_session():
  customer_id = flask_login.current_user.stripe_customer_id
  success,cancel = (flask.url_for("index",_external=True),flask.url_for("index",_external=True))
  session = BBStripe.create_checkout_session(customer_id,success,cancel)
  return flask.redirect(session.url, code=303)

# TOKEN =======================================================================================================
@app.route('/token', methods=['GET'])
@flask_login.login_required
def token():
  token = flask_login.current_user.token
  return f"your token is below. please do not share it with anyone <br><b>{token}</b>"

@app.route('/token/is_valid', methods=['GET'])
def validate_token():
  token = flask.request.args.get('token')
  token_exists = ds.find('SELECT token from user WHERE token=(?)',(token,))
  return json.dumps(token_exists is not None)
