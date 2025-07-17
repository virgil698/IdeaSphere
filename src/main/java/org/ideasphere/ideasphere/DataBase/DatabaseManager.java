package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Config.DatabaseConfig;
import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

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
        Path dbConfigPath = Paths.get(configDirPath, "config", "database.properties");
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
        } else if ("mysql".equalsIgnoreCase(dbType)) {
            String host = configChecker.readConfigProperty(dbConfigPath, "db.mysql.host");
            String port = configChecker.readConfigProperty(dbConfigPath, "db.mysql.port");
            String name = configChecker.readConfigProperty(dbConfigPath, "db.mysql.name");
            String user = configChecker.readConfigProperty(dbConfigPath, "db.mysql.user");
            String password = configChecker.readConfigProperty(dbConfigPath, "db.mysql.password");

            if (host == null || port == null || name == null || user == null || password == null) {
                logger.error("config", "Missing required MySQL database configurations.");
                return;
            }
            dbProperties.setProperty("host", host);
            dbProperties.setProperty("port", port);
            dbProperties.setProperty("name", name);
            dbProperties.setProperty("username", user);
            dbProperties.setProperty("password", password);
        } else if ("mariadb".equalsIgnoreCase(dbType)) {
            String host = configChecker.readConfigProperty(dbConfigPath, "db.mariadb.host");
            String port = configChecker.readConfigProperty(dbConfigPath, "db.mariadb.port");
            String name = configChecker.readConfigProperty(dbConfigPath, "db.mariadb.name");
            String user = configChecker.readConfigProperty(dbConfigPath, "db.mariadb.user");
            String password = configChecker.readConfigProperty(dbConfigPath, "db.mariadb.password");

            if (host == null || port == null || name == null || user == null || password == null) {
                logger.error("config", "Missing required MariaDB database configurations.");
                return;
            }
            dbProperties.setProperty("host", host);
            dbProperties.setProperty("port", port);
            dbProperties.setProperty("name", name);
            dbProperties.setProperty("username", user);
            dbProperties.setProperty("password", password);
        } else if ("postgresql".equalsIgnoreCase(dbType)) {
            String host = configChecker.readConfigProperty(dbConfigPath, "db.postgresql.host");
            String port = configChecker.readConfigProperty(dbConfigPath, "db.postgresql.port");
            String name = configChecker.readConfigProperty(dbConfigPath, "db.postgresql.name");
            String user = configChecker.readConfigProperty(dbConfigPath, "db.postgresql.user");
            String password = configChecker.readConfigProperty(dbConfigPath, "db.postgresql.password");

            if (host == null || port == null || name == null || user == null || password == null) {
                logger.error("config", "Missing required PostgreSQL database configurations.");
                return;
            }
            dbProperties.setProperty("host", host);
            dbProperties.setProperty("port", port);
            dbProperties.setProperty("name", name);
            dbProperties.setProperty("username", user);
            dbProperties.setProperty("password", password);
        } else {
            logger.error("config", "Unsupported database type: " + dbType);
            return;
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