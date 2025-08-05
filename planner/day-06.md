### **🟤 Day 6: Replication, Sentinel, High Availability**

* Master-slave replication
* Start multiple Redis instances locally, link using `replicaof`

----

# Redis Master-Slave Setup - Compact Notes

1. 🟢 Start Master:
   redis-server master.conf

2. 🟡 Start Replica:
   redis-server replica.conf  
   OR use redis-cli: replicaof <master-ip> <master-port>

3. 🔍 Verify:
   On replica: INFO replication → role:slave  
   On master: INFO replication → connected_slaves:1

4. ⚙️ Key Configs:
   - replicaof <ip> <port>
   - masterauth <pwd>
   - repl-backlog-size <bytes>
   - min-replicas-to-write, min-replicas-max-lag

5. 🔄 Runtime Change:
   - Make master: replicaof no one
   - Reconnect to master: replicaof <ip> <port>

6. 📄 Sync Behavior:
   - Full sync → RDB from master + command stream
   - Partial sync → uses replication backlog buffer

7. 🔐 If master has password:
   replica needs: masterauth <password>


---

```
# Redis Replication - Quick Notes

## 🔄 Basic Replication Flow
1. Replica connects to master
2. Replica sends `PSYNC`
3. Master replies with:
   - Full sync → sends RDB, then command stream
   - Partial sync → sends missing data from backlog

## 📦 Replication Terminology
- **replication-id**: Unique ID of the master's replication stream
- **replication-offset**: Byte position in master's command stream
- **replication backlog buffer**: Circular buffer on master storing recent writes (used for partial resync)
- **master-repl-offset**: Master’s current offset
- **slave-repl-offset**: Replica's last known offset

## 🔁 Full Sync vs Partial Sync
- **Full Sync**: Triggered on first connect or when backlog is insufficient
  - Master → RDB snapshot → Replica
  - Then, command stream resumes
- **Partial Sync**: If master’s backlog still has replica's missing data
  - Master resumes from saved offset

## 🧠 Recovery Flow
- On replica restart:
  - Sends `PSYNC` with last known ID + offset
  - If match + backlog available → partial sync
  - Else → full sync

## 💾 Where is offset stored?
- Replica stores offset & master ID in `replid` and `repl_offset`
- Written to disk (AOF or RDB + `repl-state` in memory)

## 🔄 When does replication-id change?
- On master restart or `CONFIG RESETSTAT`
- Triggers full sync for replicas

## ⚡ Multi-Master Possibilities
- **Redis Cluster**: Slot-based, multiple masters
- **Redis Enterprise CRDT**: True active-active masters
- **Manual multi-master**: Not supported, risk of conflicts

```


* Redis Sentinel:

  * Failover detection
  * Auto promotion of replicas


* Simulate master crash and observe Sentinel takeover
* Build dashboard to show real-time failover