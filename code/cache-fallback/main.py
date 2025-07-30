import redis
import functools
import time

redis = redis.Redis(host='localhost', port='6379')

def redis_cache(key_prefix, ttl=3600):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            #cache key
            arg_str=":".join(map(str, args))
            key = f"{key_prefix}:{arg_str}"

            #cache_hit
            cached_value = redis.get(key)
            if cached_value:
                return int(cached_value)

            print(f"🚨 Cache miss for key: {key}")
            result = func(*args, **kwargs) #compute

            #cache computation
            redis.setex(key, ttl, str(result))
            return result
        return wrapper
    return decorator


@redis_cache("my-cache", ttl=300)
def compute(start, end):
    result = 0
    for i in range(start, end):
        result = result + i
    return result

if __name__=="__main__":
    start_time = time.time()
    print(compute(1, 10000000))
    end_time = time.time()
    print(f"⏱️ Computed in {end_time - start_time:.4f} seconds")
    # Tune the values of start and end, you will observe
    #   - Linear change w.r.t start and end on cache miss
    #   - on cache found it returns result in constant time
