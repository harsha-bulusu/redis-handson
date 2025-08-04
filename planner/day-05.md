---

## 🎯 **Day 4: Redis Pub/Sub vs Streams – Deep Dive with Real-World Use Cases**

---

## 🔴 **Redis Pub/Sub – Push-based Fan-out Messaging**

Pub/Sub is a **lightweight, real-time messaging system** ideal for **notifications and live communication**. It’s **fire-and-forget**—no message persistence, no acknowledgment, and no recovery.

### 🔧 Core Pub/Sub Commands

| Command                      | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| `PUBLISH channel message`    | Send a message to all current subscribers.       |
| `SUBSCRIBE channel [...]`    | Subscribe to one or more channels.               |
| `UNSUBSCRIBE [channel ...]`  | Unsubscribe from channels.                       |
| `PSUBSCRIBE pattern [...]`   | Subscribe with wildcard pattern (`user:*`, etc). |
| `PUNSUBSCRIBE [pattern ...]` | Unsubscribe from patterns.                       |

### 🔍 Introspection Commands

| Command                       | Description                |
| ----------------------------- | -------------------------- |
| `PUBSUB CHANNELS [pattern]`   | List active channels.      |
| `PUBSUB NUMSUB channel [...]` | Get number of subscribers. |
| `PUBSUB NUMPAT`               | Count pattern subscribers. |

### 🧠 Mental Model

```
[PUBLISH "game:room1" "hi"] → Redis → SUBSCRIBERS
                                └─ Alice
                                └─ Bob
```

* 🔸 **No durability** — messages are discarded if no one is listening.
* 🔸 **All subscribers receive the same message**.
* 🔸 Cannot retrieve old messages or retry.

### ✅ Best For

* Live chat, multiplayer lobbies
* Config propagation
* Cache invalidation
* Realtime notification triggers

---

## 🟢 **Redis Streams – Pull-based, Durable, and Trackable**

Redis Streams are **append-only log structures** with **durability**, **acknowledgment**, and **consumer group support** for **parallel message processing and fault recovery**.

---

## ✍️ Writing to a Stream

| Command                               | Description                      |
| ------------------------------------- | -------------------------------- |
| `XADD mystream * field1 val1 ...`     | Add entry with auto-generated ID |
| `XADD mystream 1691171234567-0 ...`   | Add with explicit ID             |
| `XTRIM mystream MAXLEN 1000`          | Trim by length (soft limit)      |
| `XTRIM mystream MINID <timestamp-id>` | Trim by timestamp (hard delete)  |
| `XDEL mystream <id>`                  | Delete entry by ID               |

✅ All key-value pairs in one `XADD` = **one atomic entry**

```bash
XADD logs * level warning msg "Disk 90% full"
```

---

## 📖 Reading from Streams (Non-Group Mode)

| Command                               | Description                                |
| ------------------------------------- | ------------------------------------------ |
| `XREAD STREAMS mystream 0`            | Read all from beginning                    |
| `XREAD STREAMS mystream $`            | Read only new messages from now on         |
| `XREAD COUNT 10 STREAMS mystream 0`   | Batch read 10 messages                     |
| `XREAD BLOCK 5000 STREAMS mystream $` | Block (long-poll) up to 5s for new entries |

### ✅ Key Concepts for XREAD

* `0` → Read from **beginning**
* `$` → Read **only new messages** (like tailing a log)
* `BLOCK` → Wait up to N milliseconds if no messages
* `COUNT N` → Read up to N messages per stream

```bash
XREAD COUNT 5 BLOCK 1000 STREAMS mystream $
```

🧠 Ideal for **simple log readers or tailing tools**.

---

## 👥 Consumer Groups (Scalable Parallelism)

Use consumer groups when you want **at-least-once delivery**, **message acknowledgment**, **parallelism**, and **fault recovery**.

