package org.ideasphere.ideasphere.DataBase;

import java.sql.SQLException;

public interface Database {
    // 连接数据库
    void connect(String url, String username, String password) throws SQLException;

    // 初始化数据库（执行 SQL 脚本）
    void initialize() throws Exception;

    // 执行查询操作
    <T> T query(String sql, RowMapper<T> rowMapper) throws SQLException;

    // 关闭数据库连接
    void close() throws SQLException;
}