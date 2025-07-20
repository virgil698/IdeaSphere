package org.ideasphere.ideasphere.Config;

public interface Config {
    void initialize();
    void loadProperties();
    String getProperty(String key);
    void setProperty(String key, String value); // 添加设置属性的方法
}