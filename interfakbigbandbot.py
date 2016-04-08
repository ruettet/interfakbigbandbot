from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import configparser
from json import loads
from random import randint

config = configparser.ConfigParser()
config.read('access.properties')

consumer_key=config.get('twitter', 'consumer_key')
consumer_secret=config.get('twitter', 'consumer_secret')
access_token=config.get('twitter', 'access_token')
access_token_secret=config.get('twitter', 'access_token_secret')


class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            data = loads(data)
            print(data['user']['screen_name'], data['text'])
            print("\tcreating favorite")
            api.create_favorite(data['id'])
            if 'optreden' in data['text']:
                print("\tretweeting")
                api.retweet(data['id'])
            if randint(1, 10) > 8:
                print("\tmaking friendship")       
                api.create_friendship(user_id=data['user']['screen_name'])
        except:
          pass
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = API(auth)

    stream = Stream(auth, l)
    stream.filter(track=['jazz antwerpen', 'jazz leuven', 'jazz gent', 'jazz brussel', 'jazz hasselt', 'jazz brugge',
                         'jazz charleroi', 'jazz liege', 'jazz mons', 'jazz namur', 'jazz bruxelles', 'jazz big band',
                         'big band optreden', 'jazz belgie', 'jazz vlaanderen', 'jazz wallonie', 
                         'jazz bxl'])
