package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Properties;

public class ApplicationConfig implements ConfigChecker {
    private static final ILogger logger = new Log4j2Logger(ApplicationConfig.class);

    @Override
    public boolean checkAndCreateConfigFile(Path configFilePath, String content) {
        throw new UnsupportedOperationException("This method is no longer supported");
    }

    @Override
    public void checkConfigFileContent(Path configFilePath) {
        ConfigCheckerImpl checker = new ConfigCheckerImpl();
        checker.checkConfigFileContent(configFilePath);
    }

    @Override
    public String readConfigProperty(Path configFilePath, String key) {
        Properties props = new Properties();
        try (var inputStream = Files.newInputStream(configFilePath)) {
            if (Files.exists(configFilePath)) {
                props.load(inputStream);
            }
        } catch (IOException e) {
            logger.error("Error reading config file: " + configFilePath, e);
        }
        return props.getProperty(key);
    }

    public static void copyConfigFilesIfNeeded(String projectMainDirPath) {
        String configDirPath = Paths.get(projectMainDirPath, "config").toString();
        Path targetConfigDir = Paths.get(projectMainDirPath, "config");

        // 检查目标配置目录是否存在
        if (!Files.exists(targetConfigDir)) {
            try {
                // 创建目标目录
                Files.createDirectories(targetConfigDir);

                // 拷贝 config.properties
                Path sourceConfig = Paths.get("src", "main", "resources", "config", "config.properties");
                Path targetConfig = Paths.get(configDirPath, "config.properties");
                copyFile(sourceConfig, targetConfig);

                // 拷贝 database.properties
                Path sourceDatabase = Paths.get("src", "main", "resources", "config", "database.properties");
                Path targetDatabase = Paths.get(configDirPath, "database.properties");
                copyFile(sourceDatabase, targetDatabase);

                logger.info("config", "Successfully copied config files to: " + configDirPath);
            } catch (Exception e) {
                logger.error("config", "Failed to copy config files to: " + configDirPath, e);
            }
        } else {
            logger.info("config", "Config directory already exists: " + targetConfigDir);
        }
    }

    private static void copyFile(Path sourcePath, Path targetPath) throws IOException {
        Files.copy(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
    }
}