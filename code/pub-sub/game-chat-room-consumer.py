import redis

r = redis.Redis()

channel = f"game:{input("Enter your Game ID: ")}"
pubsub = r.pubsub()
pubsub.subscribe(channel)

print(f"Joined chat room")
for message in pubsub.listen():
    # print(message)
    if message["type"] == "message":
        print(f"{message['data'].decode()}")