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
        dbProperties.setProperty("dbType", dbType);

        if ("sqlite".equalsIgnoreCase(dbType)) {
            String sqliteFile = configChecker.readConfigProperty(dbConfigPath, "db.sqlite.file");
            if (sqliteFile == null || sqliteFile.trim().isEmpty()) {
                logger.error("config", "Missing required SQLite database configuration: db.sqlite.file");
                return;
            }
            dbProperties.setProperty("dbFile", sqliteFile); // 确保 dbFile 是有效的
        } else {
            // 其他数据库类型的逻辑保持不变
        }

        database = new GenericDatabase(dbType);
        try {
            database.connect(dbProperties);
            logger.info("database", "Connected to database.");
        } catch (Exception e) {
            logger.error("database", "Error initializing database", e);
            System.exit(1);
        }
    }

    public void close() throws SQLException {
        if (database != null) {
            database.close();
        }
    }
}