package org.ideasphere.ideasphere.Config;

import org.ideasphere.ideasphere.Logger.ILogger;
import org.ideasphere.ideasphere.Logger.Log4j2Logger;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.channels.FileChannel;

public class ConfigInitialize {
    private static final String PROJECT_DIR = System.getProperty("user.dir");
    private static final String CONFIG_DIR = PROJECT_DIR + "/config";
    private static final String RESOURCES_DIR = PROJECT_DIR + "/src/main/resources";
    private static final String CONFIG_PROPERTIES = "config.properties";
    private static final String DATABASE_PROPERTIES = "database.properties";
    private static final ILogger logger = new Log4j2Logger(ConfigInitialize.class);

    public static void initialize() {
        try {
            // 检查config文件夹是否存在，不存在则创建
            File configDir = new File(CONFIG_DIR);
            if (!configDir.exists()) {
                configDir.mkdir();
                logger.info("Config", "Created config directory: %s", CONFIG_DIR);
            }

            // 检查配置文件是否存在，不存在则从resources复制
            File configPropertiesFile = new File(CONFIG_DIR + "/" + CONFIG_PROPERTIES);
            File databasePropertiesFile = new File(CONFIG_DIR + "/" + DATABASE_PROPERTIES);

            if (!configPropertiesFile.exists() || !databasePropertiesFile.exists()) {
                copyResourceFile(CONFIG_PROPERTIES);
                copyResourceFile(DATABASE_PROPERTIES);
                logger.info("Config", "Copied example configuration files to config directory");
            }
        } catch (Exception e) {
            logger.error("Config", "Failed to initialize configuration", e);
        }
    }

    private static void copyResourceFile(String fileName) {
        File srcFile = new File(RESOURCES_DIR + "/" + fileName);
        File destFile = new File(CONFIG_DIR + "/" + fileName);

        if (srcFile.exists() && !destFile.exists()) {
            try (FileInputStream fis = new FileInputStream(srcFile);
                 FileOutputStream fos = new FileOutputStream(destFile);
                 FileChannel inChannel = fis.getChannel();
                 FileChannel outChannel = fos.getChannel()) {

                inChannel.transferTo(0, inChannel.size(), outChannel);
                logger.info("Config", "Copied file: %s", fileName);
            } catch (IOException e) {
                logger.error("Config", "Failed to copy file: %s", e);
            }
        }
    }
}