import libs.redis_cache_wrapper
import time
# import json

rc = libs.redis_cache_wrapper.RedisCacheWrapper(redis_host='redis-service.default.svc.cluster.local')
rc.session.cache.clear()

url = 'https://some_url'

start = time.time()
r = rc.get(url=url)
without_cache = time.time() - start

start = time.time()
r = rc.get(url=url)
with_cache = time.time() - start
print(without_cache, 'vs', with_cache)
# print(json.dumps(r.json(), indent=4))

rc.print_details()
