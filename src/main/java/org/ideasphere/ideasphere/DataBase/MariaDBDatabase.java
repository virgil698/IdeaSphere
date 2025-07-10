package org.ideasphere.ideasphere.DataBase;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.sql.*;
import java.util.Properties;

public class MariaDBDatabase implements Database {
    private Connection connection;

    @Override
    public void connect(Properties dbProperties) throws SQLException {
        String url = dbProperties.getProperty("url");
        String username = dbProperties.getProperty("username");
        String password = dbProperties.getProperty("password");
        connection = DriverManager.getConnection(url, username, password);
    }

    @Override
    public void initialize() throws Exception {
        String sqlFilePath = "src/main/java/org/ideasphere/ideasphere/DataBase/SQL/mariadb.sql";
        String sqlScript = loadSqlScript(sqlFilePath);

        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sqlScript);
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
    public <T> T query(String sql, RowMapper<T> rowMapper) throws SQLException {
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            if (rs.next()) {
                return rowMapper.mapRow(rs, "mariadb");
            }
            return null;
        }
    }

    @Override
    public void close() throws SQLException {
        if (connection != null && !connection.isClosed()) {
            connection.close();
        }
    }

    @Override
    public String getDbType() {
        return "mariadb";
    }
}