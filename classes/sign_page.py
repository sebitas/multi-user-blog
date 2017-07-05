from classes.handler import BlogHandler
from classes.regular_expressions import *
from classes.user_entry import User


class SignUp(BlogHandler):

    def render_sign_up(self, username="", email="", username_error="",
                       email_error="", password_error="", verify_error=""):
        self.render("signup.html", username=username, email=email,
                    username_error=username_error, email_error=email_error,
                    password_error=password_error, verify_error=verify_error)

    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.username)
        else:
            self.render_sign_up()

    def post(self):
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email")

        params = dict(username=self.username, email=self.email)
        hasError = False

        if not self.username and valid_username(self.username):
            hasError = True
            params['username_error'] = "Not valid username"

        if not self.password or not valid_password(self.password):
            hasError = True
            params['password_error'] = "Not valid password"
        elif not self.verify or not valid_password(self.verify):
            hasError = True
            params['verify_error'] = "Not valid password"

        if self.password != self.verify:
            hasError = True
            params['password_error'] = "Passwords don't match"

        if self.email and not valid_email(self.email):
            hasError = True
            params['email_error'] = "Not valid email"

        if hasError:
            self.render_sign_up(**params)
        else:
            u = User.get_by_name(self.username)
            if u:
                msg = 'That user already exists'
                self.render_sign_up(username_error=msg)
            else:
                u = User.register(self.username, self.password, self.email)
                u.put()

                self.login(u)
                self.redirect('/welcome')


class SignIn(BlogHandler):

    def renderSignIn(self, username="", username_password_error=""):
        self.render("signin.html", username=username,
                    username_password_error=username_password_error)

    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.username)
        else:
            self.renderSignIn()

    def post(self):
        self.username = self.request.get("username")
        self.password = self.request.get("password")

        params = dict(username=self.username)
        err = "invalid username or password"
        u = User.login(self.username, self.password)

        if not self.username or not self.password or not u:
            params['username_password_error'] = u
            self.renderSignIn(**params)
        else:
            self.login(u)
            self.redirect('/welcome')


class SignOut(BlogHandler):

    def get(self):
        self.logout()
        self.redirect('/signup')
