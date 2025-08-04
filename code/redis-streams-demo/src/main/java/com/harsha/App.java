package com.harsha;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Hello world!
 */
public class App {

    private static final Logger logger = LoggerFactory.getLogger(App.class);
    public static void main(String[] args) throws Exception {
        /**
         * Start all the instances (application, producer, consumers)
         */
        logger.info("App started");

        ExecutorService executor = Executors.newFixedThreadPool(2);

        executor.submit(() -> {
            try {
                new AppInstance().log();
            } catch (Exception e) {
                logger.error("❌ Error in AppInstance", e);
            }
        });

        executor.submit(() -> {
            try {
                new LogCollector().collectLogs();
            } catch (Exception e) {
                logger.error("❌ Error in LogCollector", e);
            }
        });


        /*
            * Create one consumer group in redis-cli. Can be also created via a program
            * XGROUP CREATE log-stream logs-group $
            * It requires stream to be present before. You can create stream in redis-cli using below command
            * XADD log-stream * log 123 [XADD stream-name entry-id key value]
         */

        executor.shutdown();
        executor.awaitTermination(Long.MAX_VALUE, TimeUnit.DAYS);
    }
}
