package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class Config {
    private static final ILogger logger = new Log4j2Logger(Config.class);
    private static final String CONFIG_DIR_NAME = "config";

    // 模拟的配置文件内容，实际应用中可以替换为从数据库或其他来源获取的配置
    private static final Map<String, String> sampleConfigContents = new HashMap<>();

    static {
        sampleConfigContents.put("application.properties", "server.port=8080\nspring.application.name=IdeaSphere");
        sampleConfigContents.put("db_config.properties", "db.url=jdbc:mysql://localhost:3306/ideasphere\n" +
                "db.username=root\ndb.password=root");
    }

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
        for (Map.Entry<String, String> entry : sampleConfigContents.entrySet()) {
            String fileName = entry.getKey();
            String content = entry.getValue();

            Path configFilePath = Paths.get(configDirPath, fileName);
            ConfigChecker checker = new ConfigCheckerImpl();
            if (checker.checkAndCreateConfigFile(configFilePath, content)) {
                logger.info("config", "Created config file: " + configFilePath);
            } else {
                logger.info("config", "Config file already exists: " + configFilePath);
            }
        }
    }
}

// ConfigChecker 的实现类
class ConfigCheckerImpl implements ConfigChecker {

    @Override
    public boolean checkAndCreateConfigFile(Path configFilePath, String content) {
        // 检查文件是否存在
        if (!Files.exists(configFilePath)) {
            try {
                // 创建文件并写入内容
                Files.write(configFilePath, content.getBytes());
                return true;
            } catch (IOException e) {
                System.err.println("Error creating config file: " + configFilePath);
                e.printStackTrace();
            }
        }
        return false;
    }
}