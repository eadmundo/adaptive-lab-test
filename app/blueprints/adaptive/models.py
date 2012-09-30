import datetime

from app.extensions.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # don't know how long username can be
    user_handle = db.Column(db.String(255))
    followers = db.Column(db.Integer)

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    # when this tweet was inserted into db
    inserted = db.Column(db.DateTime(), default=datetime.datetime.now)
    # stores id provided for tweet by API
    tweet_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    # don't know max length for message, but twitter-like
    # so just using string
    message = db.Column(db.String(255))
    sentiment = db.Column(db.Float)
    contains_keywords = db.Column(db.Boolean)

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

