package org.ideasphere.ideasphere.Server;

public interface Server {
    void startServer();
    void stopServer();
    int getPort();
    boolean isDebugMode();
}