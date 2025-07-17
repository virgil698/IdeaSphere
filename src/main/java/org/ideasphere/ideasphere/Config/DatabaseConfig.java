package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public class DatabaseConfig implements ConfigChecker {
    private static final ILogger logger = new Log4j2Logger(DatabaseConfig.class);

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
}