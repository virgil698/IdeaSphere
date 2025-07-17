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
        Path targetConfigDir = Paths.get(projectMainDirPath, "config");

        // 检查目标配置目录是否存在
        if (!Files.exists(targetConfigDir)) {
            try {
                // 创建目标目录
                Files.createDirectories(targetConfigDir);

                // 拷贝配置文件
                copyConfigFile("config.properties", projectMainDirPath);
                copyConfigFile("database.properties", projectMainDirPath);

                logger.info("Successfully copied config files to: " + targetConfigDir.toString());
            } catch (Exception e) {
                logger.error("Failed to copy config files to: " + targetConfigDir.toString(), e);
            }
        } else {
            logger.info("Config directory already exists: " + targetConfigDir.toString());
        }
    }

    private static void copyConfigFile(String fileName, String projectMainDirPath) throws IOException {
        // 构建源文件路径（从main/resources）
        Path sourcePath = Paths.get("src", "main", "resources", fileName);

        // 构建目标文件路径
        Path targetPath = Paths.get(projectMainDirPath, "config", fileName);

        // 复制文件
        Files.copy(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
    }
}