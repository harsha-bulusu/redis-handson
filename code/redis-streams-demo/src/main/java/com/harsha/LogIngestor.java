package com.harsha;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.StreamEntryID;
import redis.clients.jedis.params.XReadGroupParams;
import redis.clients.jedis.resps.StreamEntry;

import java.util.List;
import java.util.Map;

/**
 * Consumer app who ingests logs
 */
public class LogIngestor {

    private static final Logger logger = LoggerFactory.getLogger(LogIngestor.class);

    /**
     * Assuming we are ingesting logs to Elastic Search
     */
    public void readAndIngestLogs() throws Exception {
        String groupName = "logs-group";
        String consumerName = "logs-group-01";
        try (Jedis jedis = new Jedis("localhost", 6379)) {
            logger.info("Connected to redis, polling messages from logs-stream");

            while (true) {
                // Returns list of streams and their events
                List<Map.Entry<String, List<StreamEntry>>> streams = jedis.xreadGroup(groupName, consumerName, XReadGroupParams.xReadGroupParams().count(5), Map.of(Constants.LOGS_STREAM, StreamEntryID.XREADGROUP_UNDELIVERED_ENTRY));
                if (streams != null) {
                    logger.info("Received events, ingestion in progress");
                    for (Map.Entry<String, List<StreamEntry>> stream : streams) {
                        List<StreamEntry> messages = stream.getValue();
                        for (StreamEntry message : messages) {
                            logger.info("message ID: {}", message.getID());
                            logger.info("message Content {}", message.getFields());
                            // Acknowledgment
                            jedis.xack(Constants.LOGS_STREAM, groupName, message.getID());
                            Thread.sleep(5000);
                        }
                    }
                    logger.info("Ingestion completed");
                } else {
                    logger.info("No events");
                }
            }
        } catch (Exception ex) {
            logger.error("❌Error while reading logs from redis stream");
        }
    }

    public static void main(String[] args) throws Exception {
        new LogIngestor().readAndIngestLogs();
    }

}
