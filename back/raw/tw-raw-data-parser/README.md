# Twitter parser

## Summary
Parsing of Twitter accounts to get text.

## Requirements:
* MongoDB 4.2.6
* Python3
* Python3-pip
* tweepy(and you should get Twitter API Keys)
* python-dotenv

## Installation:
```
pip install -r requirements.txt
```

## Configuration
Create config.py at the root directory of the project and fill in needed vars:
```
from pymongo import *

# MongoDB host, db name, and collection names
mng_cl = MongoClient('mongodb://localhost:27017/')
db = mng_cl['scrapper']
user_collection = db['twitter_users_data']
tweets_collection = db['twitter_tweets_data']
sources_collection = db['sources']

# Twitter API access keys
consumer_key = 'key'
consumer_secret = 'key'
access_key = 'key'
access_secret = 'key'

# Local path to saved data(avatar and media)
path_to_files = 'Your/local/path'
```


## Limits:
* 100 000 requests is extractive for one Twitter API key per day.
* 3200-3250 tweets for one fetching(for fetching_tweets)
* So far media is not downloadable(saving links of media).
* Once per 15 minute we can check up to 10 users(as a first fetching)
