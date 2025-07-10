package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Config.DatabaseConfig;
import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.util.Properties;

public class DatabaseManager {
    private Database database;
    private String configDirPath;
    private ILogger logger;

    public DatabaseManager(String configDirPath) {
        this.configDirPath = configDirPath;
        this.logger = new Log4j2Logger(DatabaseManager.class);
        initializeDatabase();
    }

    public void initializeDatabase() {
        Path dbConfigPath = Paths.get(configDirPath, "config", "db_config.properties");
        DatabaseConfig configChecker = new DatabaseConfig();

        // 检查配置文件是否存在
        if (!Files.exists(dbConfigPath)) {
            logger.warn("config", "Database configuration file not found: " + dbConfigPath);
            logger.warn("config", "Database will not be initialized.");
            return;
        }

        logger.info("config", "Database configuration file found: " + dbConfigPath);

        Properties dbProperties = new Properties();

        String dbType = configChecker.readConfigProperty(dbConfigPath, "db.type");
        if (dbType == null || dbType.isEmpty()) {
            logger.error("config", "Database type must be specified in configuration file.");
            return;
        }

        // 设置数据库通用属性
        dbProperties.setProperty("dbType", dbType);

        // 读取通用数据库配置
        String host = configChecker.readConfigProperty(dbConfigPath, "db.host");
        String port = configChecker.readConfigProperty(dbConfigPath, "db.port");
        String name = configChecker.readConfigProperty(dbConfigPath, "db.name");
        String username = configChecker.readConfigProperty(dbConfigPath, "db.username");
        String password = configChecker.readConfigProperty(dbConfigPath, "db.password");

        // 读取 SQLite 特定配置
        String sqliteFile = configChecker.readConfigProperty(dbConfigPath, "db.sqlite.file");

        // 验证配置值
        if ("sqlite".equalsIgnoreCase(dbType)) {
            if (sqliteFile == null || sqliteFile.isEmpty()) {
                logger.error("config", "Missing required SQLite database configuration: db.sqlite.file");
                return;
            }
            dbProperties.setProperty("dbFile", sqliteFile);
        } else {
            if (host == null || port == null || name == null || username == null || password == null) {
                logger.error("config", "Missing required database configuration for type: " + dbType);
                return;
            }
            dbProperties.setProperty("host", host);
            dbProperties.setProperty("port", port);
            dbProperties.setProperty("name", name);
            dbProperties.setProperty("username", username);
            dbProperties.setProperty("password", password);
        }

        database = new GenericDatabase(dbType);

        try {
            database.connect(dbProperties);
            logger.info("database", "Connected to database.");
        } catch (Exception e) {
            logger.error("database", "Error initializing database", e);
            // 打印详细的堆栈信息
            e.printStackTrace();
            // 终止进程
            System.exit(1);
        }
    }

    public void close() throws SQLException {
        if (database != null) {
            database.close();
        }
    }
}