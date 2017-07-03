from classes.regular_expressions import *
from classes.handler import BlogHandler

class Welcome(BlogHandler):
  def get(self):
    username = self.request.get('username')
    if self.user:
      self.render('welcome.html', username = self.user.username)
    else:
      self.redirect('/signup')