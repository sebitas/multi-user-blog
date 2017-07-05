from classes.handler import BlogHandler
from classes.blog_entry import BlogEntry
from classes.blog_entry import main_comments_key


class NewPost(BlogHandler):

    def render_submit_post(self, subject="", content="", error=""):
        if self.user:
            self.render("submit_new_post.html", subject=subject,
                    content=content, error=error)
        else:
            self.redirect('/signup')

    def post(self):
        if self.user:
            subject = self.request.get("subject")
            content = self.request.get("content")
            id_str = '%d' % self.user.key().id()

            if subject and content:
                a = BlogEntry(subject=subject, content=content,
                              user_post_id=id_str, likes_count=0,
                              parent=main_comments_key())
                a.put()
                str = "/blog/%d" % a.key().id()
                self.redirect(str)
            else:
                error = "Both title and content must be filled"
                self.render_submit_post(error=error)
        else:
            self.redirect('/signup')

    def get(self):
        if self.user:
            self.render_submit_post()
        else:
            self.redirect('signin')


class PostHandler(BlogHandler):

    def get(self, id):
        post = BlogEntry.by_id(long(id))
        if not post:
            self.redirect("/blog")
        else:
            post.content = post.content.replace('\n', '<br>')
            self.render("blog.html", posts = [post])
