from httplib2 import Http
import json
import os

from flask import render_template, current_app

from app.extensions.db import db
from app.blueprints.adaptive import blueprint
from app.blueprints.adaptive.models import Tweet, User

@blueprint.route('/')
def tweets():
    # fetch new updates when page is loaded
    if current_app.config.get('ADAPTIVE_API_DEBUG'):
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'testdata/tweets.json'))
        tweets = json.loads(open(path).read())
    else:
        # can't cache because response is different each request
        # but rate limit based on last insertion time
        api_url = current_app.config.get('ADAPTIVE_API_URL')
        h = Http()
        r, tweets_json = h.request(api_url, headers={'cache-control':'no-cache'})
        tweets = json.loads(tweets_json)

    keywords = current_app.config.get('ADAPTIVE_API_KEYWORDS')

    for new_tweet in tweets:
        # see if the user exists in our db
        user = User.query.filter_by(user_handle=new_tweet['user_handle']).first()
        if user is None:
            user = User(
                user_handle=new_tweet['user_handle'],
                followers=new_tweet['followers'],
            )
        # see if the tweet exists in our db
        tweet = Tweet.query.filter_by(tweet_id=new_tweet['id']).first()
        if tweet is None:
            # see if the message contains any of the keywords
            contains_keywords = False
            for keyword in keywords:
                if keyword in new_tweet['message']:
                    contains_keywords = True
                    break
            tweet = Tweet(
                created_at=new_tweet['created_at'],
                tweet_id=new_tweet['id'],
                message=new_tweet['message'],
                sentiment=new_tweet['sentiment'],
                updated_at=new_tweet['updated_at'],
                contains_keywords=contains_keywords,
            )
            tweet.user = user
            db.session.add(tweet)
            db.session.commit()

    return render_template('tweets.jinja')
