# T.S.T. - Truth Search Tool


The main service is powered by Django REST API. Using libraries such as: django-filter, django-cors-headers, psycopg2 (for working with a "clean" PostgreSQL database), mongoengine and pymongo (for working with a "dirty" / "raw" MongoDB database). For parsing Twitter, Twitter API v1 and the Tweepy library are used.

Django is a free and open-source, Python-based web framework that follows the model–template–views architectural pattern. Django REST framework is a powerful and flexible toolkit for building Web APIs.

Tweepy is an open source Python package that gives you a very convenient way to access the Twitter API with Python. Tweepy includes a set of classes and methods that represent Twitter's models and API endpoints, and it transparently handles various implementation details.

MongoEngine is a Python library that acts as an Object Document Mapper with MongoDB, a NOSQL database. It is similar to SQLAlchemy, which is the Object Relation Mapper (ORM) for SQL based databases.

### requirements.txt
```
psycopg2-binary==2.9.5
python-dotenv==0.21.1
asgiref==3.6.0
Django==4.1.7
django-filter==22.1
djangorestframework==3.14.0
importlib-metadata==6.0.0
Markdown==3.4.1
pytz==2022.7.1
sqlparse==0.4.3
zipp==3.14.0
mongoengine==0.26.0
pymongo==4.3.3
django-cors-headers==3.13.0
certifi==2020.12.5
chardet==4.0.0
oauthlib==3.1.0
python-dateutil==2.8.1
requests==2.25.1
requests-oauthlib==1.3.0
six==1.16.0
tweepy==3.10.0
urllib3==1.26.4
```

### .env for Django:
```
Django
DJANGO_SECRET_KEY=KEY
DEBUG=False

Postgres-Default
DB_NAME=name
DB_USER=user
DB_PASSWORD=pass
DB_HOST=localhost
DB_PORT=port
```

### .env for twitter_raw:
```
# Twitter_API
CONSUMER_KEY='**********'
CONSUMER_SECRET='**********'
ACCESS_KEY='**********'
ACCESS_SECRET='**********'

# # MONGO
MONGO_HOST=localhost
MONGO_PORT=port
MONGO_DBNAME=name
TW_RAW=messages
SOURCES=sources
```
