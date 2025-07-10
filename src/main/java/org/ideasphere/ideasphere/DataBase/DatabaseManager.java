package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Config.DatabaseConfig;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.util.Properties;

public class DatabaseManager {
    private Database database;
    private String configDirPath;

    public DatabaseManager(String configDirPath) {
        this.configDirPath = configDirPath;
        initializeDatabase();
    }

    private void initializeDatabase() {
        Path dbConfigPath = Paths.get(configDirPath, "db_config.properties");
        DatabaseConfig configChecker = new DatabaseConfig();
        Properties dbProperties = new Properties();

        String dbType = configChecker.readConfigProperty(dbConfigPath, "db.type");
        dbProperties.setProperty("url", configChecker.readConfigProperty(dbConfigPath, "db." + dbType + ".url"));
        dbProperties.setProperty("username", configChecker.readConfigProperty(dbConfigPath, "db." + dbType + ".username"));
        dbProperties.setProperty("password", configChecker.readConfigProperty(dbConfigPath, "db." + dbType + ".password"));

        try {
            switch (dbType) {
                case "mysql":
                    database = new MySQLDatabase();
                    break;
                case "mariadb":
                    database = new MariaDBDatabase();
                    break;
                case "postgresql":
                    database = new PostgreSQLDatabase();
                    break;
                case "sqlite":
                    database = new SQLiteDatabase();
                    // SQLite 的配置处理
                    String dbFile = configChecker.readConfigProperty(dbConfigPath, "db." + dbType + ".file");
                    dbProperties.setProperty("dbFile", dbFile);
                    break;
                default:
                    throw new SQLException("Unsupported database type: " + dbType);
            }

            database.connect(dbProperties);
            database.initialize();
        } catch (Exception e) {
            System.err.println("Error initializing database: " + e.getMessage());
        }
    }

    public <T> T query(String sql, RowMapper<T> rowMapper) throws SQLException {
        return database.query(sql, rowMapper);
    }

    public void close() throws SQLException {
        if (database != null) {
            database.close();
        }
    }

    public String getDbType() {
        return database.getDbType();
    }
}