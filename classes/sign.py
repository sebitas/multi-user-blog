
from classes.handler import Handler
from classes.regular_expressions import *
from google.appengine.ext import db

secret = "secret"

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
  username = db.StringProperty(required = True)
  pw_hash = db.StringProperty(required = True)
  email = db.StringProperty(required = False)

  @classmethod
  def by_id(cls, uid):
    return User.get_by_id(uid, parent = users_key())

  @classmethod
  def register(cls, name, pw, email = None):
    pw_hash = make_secure_hash(name, pw)
    return User(parent = users_key(),
                name = name,
                pw_hash = pw_hash,
                email = email)


class SignUp(Handler):
    def render_sign_up(self, username = "", email = "", username_error = "", 
                       email_error = "", password_error = "", verify_error=""):
        self.render("signup.html", username = username , email = email, 
                    username_error = username_error, email_error = email_error, 
                    password_error = password_error, verify_error = verify_error)

    def get(self):
        self.render_sign_up()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username = username, email = email)
        hasError = False

        if not username and valid_username(username):
            hasError = True
            params['username_error'] ="Not valid username"

        if not password or not valid_password(password):
            hasError = True
            params['password_error'] ="Not valid password"
        elif not verify or not valid_password(verify):
            hasError = True
            params['verify_error'] ="Not valid password"

        if password != verify:
            hasError = True
            params['password_error'] ="Passwords don't match"

        if email and not valid_email(email):
            hasError = True
            params['email_error'] ="Not valid email"

        if hasError:
            self.render_sign_up(**params)
        else:
            str = ("/welcome?username=%s") % username
            self.redirect(str)

