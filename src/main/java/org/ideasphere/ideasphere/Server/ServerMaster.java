package org.ideasphere.ideasphere.Server;

import org.ideasphere.ideasphere.Config.ConfigMaster;
import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

public class ServerMaster implements Server {
    private static ServerMaster instance;
    private final ServerPort serverPort = ServerPort.getInstance();
    private final ServerDebug serverDebug = ServerDebug.getInstance();
    private final ILogger logger = new Log4j2Logger(this.getClass());
    private boolean isRunning = false;

    private ServerMaster() {
        // 私有构造函数，确保单例
    }

    public static synchronized ServerMaster getInstance() {
        if (instance == null) {
            instance = new ServerMaster();
        }
        return instance;
    }

    @Override
    public void startServer() {
        try {
            // 初始化配置
            initializeConfig();

            // 启动服务器
            isRunning = true;
            logger.info("Server", "Server started on port: " + getPort() + " (Debug Mode: " + isDebugMode() + ")");

            // 模拟服务器运行
            while (isRunning) {
                Thread.sleep(1000);
            }
        } catch (Exception e) {
            logger.error("Server", "Failed to start server", e);
        }
    }

    @Override
    public void stopServer() {
        isRunning = false;
        logger.info("Server", "Server stopped");
    }

    @Override
    public int getPort() {
        return serverPort.getPort();
    }

    @Override
    public boolean isDebugMode() {
        return serverDebug.isDebugEnabled();
    }

    private void initializeConfig() {
        // 初始化配置文件
        ConfigMaster configMaster = ConfigMaster.getInstance();
        configMaster.initialize();

        // 验证服务器配置
        validateServerConfig();
    }

    private void validateServerConfig() {
        int port = getPort();
        if (port <= 0 || port > 65535) {
            logger.error("Server", "Invalid server port: " + port);
            throw new IllegalStateException("Invalid server port: " + port);
        }
    }
}