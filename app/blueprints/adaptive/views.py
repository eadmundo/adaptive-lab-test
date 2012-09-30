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

    print tweets

    return render_template('tweets.jinja')
