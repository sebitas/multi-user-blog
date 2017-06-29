from classes.handler import Handler
from google.appengine.ext import db

class BlogEntry(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
  def render_front(self, title = "", art = "", error = ""):

    posts = db.GqlQuery("SELECT * FROM BlogEntry order by created desc")

    t = [];

    for i,s in enumerate(posts):
      s.content = s.content.replace('\n','<br>')
      t.append(s)

    self.render("blog.html", posts = t)

  def get(self):
    self.render_front()

  def post(self):
    title = self.request.get("title") 