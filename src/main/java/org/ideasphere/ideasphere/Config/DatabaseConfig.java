package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public class DatabaseConfig implements ConfigChecker {
    private final ILogger logger = new Log4j2Logger(DatabaseConfig.class); // 日志记录工具

    @Override
    public boolean checkAndCreateConfigFile(Path configFilePath, String content) {
        throw new UnsupportedOperationException("This method is no longer supported");
    }

    @Override
    public void checkConfigFileContent(Path configFilePath) {
        // 实现检查配置文件内容的逻辑
    }

    @Override
    public String readConfigProperty(Path configFilePath, String key) {
        Properties props = new Properties();
        try (InputStream inputStream = Files.newInputStream(configFilePath)) {
            if (Files.exists(configFilePath)) {
                props.load(inputStream);
            }
        } catch (IOException e) {
            logger.error("Error reading config file: " + configFilePath, e);
        }
        return props.getProperty(key);
    }

    public void setConfigProperty(Path configFilePath, String key, String value) {
        Properties props = new Properties();
        try (InputStream inputStream = Files.newInputStream(configFilePath)) {
            if (Files.exists(configFilePath)) {
                props.load(inputStream);
            }
            props.setProperty(key, value);
            try (OutputStream outputStream = Files.newOutputStream(configFilePath)) {
                props.store(outputStream, null);
            }
        } catch (IOException e) {
            logger.error("Error writing to config file: " + configFilePath, e);
        }
    }
}