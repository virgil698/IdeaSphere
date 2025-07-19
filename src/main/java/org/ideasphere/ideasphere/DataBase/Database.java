package org.ideasphere.ideasphere.DataBase;

import org.ideasphere.ideasphere.Logger.ILogger;

public interface DataBase {
    void connect(ILogger logger); // 数据库连接方法，带日志记录
    void disconnect(ILogger logger); // 数据库断开连接方法，带日志记录
    void insert(ILogger logger, String table, String columns, String values); // 插入数据，带日志记录
    void update(ILogger logger, String table, String set, String where); // 更新数据，带日志记录
    void delete(ILogger logger, String table, String where); // 删除数据，带日志记录
    void query(ILogger logger, String sql); // 查询数据，带日志记录
}