import redis

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)

