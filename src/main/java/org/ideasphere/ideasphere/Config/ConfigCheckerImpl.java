package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public class ConfigCheckerImpl implements ConfigChecker {
    private static final ILogger logger = new Log4j2Logger(ConfigCheckerImpl.class);

    @Override
    public boolean checkAndCreateConfigFile(Path configFilePath, String content) {
        if (!Files.exists(configFilePath)) {
            try {
                Files.write(configFilePath, content.getBytes());
                return true;
            } catch (IOException e) {
                logger.error("Error creating config file: " + configFilePath, e);
                return false;
            }
        }
        return false;
    }

    @Override
    public void checkConfigFileContent(Path configFilePath) {
        try {
            Properties props = new Properties();
            props.load(Files.newInputStream(configFilePath));

            if (configFilePath.toString().endsWith("db_config.properties")) {
                checkDatabaseConfig(props, configFilePath);
            } else if (configFilePath.toString().endsWith("application.properties")) {
                checkApplicationConfig(props, configFilePath);
            }
        } catch (IOException e) {
            logger.error("Error reading config file: " + configFilePath, e);
        }
    }

    private void checkDatabaseConfig(Properties props, Path configFilePath) {
        String dbType = props.getProperty("db.type");
        if (dbType == null || dbType.isEmpty()) {
            logger.error("Missing property: db.type in config file: " + configFilePath);
            return;
        }

        if (!dbType.toLowerCase().equals("mysql") && !dbType.toLowerCase().equals("mariadb") &&
                !dbType.toLowerCase().equals("postgresql") && !dbType.toLowerCase().equals("sqlite")) {
            logger.error("Invalid database type: " + dbType + " in config file: " + configFilePath);
            return;
        }

        if (dbType.toLowerCase().equals("mysql") || dbType.toLowerCase().equals("mariadb") || dbType.toLowerCase().equals("postgresql")) {
            checkPropertyExists(props, configFilePath, "db.host");
            checkPropertyExists(props, configFilePath, "db.port");
            checkPropertyExists(props, configFilePath, "db.name");
            checkPropertyExists(props, configFilePath, "db.username");
            checkPropertyExists(props, configFilePath, "db.password");
        } else if (dbType.toLowerCase().equals("sqlite")) {
            checkPropertyExists(props, configFilePath, "db.sqlite.file");
        }

        String dbInitialized = props.getProperty("db.initialized");
        if (dbInitialized == null || dbInitialized.isEmpty()) {
            logger.error("Missing property: db.initialized in config file: " + configFilePath);
        } else {
            if (!dbInitialized.toLowerCase().equals("true") && !dbInitialized.toLowerCase().equals("false")) {
                logger.error("Invalid value for db.initialized: " + dbInitialized + " in config file: " + configFilePath + ". It should be either 'true' or 'false'. Unless you know what you are doing, do not modify this configuration.");
            }
        }
    }

    private void checkApplicationConfig(Properties props, Path configFilePath) {
        String serverPort = props.getProperty("server.port");
        try {
            int port = Integer.parseInt(serverPort);
            if (port < 1 || port > 65535) {
                logger.error("Invalid port number: " + port + " in config file: " + configFilePath);
            }
        } catch (NumberFormatException e) {
            logger.error("Invalid port format: " + serverPort + " in config file: " + configFilePath, e);
        }

        String appName = props.getProperty("spring.application.name");
        if (appName == null || appName.isEmpty()) {
            logger.error("Application name is empty in config file: " + configFilePath);
        }

        String timezone = props.getProperty("application.timezone");
        if (timezone == null || timezone.isEmpty()) {
            logger.error("Timezone is empty in config file: " + configFilePath);
        }

        String debugMode = props.getProperty("debug.mode");
        if (!debugMode.toLowerCase().equals("true") && !debugMode.toLowerCase().equals("false")) {
            logger.error("Invalid debug mode: " + debugMode + " in config file: " + configFilePath);
        }
    }

    private void checkPropertyExists(Properties props, Path configFilePath, String key) {
        if (props.getProperty(key) == null || props.getProperty(key).isEmpty()) {
            logger.error("Missing property: " + key + " in config file: " + configFilePath);
        }
    }

    @Override
    public String readConfigProperty(Path configFilePath, String key) {
        Properties props = new Properties();
        try (java.io.InputStream inputStream = Files.newInputStream(configFilePath)) {
            if (Files.exists(configFilePath)) {
                props.load(inputStream);
            }
        } catch (IOException e) {
            logger.error("Error reading config file: " + configFilePath, e);
        }
        return props.getProperty(key);
    }
}