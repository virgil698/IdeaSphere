package org.ideasphere.ideasphere.Server;

import org.ideasphere.ideasphere.Config.ConfigMaster;

public class ServerPort {
    private static ServerPort instance;
    private int port;
    private final ConfigMaster configMaster = ConfigMaster.getInstance();
    private final String PROPERTY_KEY = "server.port";

    private ServerPort() {
        // 私有构造函数，确保单例
    }

    public static synchronized ServerPort getInstance() {
        if (instance == null) {
            instance = new ServerPort();
        }
        return instance;
    }

    public int getPort() {
        if (port == 0) {
            loadPortFromConfig();
        }
        return port;
    }

    private void loadPortFromConfig() {
        String portStr = configMaster.getProperty(PROPERTY_KEY);
        try {
            port = Integer.parseInt(portStr);
            releasePort(port);
        } catch (NumberFormatException e) {
            throw new IllegalStateException("Invalid port value in config.properties: " + portStr);
        }
    }

    private void releasePort(int port) {
        // 模拟释放端口逻辑
        // 在实际应用中，这里可以添加释放端口的系统调用或相关逻辑
        System.out.println("Releasing port: " + port);
        // 可以根据实际需要添加端口释放代码
    }
}