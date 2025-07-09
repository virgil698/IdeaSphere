package org.ideasphere.ideasphere.Logger;

public interface ILogger {
    void info(String message);
    void info(String format, Object... args);
    void error(String message);
    void error(String message, Throwable t);
    void warn(String message);
    void warn(String format, Object... args);
    void debug(String message);
    void debug(String format, Object... args);

    // 新增带方法类型标识的日志方法
    void info(String methodType, String message);
    void info(String methodType, String format, Object... args);
    void error(String methodType, String message);
    void error(String methodType, String message, Throwable t);
    void warn(String methodType, String message);
    void warn(String methodType, String format, Object... args);
    void debug(String methodType, String message);
    void debug(String methodType, String format, Object... args);
}