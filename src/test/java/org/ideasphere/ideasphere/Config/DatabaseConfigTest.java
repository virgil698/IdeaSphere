package org.ideasphere.ideasphere.Config;

import com.jayway.jsonpath.internal.Path;
import org.ideasphere.ideasphere.Logger.ILogger;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.IOException;
import java.lang.reflect.Field;
import java.nio.file.Files;

import static junit.framework.TestCase.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.contains;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class DatabaseConfigTest {
    @Mock
    private ILogger loggerMock;

    private DatabaseConfig databaseConfig;
    private Path tempConfigPath;

    @BeforeEach
    void setUp() throws IOException, IOException, NoSuchFieldException, IllegalAccessException {
        databaseConfig = new DatabaseConfig();
        tempConfigPath = (Path) Files.createTempFile("db_config", ".properties");

        // 替换真实logger为mock
        Field loggerField = DatabaseConfig.class.getDeclaredField("logger");
        ((java.lang.reflect.Field) loggerField).setAccessible(true);
        loggerField.set(databaseConfig, loggerMock);
    }

    @Test
    void testCreateConfigFile() {
        String content = "# Test config content";
        boolean result = databaseConfig.checkAndCreateConfigFile((java.nio.file.Path) tempConfigPath, content);

        assertTrue(result);
        verify(loggerMock).info(eq("config"), contains("Created database config file"));
    }

    @Test
    void testReadConfigProperty() throws IOException {
        String expectedValue = "test_value";
        Files.write((java.nio.file.Path) tempConfigPath, ("db.testKey=" + expectedValue).getBytes());

        String value = databaseConfig.readConfigProperty((java.nio.file.Path) tempConfigPath, "db.testKey");
        assertEquals(expectedValue, value);
    }
}
