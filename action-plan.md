Here's a **7-day deep dive plan** to master Redis with local setup, internals, and practical design-focused learning tailored for your background as a senior full stack engineer:

---

### ✅ **Goals by End of Day 7**

* Master Redis data structures, persistence, replication, clustering, and transactions.
* Understand internals (event loop, memory model, command processing).
* Build, debug, and optimize real-world use cases (e.g., rate limiting, queues, caching, pub/sub).
* Be able to reason about Redis trade-offs in systems design interviews.

---

## 🔧 **Local Setup Before Day 1**

* Install Redis from source:

  ```bash
  git clone https://github.com/redis/redis.git
  cd redis && make
  src/redis-server
  ```
* Enable persistence, set custom port, configure RDB/AOF in `redis.conf`
* Install Redis CLI tools: `redis-cli`, `redis-benchmark`, etc.

---

## 📅 **7-Day Redis Mastery Plan**

---

### **🟢 Day 1: Core Concepts, Setup, and Data Types**

**Morning**

* Redis architecture: single-threaded I/O model, command execution cycle
* Install Redis from source, start multiple instances, inspect `redis.conf`

**Afternoon**

* Core data types with hands-on:

  * `STRING`, `LIST`, `SET`, `HASH`, `ZSET`
  * Time complexity, encoding (SDS, ziplist, intset, hashtable)
* Use `MONITOR` and `INFO` to observe live command flows

**Evening**

* Implement: Simple cache with TTL, leaderboard using `ZADD`/`ZRANGE`

---

### **🟡 Day 2: Persistence (RDB + AOF), Memory Internals**

**Morning**

* RDB vs AOF: triggers, formats, use cases
* Run benchmark with and without AOF

**Afternoon**

* Memory model:

  * Object encoding
  * `maxmemory` policies
  * Eviction algorithms: `volatile-lru`, `allkeys-random`, etc.

**Evening**

* Inspect dump.rdb and appendonly.aof
* Implement: Write-through cache and observe persistence across restart

---

### **🔵 Day 3: Transactions, Lua, Pipelines, Expiry, Bitmaps**

**Morning**

* Atomic operations: `MULTI`, `EXEC`, `WATCH`
* Transactions vs pipelining

**Afternoon**

* Scripting with `EVAL`, sandboxed execution
* Advanced types: `BITFIELD`, `HYPERLOGLOG`, `GEO`, `STREAM`

**Evening**

* Implement:

  * Lua script for atomic stock decrement
  * Rate limiter using sorted set + Lua

---

### **🟣 Day 4: Pub/Sub, Streams, Blocking Commands, Redis Streams**

**Morning**

* Pub/Sub model vs Kafka
* Implement channel-based notification system

**Afternoon**

* Redis Streams:

  * Producers, consumers, consumer groups
  * Blocking reads with `XREAD`, `XGROUP`

**Evening**

* Build: Log ingestion system with Redis Stream consumers

---

### **🟤 Day 5: Replication, Sentinel, High Availability**

**Morning**

* Master-slave replication
* Start multiple Redis instances locally, link using `replicaof`

**Afternoon**

* Redis Sentinel:

  * Failover detection
  * Auto promotion of replicas

**Evening**

* Simulate master crash and observe Sentinel takeover
* Build dashboard to show real-time failover

---

### **🔴 Day 6: Redis Cluster, Sharding, Consistent Hashing**

**Morning**

* Set up Redis cluster with 6 nodes, 3 masters, 3 replicas
* Key slot hashing, rebalancing slots

**Afternoon**

* Internals: Hash slot allocation, cluster bus protocol, MOVED/ASK
* Use `redis-cli --cluster` to inspect cluster topology

**Evening**

* Design: Sharded session store, Redis cluster-based cache layer

---

### **🟠 Day 7: Real-world Patterns, Internals, and Debugging**

**Morning**

* Redis Internals:

  * Event loop (ae.c)
  * Command dispatch (server.c)
  * SDS (sds.c), Dict (dict.c)

**Afternoon**

* Debugging:

  * Latency monitoring, slowlog, `MONITOR`
  * Memory leaks with `MEMORY DOCTOR`, `valgrind`

**Evening**

* Implement & benchmark:

  * Distributed lock (RedLock)
  * Delayed job queue
* Revisit: Use cases — caching, rate limiting, sessions, pub/sub

---

## 🧰 Bonus Tools for Deep Dive

* [redis-py](https://github.com/redis/redis-py): Use Python client to script automation
* [RDM](https://redisdesktop.com/): GUI to browse Redis
* Wireshark: Inspect Redis protocol over TCP
* `perf`, `gdb`, `valgrind`: For low-level profiling

---

If you’d like, I can help you:

* Set up each day’s local experiment code
* Build a Redis client or wrapper
* Generate system design mockups with Redis usage patterns

Would you like a Notion/Markdown version of this plan or a GitHub repo with day-wise folders too?
