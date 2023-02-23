import logging
import os
import django
from numpy.lib.utils import source
import requests
from requests.utils import quote

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twitter_parser.core.settings")
django.setup()

from twitter_parser.core.settings import tw_tweets_data, tw_tweets_history, tw_tweets_sources
from twitter_parser.models import TwitterMessages, TwitterSources


logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)


def check_tw_message(user_id, tweet_id):
    check = TwitterMessages.find_message_by_id(user_id, tweet_id)
    return check


def create_message(data):
    result = TwitterMessages.create_record(data)
    return result


def check_tw_source(user_id):
    check = TwitterSources.find_source_by_id(user_id)
    return check


def create_source(data):
    result = TwitterSources.create_record(data)
    return result


def update_source_twitter(user_id, data):
    result = TwitterSources.update_record(user_id, data)
    return result


def update_source():
    sources = tw_tweets_sources.find()
    for source in sources:
        print(source)
        if source['OffsetId'] == 0:
            pass
        else:
            data = dict()
            data['channel_about'] = source['ChannelAbout']
            data['channel_title'] = source['ChannelTitle']
            data['creation_date'] = source['Date']
            data['followers'] = source['Followers: ']
            data['location'] = source['Location']
            update_source_twitter(source['UserID'], data)

def get_label(message):
    url = 'http://localhost:8228'
    source_lang = 'en'
    env_names = ['DET_EMOTION_MODEL', 'DET_TOPICS_MODEL', 'DET_APPROP_MODEL']
    env = env_names[0]
    d = requests.post(url + "/set_ip", json={'env': env, "ip": 'http://20.245.26.188:8010'})
    r = requests.get(f'{url}/label?message={quote(message)}&source_lang={source_lang}&env={env}')
    translated_text = r.json()
    return translated_text['label']



def add_new_messages_tw():
    messages = tw_tweets_data.find()
    for message in messages:
        check = check_tw_message(message['UserID'], message['TweetID'])
        if check is None:
            logging_info = f"Message is new! Start saving data for message id: {message['TweetID']}"
            logging.info(logging_info)
        else:
            logging_info = f"Message already exists. Message id: {message['TweetID']}, from user: {message['UserID']}"
            logging.info(logging_info)
            # tw_tweets_data.delete_one(message)
            continue
        try:
            source = check_tw_source(message['UserID'])
            label = get_label(message['Text'])
            # if source is None:
            #     logging_info = f"Source is new! Source: {message['UserID']}."
            #     logging.info(logging_info)
            #     source = {'user_id': message['UserID']}
            #     create_source(source)
            # else:
            data = {'user_id': source,
                    'tweet_id': message['TweetID'],
                    'date': message['Date'],
                    'text': message['Text'],
                    'retweet': message['Retweet'],
                    'likes': message['Likes'],
                    'location': message['Location'],
                    'has_media': message['HasMedia'],
                    'is_quote': message['IsQuote'],
                    'quote_id': message['QuoteID'],
                    'media': message['Media'],
                    'label':str(label)[2:-2],
                    }
            print(data)
            create_message(data)
                # tw_tweets_data.delete_one(message)
                # tw_tweets_history.insert_one(message)
        except Exception as e:
            logging_info = f"Error while inserting user to db, error: {e}. Error message id: {message['TweetID']}"
            logging.info(logging_info)


if __name__ == '__main__':
    add_new_messages_tw()
    #update_source()
