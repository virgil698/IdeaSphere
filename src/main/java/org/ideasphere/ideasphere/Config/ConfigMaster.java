package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.*;
import java.util.Properties;

public class ConfigMaster implements Config {
    private static ConfigMaster instance;
    private ConfigReading configReading = ConfigReading.getInstance();
    private static final String CONFIG_PROPERTIES_PATH = "config/config.properties";
    private static final String DATABASE_PROPERTIES_PATH = "config/database.properties";
    private final ILogger logger = new Log4j2Logger(this.getClass()); // 日志记录工具

    private ConfigMaster() {
        // 私有构造函数，确保单例
    }

    public static synchronized ConfigMaster getInstance() {
        if (instance == null) {
            instance = new ConfigMaster();
        }
        return instance;
    }

    @Override
    public void initialize() {
        try {
            // 初始化配置文件
            ConfigInitialize.initialize();
            logger.info("Config", "Configuration files initialized");

            // 加载配置文件
            loadProperties();
            logger.info("Config", "Configuration files loaded");

            // 验证配置
            validateConfig();
            logger.info("Config", "Configuration validated");
        } catch (Exception e) {
            logger.error("Config", "Failed to initialize configuration", e);
        }
    }

    @Override
    public void loadProperties() {
        configReading.loadConfigProperties();
        configReading.loadDatabaseProperties();
        logger.info("Config", "Configuration properties loaded");
    }

    @Override
    public String getProperty(String key) {
        // 先尝试从config.properties获取
        String value = configReading.getConfigProperty(key);

        // 如果没有找到，再尝试从database.properties获取
        if (value == null) {
            value = configReading.getDatabaseProperty(key);
        }

        return value;
    }

    @Override
    public void setProperty(String key, String value) {
        Properties properties = new Properties();
        try (FileInputStream fis = new FileInputStream(getPropertyPath(key))) {
            properties.load(fis);

            // 更新属性值
            properties.setProperty(key, value);

            // 写回文件
            try (FileOutputStream fos = new FileOutputStream(getPropertyPath(key))) {
                properties.store(fos, null);
                logger.info("Config", "Updated configuration property: %s=%s", key, value);
            }
        } catch (IOException e) {
            logger.error("Config", "Failed to update configuration property: %s", e);
        }
    }

    private String getPropertyPath(String key) {
        // 根据配置项的前缀确定文件路径
        if (key.startsWith("db.")) {
            return DATABASE_PROPERTIES_PATH;
        } else {
            return CONFIG_PROPERTIES_PATH;
        }
    }

    private void validateConfig() {
        // 验证config.properties中的关键配置
        String serverPort = configReading.getConfigProperty("server.port");
        if (serverPort == null) {
            logger.error("Config", "Missing required configuration: server.port");
            throw new IllegalStateException("Missing required configuration: server.port");
        }

        String appName = configReading.getConfigProperty("spring.application.name");
        if (appName == null) {
            logger.error("Config", "Missing required configuration: spring.application.name");
            throw new IllegalStateException("Missing required configuration: spring.application.name");
        }

        // 验证database.properties中的关键配置
        String dbType = configReading.getDatabaseProperty("db.type");
        if (dbType == null) {
            logger.error("Config", "Missing required configuration: db.type");
            throw new IllegalStateException("Missing required configuration: db.type");
        }

        String dbFile = configReading.getDatabaseProperty("db.sqlite.file");
        if (dbType.equals("sqlite") && dbFile == null) {
            logger.error("Config", "Missing required configuration: db.sqlite.file for db.type=sqlite");
            throw new IllegalStateException("Missing required configuration: db.sqlite.file for db.type=sqlite");
        }
    }

    public static void main(String[] args) {
        ConfigMaster configMaster = ConfigMaster.getInstance();
        configMaster.initialize();

        // 测试读取配置
        System.out.println("server.port: " + configMaster.getProperty("server.port"));
        System.out.println("db.type: " + configMaster.getProperty("db.type"));
        System.out.println("application.timezone: " + configMaster.getProperty("application.timezone"));
        System.out.println("db.sqlite.file: " + configMaster.getProperty("db.sqlite.file"));

        // 测试修改配置
        configMaster.setProperty("db.initialized", "true");
        System.out.println("Modified db.initialized: " + configMaster.getProperty("db.initialized"));
    }
}