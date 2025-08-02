import redis
from concurrent.futures import ThreadPoolExecutor

r = redis.Redis()
r.set("stock", 5)


def reserve_order(user_id):
    reserve_key = f"reserve:{user_id}"
    script = """
        local stock = tonumber(redis.call("GET", "stock"))
        if stock and stock <= 0 then
            return "sold out"
        end
        redis.call("DECR", "stock")
        redis.call("SETEX", KEYS[1], 300, 1)
        return "success"
    """

    res = r.eval(script, 1, reserve_key).decode()
    if res == "success":
        print(f"✅ Success - {reserve_key}")
    else:
        print(f"❌ Failed to order - {reserve_key}")

user_ids = [f"user{i}" for i in range(20)]

with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(reserve_order, user_ids)