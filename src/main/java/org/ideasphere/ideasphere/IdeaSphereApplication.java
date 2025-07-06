package org.ideasphere.ideasphere;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class IdeaSphereApplication {

    private static final Logger logger = LogManager.getLogger(IdeaSphereApplication.class);

    public static void main(String[] args) {
        // 服务输出测试
        logger.info("Loading libraries, please wait...");

        // 启动 Spring 应用
        SpringApplication app = new SpringApplication(IdeaSphereApplication.class);
        app.run(args);

        // 提示服务启动
        long startTime = System.currentTimeMillis();
        logger.info("Done ({} sec)! For help, type \"help\"", (System.currentTimeMillis() - startTime) / 1000);

        // 处理用户输入停止服务
        new Thread(() -> {
            while (true) {
                try {
                    // 监听用户输入
                    int input = System.in.read();
                    if (input == 's' || input == 'S') {
                        // 获取下一个字符判断是否是 'top'
                        int nextChar = System.in.read();
                        if (nextChar == 't' || nextChar == 'T') {
                            int nextNextChar = System.in.read();
                            if (nextNextChar == 'o' || nextNextChar == 'O') {
                                int nextNextNextChar = System.in.read();
                                if (nextNextNextChar == 'p' || nextNextNextChar == 'P') {
                                    logger.info("Server has been stopped.");
                                    System.exit(0);
                                }
                            }
                        }
                    } else if (input == 3) { // 判断是否是 Ctrl + C
                        logger.info("Server has been stopped.");
                        System.exit(0);
                    }
                } catch (Exception e) {
                    logger.error("Error reading input", e);
                }
            }
        }).start();
    }
}