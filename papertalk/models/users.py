from flask import g
from flask_login import AnonymousUserMixin
from bson import ObjectId

class User(dict):

    def __repr__(self):
        return 'User(%r)' % (self['username'])

    def get_id(self):
        return str(self['_id'])

    def is_active(self):
        return bool(not self.get('_inactive', False))

    def is_anonymous(self):
        if self['_id']:
            return False
        return True

    def is_authenticated(self):
        if self['_id']:
            return True
        return False

class MyAnonymousUser(AnonymousUserMixin, dict):
    def __init__(self):
        self['_id'] = None
        self['username'] = None


def update(user, *E, **doc):
    """
    Updates a user
    """
    doc.update(*E)

    return g.db.users.update({"_id" : user['_id']},
                             {"$set": doc},
                            safe=True)

def save(**doc):
    """
    Called to save a user.
    """
    _id = g.db.users.insert(doc, safe=True)
    return _id


def get(_id=None, username=None):
    """
    Gets a user by id
    """
    q = {}

    if _id:
        q["_id"] = ObjectId(_id)
    elif username:
        q["username"] = username
    else:
        return None

    user = g.db.users.find_one(q, as_class=User, safe=True)
    return user

def create(username, email, token, **doc):
    """
    Creates a new user
    """
    doc.update({'username': username,
                '_username': username.lower(),
                'email': email,
                'token': token,
                'is_active':True
               })

    _id = g.db.users.insert(doc, safe=True)
    doc.update({'_id': _id})
    user = User(doc)

    return user

