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
        // 检查文件是否存在
        if (!Files.exists(configFilePath)) {
            try {
                // 创建文件并写入内容
                Files.write(configFilePath, content.getBytes());
                return true;
            } catch (IOException e) {
                logger.error("Error creating config file: " + configFilePath);
                return false;
            }
        }
        return false;
    }

    @Override
    public void checkConfigFileContent(Path configFilePath) {
        try {
            // 读取配置文件内容
            Properties props = new Properties();
            props.load(Files.newInputStream(configFilePath));

            // 检查数据库配置文件
            if (configFilePath.toString().endsWith("db_config.properties")) {
                checkDatabaseConfig(props, configFilePath);
            }
            // 检查应用配置文件
            else if (configFilePath.toString().endsWith("application.properties")) {
                checkApplicationConfig(props, configFilePath);
            }
        } catch (IOException e) {
            logger.error("Error reading config file: " + configFilePath, e);
        }
    }

    // 检查数据库配置文件内容
    private void checkDatabaseConfig(Properties props, Path configFilePath) {
        // 检查 db.type 是否在支持的数据库类型中
        String dbType = props.getProperty("db.type");
        if (!dbType.toLowerCase().equals("mysql") && !dbType.toLowerCase().equals("mariadb") &&
                !dbType.toLowerCase().equals("postgresql") && !dbType.toLowerCase().equals("sqlite")) {
            logger.error("Invalid database type: " + dbType + " in config file: " + configFilePath);
        }

        // 检查对应数据库的连接配置是否存在
        if (dbType.toLowerCase().equals("mysql")) {
            checkPropertyExists(props, configFilePath, "db.mysql.url");
            checkPropertyExists(props, configFilePath, "db.mysql.username");
            checkPropertyExists(props, configFilePath, "db.mysql.password");
        } else if (dbType.toLowerCase().equals("mariadb")) {
            checkPropertyExists(props, configFilePath, "db.mariadb.url");
            checkPropertyExists(props, configFilePath, "db.mariadb.username");
            checkPropertyExists(props, configFilePath, "db.mariadb.password");
        } else if (dbType.toLowerCase().equals("postgresql")) {
            checkPropertyExists(props, configFilePath, "db.postgresql.url");
            checkPropertyExists(props, configFilePath, "db.postgresql.username");
            checkPropertyExists(props, configFilePath, "db.postgresql.password");
        } else if (dbType.toLowerCase().equals("sqlite")) {
            checkPropertyExists(props, configFilePath, "db.sqlite.url");
        }
    }

    // 检查应用配置文件内容
    private void checkApplicationConfig(Properties props, Path configFilePath) {
        // 检查 server.port 是否是有效的数字
        String serverPort = props.getProperty("server.port");
        try {
            int port = Integer.parseInt(serverPort);
            if (port < 1 || port > 65535) {
                logger.error("Invalid port number: " + port + " in config file: " + configFilePath);
            }
        } catch (NumberFormatException e) {
            logger.error("Invalid port format: " + serverPort + " in config file: " + configFilePath, e);
        }

        // 检查 spring.application.name 是否为空
        String appName = props.getProperty("spring.application.name");
        if (appName == null || appName.isEmpty()) {
            logger.error("Application name is empty in config file: " + configFilePath);
        }

        // 检查 application.timezone 是否是有效的时区
        String timezone = props.getProperty("application.timezone");
        if (timezone == null || timezone.isEmpty()) {
            logger.error("Timezone is empty in config file: " + configFilePath);
        }

        // 检查 debug.mode 是否是布尔值
        String debugMode = props.getProperty("debug.mode");
        if (!debugMode.toLowerCase().equals("true") && !debugMode.toLowerCase().equals("false")) {
            logger.error("Invalid debug mode: " + debugMode + " in config file: " + configFilePath);
        }
    }

    // 检查属性是否存在
    private void checkPropertyExists(Properties props, Path configFilePath, String key) {
        if (props.getProperty(key) == null || props.getProperty(key).isEmpty()) {
            logger.error("Missing property: " + key + " in config file: " + configFilePath);
        }
    }
}