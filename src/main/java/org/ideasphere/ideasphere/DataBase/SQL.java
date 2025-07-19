package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.nio.file.Files;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.nio.file.Path;
import java.nio.file.Paths;

public class SQL {
    private static final ILogger logger = new Log4j2Logger(SQL.class); // 日志记录工具

    // 初始化数据库（根据配置文件路径）
    public static void initializeDB(String dbFilePath) {
        try {
            // 创建数据库文件所在的目录
            Path dbDirPath = Paths.get(dbFilePath).getParent();
            if (!Files.exists(dbDirPath)) {
                Files.createDirectories(dbDirPath);
                logger.info("database","Created database directory: " + dbDirPath);
            }

            // 加载 SQLite 驱动并建立连接
            Class.forName("org.sqlite.JDBC");
            Connection connection = DriverManager.getConnection("jdbc:sqlite:" + dbFilePath);
            logger.info("database","Initializing database...");

            // 创建 post 表
            String createPostTable = "CREATE TABLE IF NOT EXISTS post (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "pid INTEGER," +
                    "name TEXT," +
                    "content TEXT)";
            Statement stmt = connection.createStatement();
            stmt.execute(createPostTable);

            // 创建 user 表
            String createUserTable = "CREATE TABLE IF NOT EXISTS user (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "uid TEXT," +
                    "name TEXT)";
            stmt.execute(createUserTable);

            logger.info("database","Database initialization complete!");
            connection.close();
        } catch (Exception e) {
            logger.error("database","Database initialization failed", e);
        }
    }
}