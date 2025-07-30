
## Redis setup via sourcecode
Clone the latest Redis repository:

```bash
    git clone https://github.com/redis/redis.git
    cd redis
```

Compile Redis:

```bash
    make
```
Run Redis server and CLI (in separate terminals):

```bash
    src/redis-server
    src/redis-cli
```

### Commands
    - String && counter
    - List
    - set
    - scan
    - hashes
    - Sorted Sets

### Code a rate limiter && Leaderboard