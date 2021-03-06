# -*- coding: utf-8 -*-
import oauth2 as oauth
import twitter
import urllib
import json
import yweather

import config

from collections import Counter

from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
    url_for,
    request,
    jsonify,
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
    name = session['user']['screen_name']
    img = session['user']['profile_image_url']
    
    return render_template('index.html', name=name, profile_image=img)

@app.route('/trends')
def trends(): 
    name = session['user']['screen_name']
    img = session['user']['profile_image_url']

    return render_template('trends.html', name=name, profile_image=img)

@app.route('/followers')
def followers(): 
    name = session['user']['screen_name']
    img = session['user']['profile_image_url']

    return render_template('followers.html', name=name, profile_image=img)

@app.route('/timeline')
def timeline(): 
    name = session['user']['screen_name']
    img = session['user']['profile_image_url']

    return render_template('timeline.html', name=name, profile_image=img)

@app.route('/tweets')
def tweets():
    name = session['user']['screen_name']
    img = session['user']['profile_image_url']

    return render_template('tweets.html', name=name, profile_image=img)

@app.route('/trends-woeid')
def trends_json():
    region = request.args.get('region')
    client = yweather.Client()
    woeid = client.fetch_woeid(region)

    api = oauth_login(session['oauth_token'], session['oauth_token_secret'], 
        config.object.TWITTER_OAUTH_CONSUMER_KEY, config.object.TWITTER_OAUTH_CONSUMER_SECRET)

    try:
        response = api.trends.place(_id=woeid)
        return jsonify(
            status="ok",
            trends=response[0]['trends']
        )
    except: 
        print("erro")
        return jsonify(status="error")

@app.route('/tweets/search')
def tweets_json():

    q = request.args.get('q')

    api = oauth_login(session['oauth_token'], session['oauth_token_secret'], 
        config.object.TWITTER_OAUTH_CONSUMER_KEY, config.object.TWITTER_OAUTH_CONSUMER_SECRET)

    try:
        resp = api.search.tweets(q=q, count=200)
        
        statuses = resp['statuses']
        max_results = min(1000, 100)

        for _ in range(10): #10 * 100 = 1000
            try:
                next_results = resp['search_metadata']['next_results']
            except KeyError, e:
                break

            kwargs = dict([ kv.split('=')
                            for kv in next_results[1:].split("&") ])

            search_results = api.search.tweets(**kwargs)
            
            statuses += search_results['statuses']
            
            if len(statuses) > max_results:
                break

        return jsonify(
            status="ok",
            tweets=statuses
        )
    except:
        print("error")
        return jsonify(status="error")



@app.route('/login', methods = [ 'GET', 'POST' ])
def login():
    res, content = oauth_client.request('https://api.twitter.com/oauth/request_token?%s' % urllib.urlencode({
                                        'oauth_callback': 'http://localhost:5000' + url_for('root.oauth_authorized')
                                        }).replace('+', '%20'), 'GET',)
    if res['status'] != '200':
        raise Exception("Invalid response %s: %s" % (res['status'], content))

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
    oauth_verifier = request.args.get('oauth_verifier')

    client = oauth.Client(oauth_consumer, token)
    res, content = client.request(
        'https://api.twitter.com/oauth/access_token',
        method='POST',
        body="oauth_verifier=" + oauth_verifier
    )

    if res['status'] != '200':
        raise Exception(
            "Invalid response %s: %s" % (res['status'], content)
        )
    access_token = dict(parse_qsl(content))

    api = oauth_login(access_token['oauth_token'], access_token['oauth_token_secret'], 
        config.object.TWITTER_OAUTH_CONSUMER_KEY, config.object.TWITTER_OAUTH_CONSUMER_SECRET)
    session['oauth_token'] = access_token['oauth_token']
    session['oauth_token_secret'] = access_token['oauth_token_secret']

    user = api.account.verify_credentials()
    session['user'] = user
    return redirect('http://localhost:5000/')


def oauth_login(oauth_token, oauth_token_secret, consumer_key, consumer_secret):
    auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret, consumer_key, consumer_secret)
    return twitter.Twitter(auth=auth)

@app.route('/favorites-json')
def analyze_favorites():
    screen_name = request.args.get('screen_name')
    entity_threshold=2
    api = oauth_login(session['oauth_token'], session['oauth_token_secret'], 
        config.object.TWITTER_OAUTH_CONSUMER_KEY, config.object.TWITTER_OAUTH_CONSUMER_SECRET)
    
    favs = api.favorites.list(screen_name=screen_name, count=1000)
    print "number of favorites:", len(favs)

    common_entities = get_common_entities(favs, entity_threshold=entity_threshold)

    return jsonify(
            status="ok",
            favorites=common_entities
        )

@app.route('/followers-json')
def followers_json():
    screen_name = request.args.get('screen_name')
    
    api = oauth_login(session['oauth_token'], session['oauth_token_secret'], 
        config.object.TWITTER_OAUTH_CONSUMER_KEY, config.object.TWITTER_OAUTH_CONSUMER_SECRET)

    suggest = api.followers.list(screen_name=screen_name, count=200)

    return jsonify(
            status="ok",
            followers=suggest
        )


@app.route('/tweets/timeline')
def tweets_user():
    screen_name = request.args.get('screen_name')
    
    api = oauth_login(session['oauth_token'], session['oauth_token_secret'], 
        config.object.TWITTER_OAUTH_CONSUMER_KEY, config.object.TWITTER_OAUTH_CONSUMER_SECRET)
    return jsonify(
        status="ok",
        tweets= api.statuses.user_timeline(screen_name=screen_name, count=200, include_rts=0)
    )


def get_common_entities(statuses, entity_threshold=3):
    tweet_entities = [
        e 
        for status in statuses
            for entity_type in extract_tweet_entities([status])
                for e in entity_type
    ]

    c = Counter(tweet_entities).most_common()

    return [
        (k,v)
        for (k,v) in c 
            if v >= entity_threshold
    ]


def extract_tweet_entities(statuses):
    if len(statuses) == 0:
        return [], [], [], [], []
    
    screen_name = [
        user_mention['screen_name']
            for status in statuses
                for user_mention in status['entities']['user_mentions']
    ]

    hashtags = [
        hashtag['text']
            for status in statuses
                for hashtag in status['entities']['hashtags']
    ]

    urls = [
        url['expanded_url']
            for status in statuses
                for url in status['entities']['urls']
    ]

    symbols = [
        symbol['text']
            for status in statuses
                for symbol in status['entities']['symbols']
    ]

    if status['entities'].has_key('media'):
        media = [
            media['url']
                for status in statuses
                    for media in status['entities']['media']
        ]
    else: 
        media = []

    return screen_name, hashtags, urls, media, symbols