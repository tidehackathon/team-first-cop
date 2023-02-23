import logging
from .models import TwitterMessages

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)


def find_word_in_tweets(word, start, end, page, page_size):
    results = TwitterMessages.find_tweet_by_word(word, start, end, page, page_size)
    return results


def twitter_search(word, start_date, end_date, page, page_size):
    list_of_tweets = list()
    tweets = find_word_in_tweets(word, start_date, end_date, page, page_size)
    if tweets is None:
        return None
    for tweet in tweets:
        d = dict()
        if tweet.has_media:
            media = list()
            count = 0
            for i in tweet.media[1:-1].split(','):
                if count >= 1:
                    i = i[2:-1]
                else:
                    i = i[1:-1]
                media.append(i)
                count += 1
            print(media)
        else:
            media = None
        d['tweet'] = {'user_id': tweet.user_id.user_id,
                      'date': tweet.date,
                      'message_text': tweet.text,
                      'channel': tweet.user_id.channel_title,
                      'message_type': 'Твіт',
                      'has_media': tweet.has_media,
                      'message_attachments': media,                       # path
                      'has_replies': False,
                      'is_quote': tweet.is_quote,
                      'quote_id': tweet.quote_id,
                      'likes': tweet.likes,
                      'retweets': tweet.retweet,
                      'location': tweet.location,
                      'label': tweet.label,
                      }
        list_of_tweets.append(d)
    return list_of_tweets
