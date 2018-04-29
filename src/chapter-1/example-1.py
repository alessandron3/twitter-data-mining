import twitter
from conf import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
import json


auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)
# u = twitter_api.users.show(screen_name='alessandron3')
# name = u['name']
# print(name)

user = twitter_api.account.verify_credentials()

print twitter_api