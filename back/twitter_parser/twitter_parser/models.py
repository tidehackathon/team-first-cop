from django.db import models
from asgiref.sync import sync_to_async
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, connect, ListField, ReferenceField
from .core.settings import MONGO_HOST, MONGO_PORT, MONGO_DBNAME

# MONGO_HOST = 'localhost'
# MONGO_PORT = 27017
# MONGO_DBNAME = 'twitter_parser'
# connect mongodb
mongo_connection_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}"
connect(host=mongo_connection_uri)
print(f"Connected to MongoDB: {mongo_connection_uri}")


""" Models for twitter parser mongo database """


class Twitter(Document):
    UserID = StringField(required=True)
    enabled = BooleanField(default=True)
    channel_about = StringField()
    channel_title = StringField()
    followers = IntField()
    username = StringField()
    location = StringField()
    has_photo = BooleanField()
    LastParsed = DateTimeField(null=True)
    OffsetId = IntField(default=0)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_date = models.DateTimeField(null=True, auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now=True)

    @classmethod
    @sync_to_async
    def all(cls, ):
        return list(cls.objects.all())

    @classmethod
    @sync_to_async
    def update_by_filter(cls, filters, data):
        rec = cls.objects.filter(**filters)
        rec.update(**data)
        return list(rec)


class Sources(models.Model):
    url = models.TextField()
    enabled = models.BooleanField(default=True)
    add_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'sources'
        verbose_name_plural = "Sources"

    @classmethod
    def find_source(cls, url):
        records = cls.objects.filter(url=url)
        if records:
            return records
        return None


    @classmethod
    def find_url(cls, url):
        records = cls.objects.filter(url=url)
        if records:
            return records
        return None

    @classmethod
    def new_source(cls, data):
        rec = cls.objects.create(**data)
        return rec


""" Models for Twitter: TwitterSources, TwitterMessages """


class TwitterSources(models.Model):
    source = models.ManyToManyField(Sources)
    user_id = models.TextField(db_index=True)
    has_photo = models.BooleanField(default=False)
    channel_about = models.TextField(null=True)
    channel_title = models.TextField(null=True)
    creation_date = models.DateTimeField(null=True)
    followers = models.IntegerField(null=True)
    location = models.TextField(null=True)

    class Meta:
        db_table = 'twitter_sources'
        verbose_name_plural = "Twitter Sources"

    @classmethod
    def create_record(cls, data):
        rec = cls.objects.create(**data)
        return rec

    @classmethod
    def find_source_by_id(cls, user_id):
        try:
            records = cls.objects.get(user_id=user_id)
            if records:
                return records
            return None
        except TwitterSources.DoesNotExist:
            return None

    @classmethod
    def update_record(cls, user_id, data):
        rec = cls.objects.filter(user_id=user_id)
        rec.update(**data)
        return list(rec)


class TwitterMessages(models.Model):
    user_id = models.ForeignKey(TwitterSources, models.DO_NOTHING, blank=True, null=True)
    tweet_id = models.TextField()
    date = models.DateTimeField(null=True)
    text = models.TextField(null=True)
    retweet = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)
    location = models.TextField(null=True)
    has_media = models.BooleanField()
    media = models.TextField(blank=True, null=True)
    is_quote = models.BooleanField(blank=True, null=True)
    quote_id = models.TextField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'twitter_messages'
        verbose_name_plural = "Twitter Messages"

    @classmethod
    def create_record(cls, data):
        rec = cls.objects.create(**data)
        return rec

    @classmethod
    def find_message_by_id(cls, user_id, tweet_id):
        records = cls.objects.filter(user_id__user_id=user_id, tweet_id=tweet_id)
        if records:
            return records
        return None

    @classmethod
    def count_by_word(cls, word, start, end):
        params = dict(
            text__icontains=word,
            date__range=(start, end),
        )

        num_records = cls.objects.filter(**params).count()
        return num_records

    @classmethod
    def find_tweet_by_word(cls, word, start, end, page, page_size):
        params = dict(
            text__icontains=word,
            date__range=(start, end),
        )
        records = cls.objects.filter(**params).select_related('user_id').order_by('date')
        return records[(page - 1) * page_size: page * page_size]
