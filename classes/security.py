import hashlib
import hmac
import random
from string import letters

secret = "secret"

# hashing for cookie

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#hashing for password

def make_salt(lenght = 5):
    return ''.join(random.choice(letters) for x in xrange(lenght))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name+pw+salt).hexdigest()
    return '%s,%s' % (salt,h)

def valid_pw_hash(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

