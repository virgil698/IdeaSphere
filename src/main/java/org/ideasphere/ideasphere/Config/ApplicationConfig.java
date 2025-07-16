package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.nio.charset.StandardCharsets;   // 新增
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;

public class ApplicationConfig implements ConfigChecker {
    private static final ILogger logger = new Log4j2Logger(ApplicationConfig.class);

    @Override
    public boolean checkAndCreateConfigFile(Path configFilePath, String content) {
        if (!Files.exists(configFilePath)) {
            try {
                // 明确指定 UTF-8 编码
                Files.write(configFilePath, content.getBytes(StandardCharsets.UTF_8));
                return true;
            } catch (IOException e) {
                logger.error("Error creating application config file: " + configFilePath, e);
            }
        }
        return false;
    }

    public static void createApplicationConfigFile(String configDirPath) {
        String fileName = "application.properties";
        String content = "# 网站释放端口\n" +
                "server.port=8080\n" +
                "# 站点名称\n" +
                "spring.application.name=IdeaSphere\n" +
                "# 服务时区\n" +
                "application.timezone=UTC\n" +
                "# DEBUG模式\n" +
                "debug.mode=false";

        Path configFilePath = Paths.get(configDirPath, fileName);
        ConfigChecker checker = new ApplicationConfig();
        if (checker.checkAndCreateConfigFile(configFilePath, content)) {
            logger.info("config", "Created application config file: " + configFilePath);
        } else {
            logger.info("config", "Application config file already exists: " + configFilePath);
        }
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
                props.load(inputStream); // 读取时默认 ISO-8859-1
            }
        } catch (IOException e) {
            logger.error("Error reading config file: " + configFilePath, e);
        }
        return props.getProperty(key);
    }
}