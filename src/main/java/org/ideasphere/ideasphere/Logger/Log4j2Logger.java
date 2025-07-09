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
        logger.info(String.format(format, args));
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
        logger.warn(String.format(format, args));
    }

    @Override
    public void debug(String message) {
        logger.debug(message);
    }

    @Override
    public void debug(String format, Object... args) {
        logger.debug(String.format(format, args));
    }

    // 实现带方法类型标识的日志方法
    @Override
    public void info(String methodType, String message) {
        logger.info(String.format("%s: %s", methodType, message));
    }

    @Override
    public void info(String methodType, String format, Object... args) {
        String combinedFormat = methodType + ": " + format;
        logger.info(String.format(combinedFormat, args));
    }

    @Override
    public void error(String methodType, String message) {
        logger.error(String.format("%s: %s", methodType, message));
    }

    @Override
    public void error(String methodType, String message, Throwable t) {
        logger.error(String.format("%s: %s", methodType, message), t);
    }

    @Override
    public void warn(String methodType, String message) {
        logger.warn(String.format("%s: %s", methodType, message));
    }

    @Override
    public void warn(String methodType, String format, Object... args) {
        String combinedFormat = methodType + ": " + format;
        logger.warn(String.format(combinedFormat, args));
    }

    @Override
    public void debug(String methodType, String message) {
        logger.debug(String.format("%s: %s", methodType, message));
    }

    @Override
    public void debug(String methodType, String format, Object... args) {
        String combinedFormat = methodType + ": " + format;
        logger.debug(String.format(combinedFormat, args));
    }
}