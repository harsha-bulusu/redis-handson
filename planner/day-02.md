### Redis Observability
* Observe Info and Monitor Commands

---

### Redis Data Layout
* Understand data layouts by using `OBJECT ENCODING <Key>`

----

### Redis configuration
* Understand redis.conf
     giving config to server redis-server <path-to-config-file>

     ```bash
     redis-server redis.conf
     ```
---
### Redis Persistence
* The data directory - where redis persists data
    ```bash
    grep '^dir' redis.conf
    # the default value is the present working directory
    ```
* understand redis persistence - AOF v/s RDB
    - AOF: Append Only File
    - RDB: Redis data backup

* Tune config to enable AOF appendonly true
* understand aof directory structure
    ```bash
    >> cat redis.conf | grep appendonly

    appendonly yes
    # For example, if appendfilename is set to appendonly.aof, the following file
    # - appendonly.aof.1.base.rdb as a base file.
    # - appendonly.aof.1.incr.aof, appendonly.aof.2.incr.aof as incremental files.
    # - appendonly.aof.manifest as a manifest file.
    appendfilename "appendonly.aof"
    appenddirname "appendonlydir"
    ```

#### Configuration for flushing
* understand save configuration - rdb persistence
    "seconds writes ....."
* Understand aof config
    cat redis.conf | grep aof

#### Manual Flushing of Data
* `SAVE`/`BGSAVE` - To manually flush data to RDB files    
* `BGREWRITEAOF` - To manually trigger rewrite aof **rewrites are triggered based on a threshold configuration**
 
 ---
#### Benchmark performance - AOF v/s RDB
    ```bash
    >> redis-benchmark -n 100000 -c 50 -d 256 -t set,get
    # -n number of requests
    # -c concurrency
    # -d size of data in bytes
    # -t Target commands
    ```

    * Observe the performance by enabling/disabling aof