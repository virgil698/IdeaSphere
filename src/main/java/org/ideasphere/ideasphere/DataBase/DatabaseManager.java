package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Config.DatabaseConfig;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.SQLException;

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

        String dbType = configChecker.readConfigProperty(dbConfigPath, "db.type");
        String dbUrl = configChecker.readConfigProperty(dbConfigPath, "db." + dbType + ".url");
        String dbUsername = configChecker.readConfigProperty(dbConfigPath, "db." + dbType + ".username");
        String dbPassword = configChecker.readConfigProperty(dbConfigPath, "db." + dbType + ".password");

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
                    break;
                default:
                    throw new SQLException("Unsupported database type: " + dbType);
            }

            database.connect(dbUrl, dbUsername, dbPassword);
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
}