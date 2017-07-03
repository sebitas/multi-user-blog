from google.appengine.ext import db
from classes.security import *

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
    def get_by_name(cls, name):
        u = User.all().filter('username = ', name).get()
        return u;

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                username = name,
                pw_hash = pw_hash,
                email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.get_by_name(name)
        if u and valid_pw_hash(name, pw, u.pw_hash):
            return u
