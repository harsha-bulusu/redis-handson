import uuid
import redis

r = redis.Redis()

def is_allowed(user_id):
    key = f"user:{user_id}"
    script = """
        local now = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local token = ARGV[3]
        local limit = tonumber(ARGV[4])
        local user = KEYS[1]
        redis.call("ZREMRANGEBYSCORE", user, 0, now - window)

        local count = redis.call("ZCARD", user)

        if count < limit then
            redis.call("ZADD", user, now, token)
            redis.call("EXPIRE", user, math.ceil(window/1000))
            return "allowed"
        end
        return "denied"
    """

    window = 60000
    limit = 100
    res = r.eval(script, 1, key, 1754109346, window, str(uuid.uuid4()), limit)
    print(res)

for i in range(1, 11):
    is_allowed(1)
