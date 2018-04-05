import twitter_service
import json

twitter_api = twitter_service.oauth_login()

WORLD_WOE_ID = 1

world_trends = twitter_service.twitter_trends(twitter_api, WORLD_WOE_ID)
print json.dumps(world_trends, indent=1)


BR_WOE_ID = 23424768

brazilian_trends = twitter_service.twitter_trends(twitter_api, BR_WOE_ID)

print json.dumps(brazilian_trends, indent=1)

