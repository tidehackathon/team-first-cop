import json
import time
import logging
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import AddSourceViewSerializer, DeleteSourceViewSerializer, GetSourceViewSerializer
from .models import Sources
from datetime import datetime, timedelta
from django.http import JsonResponse
from .search import twitter_search
from .models import TwitterMessages

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)


class AddSourceView(APIView):
    """ Adding new source  """
    queryset = Sources.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AddSourceViewSerializer

    @classmethod
    def post(cls, request):
        logging.info(f'Request: {request.data}')
        content = cls.serializer_class.create_source(request.data)
        return JsonResponse(content)


class DeleteSourceView(APIView):
    """ Delete source  """
    queryset = Sources.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DeleteSourceViewSerializer

    @classmethod
    def post(cls, request):
        logging.info(f'Request: {request.data}')
        content = cls.serializer_class.delete_source(request.data)
        return JsonResponse(content)


class GetAllSourcesView(APIView):
    """ Get all sources  """
    permission_classes = (AllowAny,)

    @classmethod
    def get(cls, request):
        sources = Sources.objects.all()
        sources_list = list()
        if sources is None:
            return sources_list
        else:
            for source in sources:
                sources_list.append({
                    'url': source.url,
                    'enabled': source.enabled
                })
        content = {"meta": {"status": "Ok", "error": "null"}, "sources_list": sources_list}
        return JsonResponse(content)


class GetSourceView(APIView):
    """ Get all sources  """
    queryset = Sources.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetSourceViewSerializer

    @classmethod
    def post(cls, request):
        source = cls.serializer_class.get_source(request.data)
        content = {"meta": {"status": "Ok", "error": "null"}, "source": source}
        print(content)
        return JsonResponse(content)


class SearchView(APIView):
    permission_classes = (AllowAny,)

    @classmethod
    def post(cls, request):
        if request.method == 'POST':
            PAGE_SIZE = 20
            word = request.data['string']
            date_range = request.POST.get('time', None)
            page = request.data['page']
            if word == "":
                content = {
                    "meta": {"status": "Ok", "error": "null"},
                    "response": []
                }
                return JsonResponse(content)
            logging.info(f"Request: word - {word}, date range: {date_range}, page: {page}")

            if not date_range:
                end = datetime.now()
                start = end - timedelta(days=7)
                end = end.strftime("%d.%m.%Y")
                start = start.strftime("%d.%m.%Y")
            else:
                start = date_range[0]
                end = date_range[1]
            start_date = datetime.strptime(start, '%d.%m.%Y')
            end_date = datetime.strptime(end, '%d.%m.%Y') + timedelta(days=1)
            result = []
            try:
                if page == 1:
                    tweets = TwitterMessages.count_by_word(word, start_date, end_date)
                    logging.info(f"Tweets: {tweets}")
                    if 0 < tweets < PAGE_SIZE:
                        pages_tweets = 1
                    else:
                        pages_tweets = tweets // PAGE_SIZE
                        extra_page = tweets % PAGE_SIZE
                        if extra_page > 0:
                            pages_tweets += 1
                    total_pages = pages_tweets
                    logging.info(f"Tweets: {pages_tweets}")
                    request.session['SEARCH_TWEETS_PAGE_OFFSET'] = 0
                    request.session['SEARCH_TOTAL_PAGES'] = total_pages
                    logging.info(f"SEARCH TOTAL PAGES: {request.session['SEARCH_TOTAL_PAGES']}")
                if page <= request.session.get('SEARCH_TOTAL_PAGES', 0):
                    search_page_offset = request.session.get('SEARCH_TWEETS_PAGE_OFFSET', 0)
                    logging.info(f"Test {page - search_page_offset}")
                    result = twitter_search(word, start_date, end_date, page - search_page_offset, PAGE_SIZE)
                content = {
                    "meta": {"status": "Ok", "error": "null", "page": page,
                             "pages": request.session['SEARCH_TOTAL_PAGES']},
                    "response": result
                }
                return JsonResponse(content)
            except Exception as e:
                content = {
                    "meta": {"status": "Error", "error": str(e)},
                    "response": []
                }
            return JsonResponse(content)



class Top100View(APIView):
    permission_classes = (AllowAny,)

    @classmethod
    def get(cls, request):
        tweets = TwitterMessages.objects.all().order_by('-date')[:100]
        list_of_tweets = list()
        if tweets is None:
            content = {"meta": {"status": "Error", "error": "No tweets data."}}
            return JsonResponse(content)
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
            else:
                media = None
            d['tweet'] = {'user_id': tweet.user_id.user_id,
                          'date': tweet.date,
                          'message_text': tweet.text,
                          'channel': tweet.user_id.channel_title,
                          'message_type': 'Твіт',
                          'has_media': tweet.has_media,
                          'message_attachments': media,  # path
                          'has_replies': False,
                          'is_quote': tweet.is_quote,
                          'quote_id': tweet.quote_id,
                          'likes': tweet.likes,
                          'retweets': tweet.retweet,
                          'location': tweet.location,
                          'label':tweet.label,
                          }
            list_of_tweets.append(d)
        content = {"meta": {"status": "Ok", "error": "null"}, "response": list_of_tweets}
        return JsonResponse(content)
