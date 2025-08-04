package com.harsha;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.UUID;

public class AppInstance {

    private static final Logger logger = LoggerFactory.getLogger(AppInstance.class);

    public void log() throws Exception {
        String logMessage = UUID.randomUUID() + "- created order with unique ID";
        while(true) {
            logger.info(logMessage);
            Thread.sleep(1000);
        }
    }
}
