package org.ideasphere.ideasphere.Logger;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Log4j2Logger implements ILogger {
    private final Logger logger;

    public Log4j2Logger(Class<?> clazz) {
        this.logger = LogManager.getLogger(clazz);
    }

    @Override
    public void info(String message) {
        logger.info(message);
    }

    @Override
    public void info(String format, Object... args) {
        String formattedMessage = String.format(format, args);
        logger.info(formattedMessage);
    }

    @Override
    public void error(String message) {
        logger.error(message);
    }

    @Override
    public void error(String message, Throwable t) {
        logger.error(message, t);
    }

    @Override
    public void warn(String message) {
        logger.warn(message);
    }

    @Override
    public void warn(String format, Object... args) {
        String formattedMessage = String.format(format, args);
        logger.warn(formattedMessage);
    }

    @Override
    public void debug(String message) {
        logger.debug(message);
    }

    @Override
    public void debug(String format, Object... args) {
        String formattedMessage = String.format(format, args);
        logger.debug(formattedMessage);
    }

    // 实现带方法类型标识的日志方法
    @Override
    public void info(String methodType, String message) {
        String formattedMessage = String.format("[%s] %s", methodType, message);
        logger.info(formattedMessage);
    }

    @Override
    public void info(String methodType, String format, Object... args) {
        String combinedFormat = String.format("[%s] %s", methodType, format);
        String formattedMessage = String.format(combinedFormat, args);
        logger.info(formattedMessage);
    }

    @Override
    public void error(String methodType, String message) {
        String formattedMessage = String.format("[%s] %s", methodType, message);
        logger.error(formattedMessage);
    }

    @Override
    public void error(String methodType, String message, Throwable t) {
        String formattedMessage = String.format("[%s] %s", methodType, message);
        logger.error(formattedMessage, t);
    }

    @Override
    public void warn(String methodType, String message) {
        String formattedMessage = String.format("[%s] %s", methodType, message);
        logger.warn(formattedMessage);
    }

    @Override
    public void warn(String methodType, String format, Object... args) {
        String combinedFormat = String.format("[%s] %s", methodType, format);
        String formattedMessage = String.format(combinedFormat, args);
        logger.warn(formattedMessage);
    }

    @Override
    public void debug(String methodType, String message) {
        String formattedMessage = String.format("[%s] %s", methodType, message);
        logger.debug(formattedMessage);
    }

    @Override
    public void debug(String methodType, String format, Object... args) {
        String combinedFormat = String.format("[%s] %s", methodType, format);
        String formattedMessage = String.format(combinedFormat, args);
        logger.debug(formattedMessage);
    }
}