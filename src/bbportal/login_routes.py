from datastore.user import User
from bbportal.forms.registration_form import RegistrationForm, ForgotPasswordForm, UpdatePasswordForm
from bbportal.external_services.sendgrid import BBSendgrid

import datastore.datastore as ds

import flask
import flask_login

import secrets
import datetime

login_page = flask.Blueprint('login', __name__, template_folder='templates')

# EMAIL VERIFICATION ====================================================================================
def generate_validation_link(user):
  link_token = secrets.token_urlsafe(16)
  expiration = datetime.datetime.now() + datetime.timedelta(days=1)
  params = (user.uid, link_token, expiration)
  ds.execute('INSERT INTO user_link (uid,link_token,expiration) values (?,?,?)',params)
  return link_token

def send_user_validate_email(user: User):
  link = generate_validation_link(user)
  route = flask.url_for("verification",token=link,_external=True)
  msg = f"Validate your account at <a href='{route}'><b>here</b></a>"
  BBSendgrid.send(user.email, "Validate your Biobricks.ai account", msg)

def validate_user_from_email(token):
  uid = ds.find('SELECT uid from user_link WHERE link_token=(?)',(token,))['uid']
  ds.execute('UPDATE user set email_verified = 1 WHERE uid = (?)',(uid,))
  if User.get(uid) is not None:
    flask_login.login_user(User.get(uid))
  return flask.redirect('/')

# USER PASSWORD RESET ===================================================================================
def send_password_reset(email):
  link = generate_validation_link(User.get_user(email))
  route = flask.url_for("reset_password",token=link,_external=True)
  msg = f"Reset your password at this <a href='{route}'>link</a>"
  BBSendgrid.send(email,"Biobricks.ai Password Reset",msg)

def forgot_password():
  form = ForgotPasswordForm()
  if flask.request.method == "GET": 
    return flask.render_template('forgot_password.html', form=form)
  
  email = flask.request.form['email']
  send_password_reset(email)
  return "check your email for a reset link"

def reset_password(token):
  form = UpdatePasswordForm()

  if flask.request.method == "GET": 
    return flask.render_template('reset_password.html', form=form, token=token)
  
  passw = flask.request.form['password']
  uid = ds.find('SELECT uid from user_link WHERE link_token=(?)',(token,))['uid']
  ds.execute('UPDATE user set password = (?) WHERE uid = (?)',(passw,uid,))
  
  if User.get(uid) is not None:
    flask_login.login_user(User.get(uid))

  return flask.redirect('/')

# USER Registration =====================================================================================
def register():
  form = RegistrationForm()
  
  if flask.request.method == "POST" and User.user_exists(form.email.data):
    flask.flash(f"{form.email.data} already exists, please log in")
    return flask.redirect('register')
  
  if flask.request.method == "POST" and not User.user_exists(form.email.data):
    user = User.create_user(form.email.data, form.password.data)
    send_user_validate_email(user)
    return "please check your email for a verification link"
    
  return flask.render_template('register.html', form=form)

# USER LOGIN/OUT ==================================================================================
def login():

  if flask.request.method == "GET" and flask_login.current_user.is_authenticated: 
    return flask.redirect(flask.url_for('index'))
  
  if not flask_login.current_user.is_authenticated:
    return flask.render_template('login.html')

  email = flask.request.form['email']
  passw = flask.request.form['password']
  user  = User.get_user(email)

  if not User.user_exists(email) or not user.validate_password(passw):
    flask.flash("incorrect email or password",category="error")
    return flask.redirect(flask.url_for('login'))

  flask_login.login_user(user)
  return flask.redirect(flask.url_for('index'))

def logout():
  flask_login.logout_user()
  return flask.redirect(flask.url_for('index'))