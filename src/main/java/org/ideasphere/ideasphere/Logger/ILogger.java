package org.ideasphere.ideasphere.Logger;

public interface ILogger {
    void info(String message);
    void info(String format, Object... args);
    void error(String message, Throwable t);
    void warn(String message); // 新增警告日志方法
    void warn(String format, Object... args); // 新增警告日志方法，支持格式化字符串
    void debug(String message); // 新增调试日志方法
    void debug(String format, Object... args); // 新增调试日志方法，支持格式化字符串
}