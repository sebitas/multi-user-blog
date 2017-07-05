from classes.handler import Handler
from classes.blog_entry import *
from classes.handler import BlogHandler


class Blog(Handler):

    def render_front(self, title="", art="", error=""):

        posts = BlogEntry.get_all_main_comments()

        t = []

        for i, s in enumerate(posts):
            s.content = s.content.replace('\n', '<br>')
            t.append(s)

        self.render("blog.html", posts=t)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")

    def likePost(post_id):
        if not self.user:
            self.redirect('/signin')

        result = BlogEntry.like_post(post_id, str(self.user.key().id()))

        if not result:
            self.render_front(error="You cant't like this post")
        else:
            self.render_front()


class DeletePost(BlogHandler):

    def render_front(self, error="", success=""):
        self.render("delete_post.html", error=error, success=success)

    def get(self):
        self.render_front()

    def deletePost(self, post_id, post_parent_id="default"):

        post = BlogEntry.by_id(post_id, post_parent_id)
        error = ""
        success = ""

        if not post:
            error = "User id %s not found" % (post_id)

        else:

            if str(post.user_post_id) == str(self.user.key().id()):
                post.delete()
                success = "Blog post with id %s was found and deleted!" % (
                    post_id)

            else:
                error = "You are not owner/creator of selected post"

        self.render_front(error=error, success=success)

    def post(self):
        if not self.user:
            self.redirect("/signin")

        else:
            post_id = self.request.get("post_id")
            post_parent_id = self.request.get("post_parent_id")

            if post_parent_id:
                result = self.deletePost(post_id, post_parent_id)
            else:
                result = self.deletePost(post_id)


class EditPost(BlogHandler):
    post_id = ""
    subject = ""
    content = ""
    post_parent_id = ""

    def render_front(self, error="", content="", subject="",
                     success="", post_id="", post_parent_id=""):
        self.render("edit_post.html", error=error, content=content,
                    subject=subject, success=success, post_id=post_id,
                    post_parent_id=post_parent_id)

    def get(self):
        self.render_front(post_id=self.post_id,
                          post_parent_id=self.post_parent_id)

    def editPost(self, post_id, subject, content,
                 post_parent_id="default"):
        post = BlogEntry.by_id(post_id, post_parent_id)

        params = dict(subject=subject, content=content)
        hasError = False
        if not post:
            hasError = True
            error = "User id %s not found" % (post_id)
        else:
            if str(post.user_post_id) == str(self.user.key().id()):
                post.subject = subject
                post.content = content
                post.put()
                params['success'] = "Blog post updated!"
            else:
                hasError = True
                params['error'] = "You are not owner/creator of selected post"

        if hasError:
            self.render_front(**params)
        else:
            self.render_front(error="Post Edition completed",
                              post_id=self.post_id)

    def post(self):
        if not self.user:
            self.redirect("/signin")

        else:
            self.post_id = self.request.get("post_id")
            self.post_parent_id = self.request.get("post_parent_id")
            self.subject = self.request.get("subject")
            self.content = self.request.get("content")

            if self.subject and self.content and self.post_id:
                if self.post_parent_id:
                    self.editPost(self.post_id, self.subject, self.content,
                                  self.post_parent_id)
                else:
                    self.editPost(self.post_id, self.subject, self.content)

            else:
                self.render_front(subject=self.subject,
                                  content=self.content,
                                  error="Please fill Content and Subject",
                                  post_id=self.post_id,
                                  post_parent_id=self.post_parent_id
                                  )


class LikePost(BlogHandler):

    def render_front(self, msg=""):
        self.render('likepost.html', msg=msg)

    def get(self):
        self.render_front()

    def post(self):
        if not self.user:
            self.redirect('/signin')

        post_id = self.request.get("post_id")
        post_parent_id = self.request.get("post_parent_id")

        if post_parent_id:
            result = BlogEntry.like_post(post_id, str(self.user.key().id()),
                                         post_parent_id)
        else:
            result = BlogEntry.like_post(post_id, str(self.user.key().id()))

        if not result:
            self.render_front(msg="You cant't like this post")
        else:
            self.render_front(msg="You liked the post")


class UnLikePost(BlogHandler):

    def render_front(self, msg=""):
        self.render('likepost.html', msg=msg)

    def get(self):
        self.render_front()

    def post(self):
        if not self.user:
            self.redirect('/signin')

        post_id = self.request.get("post_id")
        post_parent_id = self.request.get("post_parent_id")

        if post_parent_id:
            result = BlogEntry.unlike_post(post_id, str(self.user.key().id()),
                                           post_parent_id)
        else:
            result = BlogEntry.unlike_post(post_id, str(self.user.key().id()))

        if not result:
            self.render_front(msg="You cant't unlike this post")
        else:
            self.render_front(msg="You unliked the post")


class CommentPost(BlogHandler):
    subject = ""
    content = ""
    post_id = ""

    def get_son_posts(self, post_id):
        posts = BlogEntry.by_id_get_sons(post_id)
        result = []

        for i, s in enumerate(posts):
            s.content = s.content.replace('\n', '<br>')
            result.append(s)

        return result

    def get_parent_post(self, post_id):
        result = BlogEntry.by_id(post_id)

        if result:
            result.content = result.content.replace('\n', '<br>')

        return result

    def render_front(self, error="", posts="", post_id="",
                     subject="", content="", parent_post=""):

        self.render('commentpost.html', error=error,
                    posts=posts, post_id=post_id,
                    subject=subject, content=content,
                    parent_post=parent_post)

    def get(self):
        self.render_front(post_id=self.post_id)

    def commentpost(self, subject, content, parent_post):
        result = True
        id_str = '%d' % self.user.key().id()

        if self.subject and self.content:
            a = BlogEntry(subject=subject, content=content,
                          user_post_id=id_str, likes_count=0,
                          parent=main_comments_key(parent_post.key().id()))
            a.put()
        else:
            result = False

        return result

    def post(self):
        self.subject = self.request.get("subject")
        self.content = self.request.get("content")
        self.post_id = self.request.get("post_id")
        parent_post = self.get_parent_post(self.post_id)
        son_posts = self.get_son_posts(self.post_id)
        error = ""

        if not self.user:
            self.redirect('/signin')

        if not self.commentpost(self.content, self.subject, parent_post):
            error = "Please complete subject and content to comment"
        else:
            son_posts = self.get_son_posts(self.post_id)

        self.render_front(subject=self.subject,
                          content=self.content,
                          post_id=self.post_id,
                          posts=son_posts,
                          parent_post=parent_post,
                          error=error
                          )
