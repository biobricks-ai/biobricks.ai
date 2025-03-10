from datastore.user import User
from bbportal.forms.registration_form import RegistrationForm, ForgotPasswordForm, UpdatePasswordForm
from bbportal.external_services.sendgrid import BBSendgrid
from werkzeug.security import generate_password_hash, check_password_hash

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
  route = flask.url_for("validate_user_from_email",token=link,_external=True)
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
    user = User.get_user(email)
    if not user:
        return False
    
    link = generate_validation_link(user)
    route = flask.url_for("reset_password", token=link, _external=True)
    msg = f"Reset your password at <b><a href='{route}'>biobricks.ai forgot password</a></b>"
    BBSendgrid.send(email, "Biobricks.ai Password Reset", msg)
    return True

def forgot_password():
    form = ForgotPasswordForm()
    
    if flask.request.method == "GET": 
        return flask.render_template('forgot_password.html', form=form)
    
    if form.validate_on_submit():
        email = form.email.data
        user = User.get_user(email)
        
        if user:
            send_password_reset(email)
            return "Check your email for a reset link"
        else:
            flask.flash("Email not found", "error")
            return flask.redirect(flask.url_for('forgot_password'))
    
    # If form validation failed
    return flask.render_template('forgot_password.html', form=form)

def reset_password(token):
  form = UpdatePasswordForm()

  if flask.request.method == "GET": 
    return flask.render_template('reset_password.html', form=form, token=token)
  
  if form.validate_on_submit():
    uid = ds.find('SELECT uid from user_link WHERE link_token=(?)',(token,))['uid']
    user = User.get(uid)
    if user:
      hashpw = generate_password_hash(form.password.data)
      ds.execute('UPDATE user set hashpw = (?) WHERE uid = (?)', (hashpw, uid))
      flask_login.login_user(user)
      return flask.redirect('/')
  
  # If validation fails, return to form
  return flask.render_template('reset_password.html', form=form, token=token)

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
    if flask.request.method == "GET":
        if flask_login.current_user.is_authenticated:
            return flask.redirect(flask.url_for('index'))
        return flask.render_template('login.html')

    if flask.request.method == "POST":
        email = flask.request.form['email']
        passw = flask.request.form['password']
        user = User.get_user(email)

        if not User.user_exists(email) or not user.validate_password(passw):
            flask.flash("incorrect email or password", category="error")
            return flask.redirect(flask.url_for('login'))

        flask_login.login_user(user)

        # Check if there is a 'next' URL in the session and redirect to it
        next_page = flask.session.pop('next', None)
        if next_page:
            return flask.redirect(next_page)

        return flask.redirect(flask.url_for('index'))

def logout():
  flask_login.logout_user()
  return flask.redirect(flask.url_for('index'))