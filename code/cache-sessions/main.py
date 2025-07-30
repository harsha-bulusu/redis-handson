import json
import sqlite3
import os
import uuid

import redis


DATABASE_NAME = "data/my-db"

redis = redis.Redis(host='localhost', port=6379, db=0)

def setup_users():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF not exists users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
                   );
    """)
    users = [("Harsha", "Harsha123"), ("test-user", "test-user")]
    cursor.executemany("""
        INSERT INTO users (username, password) values(?,?) ON CONFLICT(username) DO NOTHING;
    """, users)
    connection.commit()
    connection.close()

def authenticate(username, password):
    # authenticate user and add session object
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    count = cursor.execute("SELECT count(*) from users where username = ? AND password = ?", (username, password))
    if count:
        # store session
        session_id = str(uuid.uuid4())
        session_key = f"session:{session_id}"
        session_data = json.dumps({"username": username})
        redis.set(session_key, session_data, ex=900)
        print(session_id)
    else:
        print("Bad credentials")

def has_session(session_id):
    # check if user has a valid session or not
    session_key = f"session:{session_id}"
    session_data = redis.get(session_key)
    return json.loads(session_data) if session_data else None

def request_home_page(session_id):
    # Return if user has valid session else ask user to authenticate
    if has_session(session_id):
        print("Welcome")
    else:
        print("Unauthorized")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    setup_users()
    username = "Harsha"
    password = "Harsha123"
    # Comment this while testing request_home_page
    # authenticate(username, password)

    # Enable it in second run so a session gets created and session id gets printed in the terminal
    # You can delete the session key from redis and give a try
    request_home_page("68ab69c7-9e7f-46c3-a83f-74475f33c65d")

