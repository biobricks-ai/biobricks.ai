from datastore.user import User
import flask_login

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
