import logging
from .models import Sources, TwitterSources

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)


# TWITTER SOURCE
def add_new_twitter_source(data):
    result = TwitterSources.create_record(data)
    return result


def check_twitter_source(data):
    result = TwitterSources.find_source_by_id(data)
    return result


# Twitter
def add_twitter(source):
    """Add twitter source from view.py"""
    url = '@' + (source.url.split('/')[-1])
    if check_twitter_source(url):
        twitter_source = check_twitter_source(url)
        twitter_source.source.add(source)
        logging.info(f'Source twitter {url} already exists.')
    else:
        new_twitter_source = {'user_id': url}
        twitter_source = add_new_twitter_source(new_twitter_source)
        twitter_source.source.add(source)
        logging.info(f'Source twitter {url} saved as new.')
