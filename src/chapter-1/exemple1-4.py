import twitter
import json
from conf import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

WORLD_WOE_ID = 1
BR_WOE_ID = 23424768 #Brazil code

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
br_trends = twitter_api.trends.place(_id=BR_WOE_ID)

world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])

br_trends_set = set([trend['name'] for trend in br_trends[0]['trends']])


common_trends = world_trends_set.intersection(br_trends_set)

print common_trends