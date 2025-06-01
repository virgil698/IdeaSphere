@echo off
echo 正在检查 Python3 和 pip 环境...

REM 检查 Python3 是否存在
where python3 >nul 2>nul
if %errorlevel% neq 0 (
    echo Python3 环境未找到，请先安装 Python3 后重新运行此脚本。
    exit /b
)

REM 检查 pip 是否存在
python3 -m ensurepip --default-pip >nul 2>nul
python3 -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip 未找到，正在尝试安装...
    python3 -m ensurepip --upgrade >nul 2>nul
    if %errorlevel% neq 0 (
        echo pip 安装失败，请手动安装 pip 后重新运行此脚本。
        exit /b
    )
)

echo Python3 和 pip 环境正常，正在安装 IdeaSphere 论坛程序依赖...
python3 -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 依赖安装失败，请检查 requirements.txt 文件路径是否正确，以及网络连接是否正常后重试。
    exit /b
)

echo 依赖安装完成！