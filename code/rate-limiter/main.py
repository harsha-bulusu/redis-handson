import redis
import time

redis = redis.Redis(host='localhost', port=6379)

def is_allowed(user_id: str):
    key = f"rate:{user_id}"

    count = redis.incr(key)

    if count == 1:
        redis.expire(count, window)

    print(f"User {user_id}: count = {count}")
    return count <= limit

if __name__ == '__main__':
    limit = 5
    window = 60

    for i in range(1, 10):
        if is_allowed("user123"):
            print("✅ Allowed")
        else:
            print("❌ Rejected")
        time.sleep(2)