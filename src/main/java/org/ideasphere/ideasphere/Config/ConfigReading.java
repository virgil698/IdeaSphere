package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class ConfigReading {
    private Properties configProperties = new Properties();
    private Properties databaseProperties = new Properties();
    private static ConfigReading instance;
    private static final ILogger logger = new Log4j2Logger(ConfigReading.class);

    private ConfigReading() {
        // 私有构造函数，确保单例
    }

    public static synchronized ConfigReading getInstance() {
        if (instance == null) {
            instance = new ConfigReading();
        }
        return instance;
    }

    public void loadConfigProperties() {
        File configPropertiesFile = new File("config/config.properties");
        if (configPropertiesFile.exists()) {
            try (FileInputStream fis = new FileInputStream(configPropertiesFile)) {
                configProperties.load(fis);
                logger.info("Config", "Loaded config.properties");
            } catch (IOException e) {
                logger.error("Config", "Failed to load config.properties", e);
            }
        }
    }

    public void loadDatabaseProperties() {
        File databasePropertiesFile = new File("config/database.properties");
        if (databasePropertiesFile.exists()) {
            try (FileInputStream fis = new FileInputStream(databasePropertiesFile)) {
                databaseProperties.load(fis);
                logger.info("Config", "Loaded database.properties");
            } catch (IOException e) {
                logger.error("Config", "Failed to load database.properties", e);
            }
        }
    }

    public String getConfigProperty(String key) {
        return configProperties.getProperty(key);
    }

    public String getDatabaseProperty(String key) {
        return databaseProperties.getProperty(key);
    }
}