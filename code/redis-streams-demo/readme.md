
---

## 🔧 Redis Stream Log Ingestion System

A sample Java project demonstrating how to:

* Generate logs,
* Collect and stream them into Redis,
* Consume them from a Redis Stream using Consumer Groups.

---

### 📁 File Overview

| File/Class          | Role                                                                  |
| ------------------- | --------------------------------------------------------------------- |
| `App.java`          | Entry point. Starts log generator and log collector in parallel.      |
| `AppInstance.java`  | Simulates log generation by writing random logs to `logs/app.log`.    |
| `LogCollector.java` | Reads lines from `logs/app.log` and pushes each line to Redis Stream. |
| `LogIngestor.java`  | Consumer that reads from Redis Stream using a consumer group.         |
| `Constants.java`    | Holds constants like stream name (not shown above, assumed present).  |

---

### ▶️ How to Run

1. **Start Redis locally** on port `6379`.
2. **Create the stream manually (only once)**:

   ```bash
   XADD log-stream * log "init"
   ```
3. **Create a consumer group**:

   ```bash
   XGROUP CREATE log-stream logs-group $
   ```
4. **Run `App.java`** (starts log generator and pushes logs to Redis stream).
5. **Run `LogIngestor.java`** (separately) to consume and process logs from the stream.

---

Let me know if you'd like Docker and Grafana support added for visualization/log metrics.
