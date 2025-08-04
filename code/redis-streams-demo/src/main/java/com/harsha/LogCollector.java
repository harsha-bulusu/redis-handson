package com.harsha;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.StreamEntryID;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

/**
 * Producer Instance
 */
public class LogCollector {

    private static final Logger logger = LoggerFactory.getLogger(LogCollector.class);
    private static final Jedis jedis = new Jedis("localhost", 6379);

    public void collectLogs() throws Exception {
        Path logFilePath = Paths.get("logs/app.log");

        if (!Files.exists(logFilePath)) {
            logger.error("Log File not found");
            return;
        }

        logger.info("reading logs");
        try(BufferedReader bufferedReader = Files.newBufferedReader(logFilePath)) {
            String line;
            while((line = bufferedReader.readLine()) != null) {
                Map<String, String> message =  new HashMap<>();
                message.put("log", line);
                jedis.xadd(Constants.LOGS_STREAM, StreamEntryID.NEW_ENTRY, message);
                logger.info("☑️ Added message to stream");
                Thread.sleep(1000);
            }
            logger.info("✅ Completed reading logs from app");
        }
    }
}
