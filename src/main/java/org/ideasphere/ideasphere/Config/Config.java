package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Config {
    private static final ILogger logger = new Log4j2Logger(Config.class);
    private static final String CONFIG_DIR_NAME = "config";

    // 检查并创建 config 文件夹
    public static void checkAndCreateConfigDir(String mainDirPath) {
        String configDirPath = Paths.get(mainDirPath, CONFIG_DIR_NAME).toString();

        File configDir = new File(configDirPath);
        if (!configDir.exists()) {
            try {
                Files.createDirectories(configDir.toPath());
                logger.info("config", "Created config directory: " + configDirPath);
            } catch (Exception e) {
                logger.error("config", "Failed to create config directory: " + configDirPath, e);
            }
        } else {
            logger.info("config", "Config directory already exists: " + configDirPath);
        }

        // 检查并创建配置文件
        checkAndCreateConfigFiles(configDirPath);
    }

    // 检查并创建配置文件
    private static void checkAndCreateConfigFiles(String configDirPath) {
        // 创建数据库配置文件
        DatabaseConfig.createDatabaseConfigFile(configDirPath);

        // 创建应用配置文件
        ApplicationConfig.createApplicationConfigFile(configDirPath);

        // 检查配置文件内容
        checkConfigFilesContent(configDirPath);
    }

    // 检查配置文件内容
    private static void checkConfigFilesContent(String configDirPath) {
        ConfigChecker checker = new ConfigCheckerImpl();

        // 检查数据库配置文件内容
        Path dbConfigPath = Paths.get(configDirPath, "db_config.properties");
        checker.checkConfigFileContent(dbConfigPath);

        // 检查应用配置文件内容
        Path appConfigPath = Paths.get(configDirPath, "application.properties");
        checker.checkConfigFileContent(appConfigPath);
    }
}