import datastore.datastore as ds
from bbportal.stripe import BBStripe

import secrets
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

class User(flask_login.UserMixin):
  
  def __init__(self, uid, email, token, hashpw, stripe_customer_id):
    self.uid = uid
    self.email = email
    self.token = token
    self.hashpw = hashpw
    self.stripe_customer_id = stripe_customer_id

  def is_authenticated(self):
    return super().is_authenticated

  def get_id(self):
    return self.uid
  
  def is_anonymous(self):
    return super().is_anonymous
  
  def validate_password(self,password):
    print(f"""validating password {password} for {self.email} 
      it is {check_password_hash(self.hashpw,password)}""")

    return check_password_hash(self.hashpw,password)

  @staticmethod
  def user_exists(email):
    res = ds.find("SELECT email from user where email = (?)",(email,))
    return res is not None

  @staticmethod
  def make_token():
    return secrets.token_urlsafe(16)  

  @staticmethod
  def from_row(row):
    return User(row['uid'], row['email'], row['token'], row['hashpw'], row['stripe_customer_id'])

  @staticmethod
  def get(uid):
    res = ds.find("SELECT * from user where uid = (?)",(uid,))
    return User.from_row(res) if res is not None else None

  @staticmethod
  def get_user(email):
    res = ds.find("SELECT * from user where email = (?)",(email,))
    return User.from_row(res) if res is not None else None

  @staticmethod
  def create_stripe_customer(email):
    return BBStripe.create_customer(email)
  
  def create_datastore_customer(email, password, stripe_customer_id):
    hashpw = generate_password_hash(password)
    token = User.make_token()
    params = (email,hashpw,token,stripe_customer_id)
    ds.execute("INSERT INTO user (email,hashpw,token,stripe_customer_id) values (?,?,?,?)",params)
  
  @staticmethod
  def create_user(email, password):
    if User.user_exists(email): raise ValueError(f"{email} already exists")
    customer = User.create_stripe_customer(email)
    User.create_datastore_customer(email, password, customer.id)
    return User.get_user(email)

  @staticmethod
  def delete_user(email):
    if not User.user_exists: raise ValueError(f"{email} does not exist")
    user = User.get_user(email)
    BBStripe.delete_customer(user.stripe_customer_id)
    ds.execute("DELETE FROM user WHERE email = (?)",(email,))