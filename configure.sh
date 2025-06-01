#!/bin/bash

# 检查并安装IdeaSphere论坛程序依赖的shell脚本

# 定义颜色变量
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始检查并安装IdeaSphere论坛程序依赖${NC}\n"

# 检查Python3是否存在
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}错误：Python3未安装${NC}"
    echo -e "${YELLOW}在Ubuntu/Debian上，可以使用以下命令安装：${NC}"
    echo -e "${GREEN}sudo apt update && sudo apt install python3${NC}"
    echo -e "${YELLOW}在CentOS/RHEL上，可以使用以下命令安装：${NC}"
    echo -e "${GREEN}sudo yum install python3${NC}"
    exit 1
else
    echo -e "${GREEN}检查通过：Python3已安装${NC}"
fi

# 检查pip是否存在
if ! command -v pip3 &> /dev/null
then
    echo -e "${YELLOW}警告：pip3未安装，正在尝试安装...${NC}"

    # 尝试安装pip
    if ! python3 -m ensurepip --upgrade --default-pip &> /dev/null; then
        echo -e "${RED}自动安装pip失败，请手动安装pip3${NC}"
        echo -e "${YELLOW}在Ubuntu/Debian上，可以使用以下命令安装：${NC}"
        echo -e "${GREEN}sudo apt install python3-pip${NC}"
        echo -e "${YELLOW}在CentOS/RHEL上，可以使用以下命令安装：${NC}"
        echo -e "${GREEN}sudo yum install python3-pip${NC}"
        exit 1
    else
        echo -e "${GREEN}成功安装pip3${NC}"
    fi
else
    echo -e "${GREEN}检查通过：pip3已安装${NC}"
fi

# 安装依赖
echo -e "\n${GREEN}开始安装IdeaSphere论坛程序依赖...${NC}"
if pip3 install -r requirements.txt; then
    echo -e "\n${GREEN}所有依赖安装完成！${NC}"
else
    echo -e "${RED}安装依赖失败，请检查requirements.txt文件或网络连接${NC}"
    exit 1
fi