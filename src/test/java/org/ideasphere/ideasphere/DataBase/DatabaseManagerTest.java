package org.ideasphere.ideasphere.DataBase;

import com.jayway.jsonpath.internal.Path;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.IOException;
import java.nio.file.Files;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DatabaseManagerTest {
    @Mock
    private Database databaseMock;

    private DatabaseManager databaseManager;
    private Path tempConfigDir;

    @BeforeEach
    void setUp() throws IOException {
        tempConfigDir = (Path) Files.createTempDirectory("config");
        Path configPath = tempConfigDir;

        // 创建测试配置文件
        String configContent = "db.type=mysql\ndb.host=localhost\ndb.port=3306";
        Files.write((java.nio.file.Path) configPath, configContent.getBytes());

        databaseManager = new DatabaseManager(tempConfigDir.toString()) {
            @Override
            protected Database createDatabase(String dbType) {
                return databaseMock;
            }
        };
    }

    @Test
    void testDatabaseInitialization() throws Exception {
        when(databaseMock.getDbType()).thenReturn("mysql");

        assertNotNull(databaseManager);
        verify(databaseMock).connect(any(java.util.Properties.class));
        verify(databaseMock).initialize();
    }
}
