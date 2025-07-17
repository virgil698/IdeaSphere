package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.File;
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
    }

    // 检查配置文件内容
    public static void checkConfigFilesContent(String configDirPath) {
        ConfigChecker checker = new ConfigCheckerImpl();

        // 检查数据库配置文件内容
        Path dbConfigPath = Paths.get(configDirPath, "database.properties");
        checker.checkConfigFileContent(dbConfigPath);

        // 检查应用配置文件内容
        Path appConfigPath = Paths.get(configDirPath, "config.properties");
        checker.checkConfigFileContent(appConfigPath);
    }
}