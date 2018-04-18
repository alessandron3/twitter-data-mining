# -*- coding: utf-8 -*-
import oauth2 as oauth
import twitter
import urllib

import config

from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
    url_for,
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
    res, content = oauth_client.request(
        'https://api.twitter.com/oauth/request_token?%s'
        % urllib.urlencode({
             'oauth_callback': 'http://localhost:5000' + url_for('root.oauth_authorized')
        }).replace('+', '%20'),
        'GET',
    )
    if res['status'] != '200':
        raise Exception(
            "Invalid response %s: %s" % (res['status'], content)
        )

    request_token = dict(parse_qsl(content))
    session['request_token'] = request_token
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
    print(">>>>>>>>>>>>>>>")
    print(token)
    print("<<<<<<<<<<<<<<<")
    client = oauth.Client(oauth_consumer, token)
    res, content = client.request(
        'https://api.twitter.com/oauth/access_token',
        'POST'
    )

    if res['status'] != '200':
        raise Exception(
            "Invalid response %s: %s" % (res['status'], content)
        )
    access_token = dict(parse_qsl(content))

    api = twitter.Api(
        consumer_key = config.object.TWITTER_OAUTH_CONSUMER_KEY,
        consumer_secret = config.object.TWITTER_OAUTH_CONSUMER_SECRET,
        access_token_key = access_token['oauth_token'],
        access_token_secret =  access_token['oauth_token_secret'],
    )
    return str(api.VerifyCredentials())