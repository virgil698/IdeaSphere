package org.ideasphere.ideasphere.Server;

import org.ideasphere.ideasphere.Config.ConfigMaster;

public class ServerDebug {
    private static ServerDebug instance;
    private boolean debugMode;
    private final ConfigMaster configMaster = ConfigMaster.getInstance();
    private final String PROPERTY_KEY = "debug.mode";

    private ServerDebug() {
        // 私有构造函数，确保单例
    }

    public static synchronized ServerDebug getInstance() {
        if (instance == null) {
            instance = new ServerDebug();
        }
        return instance;
    }

    public boolean isDebugEnabled() {
        if (!debugMode) {
            loadDebugModeFromConfig();
        }
        return debugMode;
    }

    private void loadDebugModeFromConfig() {
        String debugModeStr = configMaster.getProperty(PROPERTY_KEY);
        debugMode = Boolean.parseBoolean(debugModeStr);
    }

    public void setDebugEnabled(boolean debugMode) {
        this.debugMode = debugMode;
        // 更新配置文件
        configMaster.setProperty(PROPERTY_KEY, Boolean.toString(debugMode));
    }
}