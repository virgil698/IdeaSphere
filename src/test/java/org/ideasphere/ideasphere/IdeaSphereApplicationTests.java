package org.ideasphere.ideasphere;

import org.ideasphere.ideasphere.Config.Config;
import org.ideasphere.ideasphere.Config.DatabaseConfig;
import org.ideasphere.ideasphere.Logger.ILogger;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ConfigurableApplicationContext;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Optional;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class IdeaSphereApplicationTest {

    @Mock
    private ILogger loggerMock;

    @Mock
    private SpringApplication springApplicationMock;

    @InjectMocks
    private IdeaSphereApplication ideaSphereApplication;

    private ILogger originalLogger;

    @BeforeEach
    void setUp() throws NoSuchFieldException, IllegalAccessException {
        // 保存原始 logger
        originalLogger = IdeaSphereApplication.logger;

        // 替换为 mock 的 logger
        Field loggerField = IdeaSphereApplication.class.getDeclaredField("logger");
        loggerField.setAccessible(true);
        loggerField.set(null, loggerMock);

        // 模拟 springApplication 的行为
        when(springApplicationMock.run(any())).thenReturn((ConfigurableApplicationContext) springApplicationMock);
    }

    @AfterEach
    void tearDown() throws NoSuchFieldException, IllegalAccessException {
        // 恢复原始 logger
        Field loggerField = IdeaSphereApplication.class.getDeclaredField("logger");
        loggerField.setAccessible(true);
        loggerField.set(null, originalLogger);
    }

    @Test
    void testMain() throws IOException {
        // 模拟 System.in 输入
        System.setIn(new ByteArrayInputStream("stop\n".getBytes()));

        // 调用 main 方法
        IdeaSphereApplication.main(new String[]{});

        // 验证 logger 是否被调用
        verify(loggerMock).info("Loading libraries, please wait...");
        verify(loggerMock).info(anyString(), Optional.ofNullable(any()));
        verify(loggerMock).info("Stopping the server...");
        verify(loggerMock).info("Shutting down the server...");
    }

    @Test
    void testLoggerInfo() {
        // 调用 info 方法
        IdeaSphereApplication.logger.info("Test message");

        // 验证 logger 是否被调用
        verify(loggerMock).info("Test message");
    }

    @Test
    void testLoggerInfoWithFormat() {
        // 调用 info 方法
        IdeaSphereApplication.logger.info("Test message with arg: %s", "test");

        // 验证 logger 是否被调用
        verify(loggerMock).info(anyString(), Optional.ofNullable(any()));
    }

    @Test
    void testLoggerError() {
        // 创建一个异常
        Exception ex = new Exception("Test exception");

        // 调用 error 方法
        IdeaSphereApplication.logger.error("Test error message", ex);

        // 验证 logger 是否被调用
        verify(loggerMock).error("Test error message", ex);
    }

    @Test
    void testSpringApplicationRun() {
        // 调用 main 方法
        IdeaSphereApplication.main(new String[]{});

        // 验证 springApplication 是否被调用
        verify(springApplicationMock).run(any());
    }

    @Test
    void testShutdownHook() throws IOException {
        // 模拟 System.in 输入
        System.setIn(new ByteArrayInputStream("stop\n".getBytes()));

        // 调用 main 方法
        IdeaSphereApplication.main(new String[]{});

        // 验证 ShutdownHook 是否被调用
        verify(loggerMock).info("Shutting down the server...");
    }

    // 在现有类中添加以下测试方法

    @Test
    void testConfigDirCreation() throws Exception {
        // 模拟主目录路径
        String testDir = "testConfigDir";

        // 调用配置检查方法
        Config.checkAndCreateConfigDir(testDir);

        // 验证日志输出
        verify(loggerMock).info(eq("config"), contains("Created config directory"));

        // 清理测试目录
        Files.deleteIfExists(Paths.get(testDir, "config"));
    }

    @Test
    void testInvalidDatabaseType() throws IOException {
        // 模拟错误配置
        Path invalidConfig = Files.createTempFile("invalid_db", ".properties");
        Files.write(invalidConfig, "db.type=invalid".getBytes());

        DatabaseConfig config = new DatabaseConfig();
        config.checkConfigFileContent(invalidConfig);

        verify(loggerMock).error(contains("Invalid database type"));
    }}