| Command                                                | Description                           |
| ------------------------------------------------------ | ------------------------------------- |
| `XGROUP CREATE mystream group1 $`                      | Create group. `$` = start from latest |
| `XREADGROUP GROUP group1 consumer1 STREAMS mystream >` | Read unacknowledged entries           |
| `XACK mystream group1 id`                              | Acknowledge message                   |
| `XPENDING mystream group1`                             | View unacked message stats            |
| `azaz    | Auto-claim messages pending for > 60s |

### 🧠 How `XREADGROUP` Works

* `>` → Only fetch **unseen entries** for this group
* Each consumer in the group receives different messages
* Messages must be **acknowledged** with `XACK`
* Unacked messages stay in the Pending Entries List (PEL)

```bash
XREADGROUP GROUP group1 c1 COUNT 5 BLOCK 3000 STREAMS mystream >
```

🔄 **If a consumer crashes**, another can use `XCLAIM` or `XAUTOCLAIM` to recover its messages.

---

## 📋 Tracking & Introspection

| Command                                     | Description                                    |
| ------------------------------------------- | ---------------------------------------------- |
| `XINFO STREAM mystream`                     | Overview: length, last ID, first entry, etc.   |
| `XINFO GROUPS mystream`                     | All groups: last-delivered ID, pending counts  |
| `XINFO CONSUMERS mystream group`            | See per-consumer lag, pending count, idle time |
| `XPENDING mystream group [start end count]` | See exact pending entries                      |

---

## ⚙️ Durable Stream Flow – Group Mode

```
Producer ——(XADD)—→ [ Redis Stream ]

                        ↓
     ┌─────────────────────────────────────┐
     │     Consumer Group: payments        │
     │  ┌────────────┬────────────┬──────┐ │
     │  │ consumer-a │ consumer-b │ ...  │ │
     │  └────────────┴────────────┴──────┘ │
     └─────────────────────────────────────┘
                        ↓
                [ XREADGROUP ] → [ Process ] → [ XACK ]
                                   ↓
                     [ XPENDING for monitoring ]
```

---

## 🧠 Pub/Sub vs Stream – Mental & Functional Differences

| Feature                  | Pub/Sub                      | Redis Streams                    |
| ------------------------ | ---------------------------- | -------------------------------- |
| **Delivery Model**       | Push                         | Pull (XREAD or XREADGROUP)       |
| **Persistence**          | ❌ Ephemeral                  | ✅ Durable                        |
| **Replay Old Messages**  | ❌ Not possible               | ✅ Use XRANGE or start from ID    |
| **Acknowledgment**       | ❌ None                       | ✅ With `XACK`                    |
| **Consumer Parallelism** | ❌ All receive same           | ✅ 1-of-N in consumer group       |
| **Fault Recovery**       | ❌ Not possible               | ✅ Use `XPENDING`, `XCLAIM`, etc. |
| **Good For**             | Realtime alerts, simple chat | Queues, pipelines, audits        |
| **Ordering**             | N/A                          | ✅ Stream order guaranteed        |

---

## ✅ Use Case Guide

| Use Case                  | Pub/Sub ✅ | Streams ✅  |
| ------------------------- | --------- | ---------- |
| **Live Chat (untracked)** | ✅         | ❌ Overkill |
| **Durable Job Queues**    | ❌         | ✅          |
| **Log Aggregation**       | ❌         | ✅          |
| **Sensor Data Ingestion** | ❌         | ✅          |
| **Cache Invalidation**    | ✅         | ❌          |
| **Real-Time Push**        | ✅         | ❌          |
| **Payment Retry Queue**   | ❌         | ✅          |

---

## 🛠️ Real Systems You Can Build

### 🔸 Chat Room (Fast, Stateless)

* `PUBLISH chat:room1 "hi"`
* WebSocket → Redis → Subscribers

### 🔸 Log Collector (Durable)

* `XADD logs * msg "error at 12:04"`
* `XREADGROUP GROUP collectors c1 STREAMS logs >`

### 🔸 Payment Retry Queue

* `XADD payments * id 123 status pending`
* Retry stuck with `XPENDING` → `XCLAIM`

### 🔸 IoT Data Aggregator

* `XADD sensors:dev01 * temp 32.5`
* Stream → Batch Processor → TSDB

---
