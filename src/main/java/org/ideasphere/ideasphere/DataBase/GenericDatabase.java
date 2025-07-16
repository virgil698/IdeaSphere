package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.*;
import java.nio.file.*;
import java.sql.*;
import java.util.Properties;

public class GenericDatabase implements Database {
    private Connection connection;
    private String dbType;
    private static final ILogger logger = new Log4j2Logger(GenericDatabase.class);

    public GenericDatabase(String dbType) {
        this.dbType = dbType;
    }

    public void connect(Properties dbProperties) throws SQLException {
        String url;
        String username = dbProperties.getProperty("username");
        String password = dbProperties.getProperty("password");

        if ("sqlite".equalsIgnoreCase(dbType)) {
            try {
                Class.forName("org.sqlite.JDBC");
                logger.info("database", "Loaded SQLite JDBC driver.");
            } catch (ClassNotFoundException e) {
                logger.error("database", "SQLite JDBC driver not found.", e);
                throw new SQLException("SQLite JDBC driver not found.", e);
            }

            String dbFile = dbProperties.getProperty("dbFile");
            if (dbFile == null || dbFile.trim().isEmpty()) { // 检查 dbFile 是否为空
                throw new SQLException("SQLite database file must be specified.");
            }

            Path dbFilePath = Paths.get(dbFile);
            if (!Files.exists(dbFilePath)) {
                try {
                    // 确保父目录存在
                    if (dbFilePath.getParent() != null && !Files.exists(dbFilePath.getParent())) {
                        Files.createDirectories(dbFilePath.getParent()); // 创建父目录
                    }
                    Files.createFile(dbFilePath); // 创建文件
                    logger.info("database", "Created SQLite database file: " + dbFilePath);
                } catch (IOException e) {
                    logger.error("database", "Failed to create SQLite database file: " + dbFilePath, e);
                    throw new SQLException("Failed to create SQLite database file: " + dbFilePath, e);
                }
            }
            url = "jdbc:sqlite:" + dbFile;
        } else if ("mysql".equalsIgnoreCase(dbType)) {
            try {
                Class.forName("com.mysql.cj.jdbc.Driver");
                logger.info("database", "Loaded MySQL JDBC driver.");
            } catch (ClassNotFoundException e) {
                logger.error("database", "MySQL JDBC driver not found.", e);
                throw new SQLException("MySQL JDBC driver not found.", e);
            }
            String host = dbProperties.getProperty("host");
            String port = dbProperties.getProperty("port");
            String name = dbProperties.getProperty("name");
            if (host == null || port == null || name == null) {
                throw new SQLException("Database connection details must be specified.");
            }
            url = "jdbc:" + dbType + "://" + host + ":" + port + "/" + name;
        } else if ("mariadb".equalsIgnoreCase(dbType)) {
            try {
                Class.forName("org.mariadb.jdbc.Driver");
                logger.info("database", "Loaded MariaDB JDBC driver.");
            } catch (ClassNotFoundException e) {
                logger.error("database", "MariaDB JDBC driver not found.", e);
                throw new SQLException("MariaDB JDBC driver not found.", e);
            }
            String host = dbProperties.getProperty("host");
            String port = dbProperties.getProperty("port");
            String name = dbProperties.getProperty("name");
            if (host == null || port == null || name == null) {
                throw new SQLException("Database connection details must be specified.");
            }
            url = "jdbc:" + dbType + "://" + host + ":" + port + "/" + name;
        } else if ("postgresql".equalsIgnoreCase(dbType)) {
            try {
                Class.forName("org.postgresql.Driver");
                logger.info("database", "Loaded PostgreSQL JDBC driver.");
            } catch (ClassNotFoundException e) {
                logger.error("database", "PostgreSQL JDBC driver not found.", e);
                throw new SQLException("PostgreSQL JDBC driver not found.", e);
            }
            String host = dbProperties.getProperty("host");
            String port = dbProperties.getProperty("port");
            String name = dbProperties.getProperty("name");
            if (host == null || port == null || name == null) {
                throw new SQLException("Database connection details must be specified.");
            }
            url = "jdbc:" + dbType + "://" + host + ":" + port + "/" + name;
        } else {
            throw new SQLException("Unsupported database type: " + dbType);
        }

        try {
            connection = DriverManager.getConnection(url, username, password);
            logger.info("database", "Connected to database.");
        } catch (SQLException e) {
            logger.error("database", "Error connecting to database.", e);
            throw e;
        }
    }

    private String loadSqlScript(String filePath) throws IOException {
        StringBuilder sqlScript = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                sqlScript.append(line).append(" ");
            }
        }
        return sqlScript.toString();
    }

    @Override
    public void initialize() throws Exception {
        String sqlFilePath;
        switch (dbType.toLowerCase()) {
            case "mariadb":
                sqlFilePath = "src/main/java/org/ideasphere/ideasphere/DataBase/SQL/mariadb.sql";
                break;
            case "mysql":
                sqlFilePath = "src/main/java/org/ideasphere/ideasphere/DataBase/SQL/mysql.sql";
                break;
            case "postgresql":
                sqlFilePath = "src/main/java/org/ideasphere/ideasphere/DataBase/SQL/postgresql.sql";
                break;
            case "sqlite":
                sqlFilePath = "src/main/java/org/ideasphere/ideasphere/DataBase/SQL/sqlite.sql";
                break;
            default:
                throw new IllegalArgumentException("Unsupported database type: " + dbType);
        }

        String sqlScript = loadSqlScript(sqlFilePath);

        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sqlScript);
        }
    }

    @Override
    public <T> T query(String sql, RowMapper<T> rowMapper) throws SQLException {
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            if (rs.next()) {
                return rowMapper.mapRow(rs, dbType.toLowerCase());
            }
            return null;
        }
    }

    @Override
    public int update(String sql) throws SQLException {
        try (Statement stmt = connection.createStatement()) {
            return stmt.executeUpdate(sql);
        }
    }

    @Override
    public int delete(String sql) throws SQLException {
        return update(sql);
    }

    @Override
    public void close() throws SQLException {
        if (connection != null && !connection.isClosed()) {
            connection.close();
        }
    }

    @Override
    public String getDbType() {
        return dbType;
    }
}