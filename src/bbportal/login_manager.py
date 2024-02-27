from functools import wraps
from flask import redirect, url_for
from datastore.user import User
import flask_login
import flask

login_manager = flask_login.LoginManager()

@login_manager.user_loader
def load_user(user_id): 
  return User.get(user_id)

@login_manager.request_loader
def request_loader(request):
  email = request.form.get('email')
  return User.get_user(email) if User.user_exists(email) else None

def init(app):
  login_manager.init_app(app)
  login_manager.login_view = "/"
  return login_manager

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not flask_login.current_user.is_authenticated:
            return flask.redirect('login')
        return f(*args, **kwargs)
    return decorated_function