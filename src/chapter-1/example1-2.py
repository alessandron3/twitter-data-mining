import twitter
import json
from conf import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

WORLD_WOE_ID = 1
BR_WOE_ID = 23424768 #Brazil code

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
br_trends = twitter_api.trends.place(_id=BR_WOE_ID)

print json.dumps(world_trends, indent=1)
print 
print json.dumps(br_trends, indent=1)