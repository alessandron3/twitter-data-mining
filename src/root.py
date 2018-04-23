# -*- coding: utf-8 -*-
import oauth2 as oauth
import twitter
import urllib
import json

import config

from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
    url_for,
    request,
)

try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl


app = Blueprint('root', __name__)

oauth_consumer = oauth.Consumer(
    key = config.object.TWITTER_OAUTH_CONSUMER_KEY,
    secret = config.object.TWITTER_OAUTH_CONSUMER_SECRET,
)

oauth_client = oauth.Client(oauth_consumer)

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('root.login'))
 
    access_token = access_token[0]
 
    return render_template('index.html')

@app.route('/login', methods = [ 'GET', 'POST' ])
def login():
    res, content = oauth_client.request('https://api.twitter.com/oauth/request_token?%s' % urllib.urlencode({
                                        'oauth_callback': 'http://localhost:5000' + url_for('root.oauth_authorized')
                                        }).replace('+', '%20'),
                    'GET',)
    if res['status'] != '200':
        raise Exception(
            "Invalid response %s: %s" % (res['status'], content)
        )

    request_token = dict(parse_qsl(content))
    session['request_token'] = request_token

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(request_token)
    url = 'https://api.twitter.com/oauth/authorize?%s' % (
        urllib.urlencode({
             'oauth_token': request_token['oauth_token'],
             'oauth_callback': 'http://localhost:5000' + url_for('root.oauth_authorized')
        }).replace('+', '%20'),
    )
    return redirect(url)

@app.route('/oauth_authorized')
def oauth_authorized():
    request_token = session['request_token']
    token = oauth.Token(
        request_token['oauth_token'],
        request_token['oauth_token_secret']
    )
    oauth_verifier = request.args.get('oauth_verifier')

    client = oauth.Client(oauth_consumer, token)
    res, content = client.request(
        'https://api.twitter.com/oauth/access_token',
        method='POST',
        body="oauth_verifier=" + oauth_verifier
    )
    print(">>>>>>>>>>>>>>>>>>>> Request <<<<<<<<<<<<<<<<<<")
    print(oauth_verifier)
    if res['status'] != '200':
        raise Exception(
            "Invalid response %s: %s" % (res['status'], content)
        )
    access_token = dict(parse_qsl(content))


    api = oauth_login(access_token['oauth_token'], access_token['oauth_token_secret'], 
        config.object.TWITTER_OAUTH_CONSUMER_KEY, config.object.TWITTER_OAUTH_CONSUMER_SECRET)
    
    return json.dumps(api.trends.place(_id=23424768))


def oauth_login(oauth_token, oauth_token_secret, consumer_key, consumer_secret):
    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret, consumer_key, consumer_secret)
    return twitter.Twitter(auth=auth)