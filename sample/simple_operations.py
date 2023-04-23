import redis
import json

rdb = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
data = {
    'key': 'value'
}

namespace = 'ns'  # Redis namespace
key = f'{namespace}:test_key1'
rdb.json().set(key, '.', {})
rdb.json().set(key, 'something1', data)

for item in rdb.keys(f'{namespace}:*'):
    print(item.replace(f'{namespace}:', ''))
    r = rdb.json().get(item)
    print(json.dumps(r, indent=4))

rdb.delete(key)
