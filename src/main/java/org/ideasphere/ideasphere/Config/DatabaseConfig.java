package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.nio.charset.StandardCharsets;   // 新增
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;

public class DatabaseConfig implements ConfigChecker {
    private static final ILogger logger = new Log4j2Logger(DatabaseConfig.class);

    @Override
    public boolean checkAndCreateConfigFile(Path configFilePath, String content) {
        if (!Files.exists(configFilePath)) {
            try {
                // 明确指定 UTF-8 编码
                Files.write(configFilePath, content.getBytes(StandardCharsets.UTF_8));
                return true;
            } catch (IOException e) {
                logger.error("Error creating database config file: " + configFilePath, e);
            }
        }
        return false;
    }

    public static void createDatabaseConfigFile(String configDirPath) {
        String fileName = "db_config.properties";
        String content = "# 数据库类型，可选：mysql、mariadb、postgresql或者sqlite\n" +
                "db.type=mysql\n" +
                "# 数据库连接配置\n" +
                "# MySQL、MariaDB、PostgreSQL通用配置\n" +
                "db.host=localhost\n" +
                "db.port=3306\n" +
                "db.name=ideasphere\n" +
                "db.username=root\n" +
                "db.password=root\n" +
                "# SQLite配置\n" +
                "db.sqlite.file=ideasphere.db\n" +
                "# 数据库是否已初始化\n" +
                "db.initialized=false\n";

        Path configFilePath = Paths.get(configDirPath, fileName);
        ConfigChecker checker = new DatabaseConfig();
        if (checker.checkAndCreateConfigFile(configFilePath, content)) {
            logger.info("config", "Created database config file: " + configFilePath);
        } else {
            logger.info("config", "Database config file already exists: " + configFilePath);
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
                props.load(inputStream);
            }
        } catch (IOException e) {
            logger.error("Error reading config file: " + configFilePath, e);
        }
        return props.getProperty(key);
    }
}