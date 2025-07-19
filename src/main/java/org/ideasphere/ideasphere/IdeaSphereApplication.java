package org.ideasphere.ideasphere;

import org.ideasphere.ideasphere.Config.ApplicationConfig;
import org.ideasphere.ideasphere.Config.Config;
import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@SpringBootApplication
public class IdeaSphereApplication {

    public static final ILogger logger = new Log4j2Logger(IdeaSphereApplication.class);

    public static void main(String[] args) {
        // 服务输出测试
        logger.info("main", "Loading libraries, please wait...");

        long startTime = System.currentTimeMillis();

        // 启动 Spring 应用
        SpringApplication app = new SpringApplication(IdeaSphereApplication.class);
        app.run(args);

        // 获取主目录路径
        String mainDirPath = Paths.get(".").toAbsolutePath().normalize().toString();
        logger.info("main", "Main directory path: " + mainDirPath);

        // 检查并创建 config 文件夹
        Config.checkAndCreateConfigDir(mainDirPath);

        // 复制默认配置文件
        ApplicationConfig.copyConfigFilesIfNeeded(mainDirPath);

        // 验证 config 文件夹是否创建成功
        Path configPath = Paths.get(mainDirPath, "config");
        if (!Files.exists(configPath)) {
            logger.error("main", "Failed to create config directory: " + configPath);
            return;
        }

        // 提示服务启动
        double elapsedTime = ((System.currentTimeMillis() - startTime) / 1000.0); // 确保是 double 类型
        logger.info("main", "Done (%.2f sec)! For help, type \"help\"", elapsedTime);

        // 处理用户输入停止服务
        new Thread(() -> {
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
                String input;
                while ((input = reader.readLine()) != null) {
                    if ("stop".equalsIgnoreCase(input)) {
                        logger.info("main", "Stopping the server...");
                        System.exit(0);
                    }
                }
            } catch (IOException e) {
                logger.error("main", "Error reading input", e);
            }
        }).start();
    }
}