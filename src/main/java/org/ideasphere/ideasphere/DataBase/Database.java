package org.ideasphere.ideasphere.DataBase;

import java.sql.SQLException;
import java.util.Properties;

public interface Database {
    // 连接数据库
    void connect(Properties dbProperties) throws SQLException;

    // 初始化数据库（执行 SQL 脚本）
    void initialize() throws Exception;

    // 执行查询操作并返回结果
    <T> T query(String sql, RowMapper<T> rowMapper) throws SQLException;

    // 关闭数据库连接
    void close() throws SQLException;

    // 获取数据库类型
    String getDbType();
}