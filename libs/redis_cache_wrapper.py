from requests_cache import RedisCache, CachedSession
import logging
import sys


class RedisCacheWrapper:
    """Redis Cache wrapper class"""

    def __init__(self, log_level='WARNING', redis_host='', redis_port=6379, ttl=3600, name='default_cache'):
        assert redis_host
        logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s', level=log_level.upper(), stream=sys.stderr)
        backend = RedisCache(namespace=name, host=redis_host, port=redis_port)
        self.ttl = ttl
        self.session = CachedSession(cache_name=name, expire_after=self.ttl, backend=backend, allowable_codes=(200, 301))
        self.local_session = CachedSession(expire_after=self.ttl, backend='sqlite')

    def get(self, url='', params=None, **kwargs):
        assert url
        try:
            r = self.session.get(url=url, params=params, **kwargs)
        except Exception:
            logging.error('Fallback to local cache')
            r = self.local_session.get(url=url, params=params, **kwargs)
        return r

    def print_urls(self):
        print('Cached URLS:')
        print('\n'.join(self.session.cache.urls()))  # will print cached URLs

    def print_details(self):
        print('\nCache details:')
        for response in self.session.cache.responses.values():
            print('Request: {}'.format(response.url))
            print('Is response form cache: {}'.format(response.from_cache))
            print('When was cache created: {}'.format(response.created_at))
            print('When will cache expire: {}'.format(response.expires))
            print('Is cache expired: {}'.format(response.is_expired))
            print('Cache size: {} bytes'.format(response.size))
            print('------------------')
