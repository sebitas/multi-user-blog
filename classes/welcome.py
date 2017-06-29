from classes.regular_expressions import *
from classes.handler import Handler

class Welcome(Handler):
  def get(self):
    username = self.request.get('username')
    if(valid_username(username)):
      self.render('welcome.html', username = username)
    else:
      self.redirect('/signup')