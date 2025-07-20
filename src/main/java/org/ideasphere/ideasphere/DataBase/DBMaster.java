package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Config.ConfigMaster;
import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DBMaster implements DataBase {
    private Connection connection;
    private final ConfigMaster configMaster = ConfigMaster.getInstance(); // 配置文件读取工具
    private final ILogger logger = new Log4j2Logger(DBMaster.class); // 日志记录工具

    @Override
    public void connect(ILogger logger) {
        try {
            // 从配置文件中读取数据库文件路径
            String dbFilePath = configMaster.getProperty("db.sqlite.file");
            String dbType = configMaster.getProperty("db.type");
            boolean isInitialized = Boolean.parseBoolean(configMaster.getProperty("db.initialized"));

            // 如果数据库类型不是 sqlite 则抛出异常（目前仅支持 sqlite）
            if (!"sqlite".equals(dbType)) {
                throw new SQLException("Unsupported database type: " + dbType);
            }

            // 如果数据库未初始化，则调用 SQL.java 进行初始化
            if (!isInitialized) {
                logger.info("database", "Database is not initialized, initializing now...");
                SQL.initializeDB(dbFilePath);
                configMaster.setProperty("db.initialized", "true"); // 设置已初始化
            }

            // 检查数据库文件是否存在于指定路径
            if (!new java.io.File(dbFilePath).exists()) {
                logger.error("database", "Database file not found: " + dbFilePath);
                return;
            }

            // 加载 SQLite 驱动并建立连接
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection("jdbc:sqlite:" + dbFilePath);
            logger.info("database","Database connection successful!");
        } catch (Exception e) {
            logger.error("database","Database connection failed", e);
        }
    }

    @Override
    public void disconnect(ILogger logger) {
        try {
            if (connection != null && !connection.isClosed()) {
                connection.close();
                logger.info("database","Database connection closed");
            }
        } catch (SQLException e) {
            logger.error("database","Failed to close database connection", e);
        }
    }

    @Override
    public void insert(ILogger logger, String table, String columns, String values) {
        try {
            String sql = "INSERT INTO " + table + " (" + columns + ") VALUES (" + values + ")";
            Statement stmt = connection.createStatement();
            stmt.execute(sql);
            logger.info("database","Data inserted successfully!");
        } catch (SQLException e) {
            logger.error("database","Failed to insert data", e);
        }
    }

    @Override
    public void update(ILogger logger, String table, String set, String where) {
        try {
            String sql = "UPDATE " + table + " SET " + set + " WHERE " + where;
            Statement stmt = connection.createStatement();
            stmt.execute(sql);
            logger.info("database","Data updated successfully!");
        } catch (SQLException e) {
            logger.error("database","Failed to update data", e);
        }
    }

    @Override
    public void delete(ILogger logger, String table, String where) {
        try {
            String sql = "DELETE FROM " + table + " WHERE " + where;
            Statement stmt = connection.createStatement();
            stmt.execute(sql);
            logger.info("database","Data deleted successfully!");
        } catch (SQLException e) {
            logger.error("database","Failed to delete data", e);
        }
    }

    @Override
    public void query(ILogger logger, String sql) {
        try {
            Statement stmt = connection.createStatement();
            java.sql.ResultSet rs = stmt.executeQuery(sql);
            StringBuilder result = new StringBuilder();
            while (rs.next()) {
                for (int i = 1; i <= rs.getMetaData().getColumnCount(); i++) {
                    result.append(rs.getMetaData().getColumnName(i)).append(": ").append(rs.getString(i)).append(" | ");
                }
                result.append("\n");
            }
            logger.info("database","Query result:\n%s", result.toString());
        } catch (SQLException e) {
            logger.error("database","Failed to execute query", e);
        }
    }
}