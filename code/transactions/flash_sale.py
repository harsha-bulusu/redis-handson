import redis
import threading
from concurrent.futures import ThreadPoolExecutor

redis_client = redis.Redis(host = "localhost", port = "6379", db=0)

redis_client.set("stock", 3)
lock = threading.Lock()  # for clean prints

def reserve_item(user_id):
    MAX_RETRIES = 3
    retry = 0
    while retry < MAX_RETRIES:
        try:
            pipe = redis_client.pipeline()
            pipe.watch("stock")
            stock = int(pipe.get('stock'))

            if stock <= 0:
                with lock:
                    print("❌Stock unavailable")
                return

            pipe.multi()
            pipe.decr("stock")
            pipe.setex(f"reserved:{user_id}", 300, 1)
            res = pipe.execute()
            with lock:
                print("Transaction successful", res)
            return
        except redis.WatchError:
            with lock:
                print("🔁 retry")
            retry += 1
        except Exception as e:
            print("error", e)
        finally:
            redis_client.unwatch()
    
    with lock:
        print(f"❗ {user_id}: Failed after {MAX_RETRIES} retries")



user_ids = [f"user{i}" for i in range(10)]

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(reserve_item, user_ids)