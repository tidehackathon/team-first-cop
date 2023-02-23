from datetime import datetime
from rest_framework import serializers
from .models import Sources, TwitterSources, Twitter
from . import add_source
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)


class AddSourceViewSerializer(serializers.ModelSerializer):
    url = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Sources
        fields = ('url',)

    @classmethod
    def create_source(cls, attrs):
        source = Sources.find_source(attrs['url'])
        if source:
            content = {"meta": {"status": "Ok", "error": "null"}, "msg": "Source already exists."}
            return content
        else:
            source = Sources.objects.create(
                url=attrs['url'],
                add_date=datetime.now()
            )
            source.save()
            username = '@' + (attrs['url'].split('/')[-1])
            Twitter(UserID=username).save()
            add_source.add_twitter(source)
            content = {"meta": {"status": "Ok", "error": "null"}, "msg": "Source added."}
            return content


class DeleteSourceViewSerializer(serializers.ModelSerializer):
    url = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Sources
        fields = ('url',)

    @classmethod
    def delete_source(cls, data):
        source = Sources.find_source(url=data['url'])
        if source:
            source[0].delete()
            source = Sources.find_url(data['url'])
            if source is None:
                if data['source_type'] == 'twitter':
                    url = '@' + (data['url'].split('/')[-1])
                    TwitterSources.find_source_by_id(url).delete()
                    logging.info(f'{data["url"]} successfully deleted')
                content = {"meta": {"status": "Ok", "error": "null"}, "msg": "Source deleted."}
                return content
        else:
            content = {"meta": {"status": "error", "error": "No such source found."}}
            return content


class GetSourceViewSerializer(serializers.ModelSerializer):
    url = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Sources
        fields = ('url',)

    @classmethod
    def get_source(cls, attrs):
        url = attrs['url']
        try:
            source = Sources.objects.get(url=url)
            logging.info(f'{attrs["url"]} successfully found. Gathering info...')
        except Sources.DoesNotExist:
            content = {"meta": {"status": "error", "error": "No such source found."}}
            return content
        context = {'url': source.url, 'enabled': source.enabled}
        return context
