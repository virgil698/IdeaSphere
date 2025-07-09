package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ApplicationConfig implements ConfigChecker {
    private static final ILogger logger = new Log4j2Logger(ApplicationConfig.class);

    @Override
    public boolean checkAndCreateConfigFile(Path configFilePath, String content) {
        // 检查文件是否存在
        if (!Files.exists(configFilePath)) {
            try {
                // 创建文件并写入内容
                Files.write(configFilePath, content.getBytes());
                return true;
            } catch (IOException e) {
                logger.error("Error creating application config file: " + configFilePath, e);
            }
        }
        return false;
    }

    // 创建应用配置文件
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
        // 实现检查配置文件内容的逻辑
        // 例如，可以调用 ConfigCheckerImpl 的实现
        ConfigCheckerImpl checker = new ConfigCheckerImpl();
        checker.checkConfigFileContent(configFilePath);
    }
}