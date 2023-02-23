import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
# MongoDB host, db name, and collection names
mng_cl = pymongo.MongoClient(f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}/")
db = mng_cl['twitter_parser']
tweets_collection = db['tw_raw']
sources_collection = db['twitter']


# Twitter API access keys(M)
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_key = os.environ["ACCESS_KEY"]
access_secret = os.environ["ACCESS_SECRET"]

# Local path to saved data(avatar and media)
path_to_files = 'data'
