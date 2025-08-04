import redis

r = redis.Redis()

username = input("Enter your username: ")
game_room_id = "game:" + input("Enter Game ID: ")
print("=======You Can Chat Now=========")
# consider it like a web socket connection
while True:
    message = input()
    #PUBLISH Channel message
    r.publish(game_room_id, f"{username}: {message}")
    