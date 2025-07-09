package org.ideasphere.ideasphere.Config;

import java.nio.file.Path;

public interface ConfigChecker {
    // 检查指定路径下是否存在配置文件，若不存在则生成
    boolean checkAndCreateConfigFile(Path configFilePath, String content);

    // 检查配置文件内容是否正确
    void checkConfigFileContent(Path configFilePath);
}