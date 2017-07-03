from google.appengine.ext import db

class BlogEntry(db.Model):
  user_post_id = db.StringProperty(required = True)
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  likes_count = db.IntegerProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)
  likes_list_of_user_ids = db.StringListProperty()

  @classmethod
  def by_id(cls, uid):
      return BlogEntry.get_by_id(long(uid))

  @classmethod
  def like_post(cls, post_id, uid):
    post = cls.by_id(post_id)
    result = True

    if post and uid != post.user_post_id:
      if not uid in post.likes_list_of_user_ids:
        post.likes_list_of_user_ids.append(uid)
        post.likes_count = int(post.likes_count) + 1
        post.put()
      else:
        result = False
    else:
      result = False

    return result

  @classmethod
  def unlike_post(cls, post_id, uid):
    post = cls.by_id(post_id)
    result = True

    if post and uid != post.user_post_id:
      if uid in post.likes_list_of_user_ids:
        post.likes_list_of_user_ids.remove(uid)
        post.likes_count = int(post.likes_count) - 1
        post.put()
      else:
        result = False
    else:
      result = False

    return result
