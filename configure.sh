#!/bin/bash
echo "正在安装IdeaSphere所需环境..."

# 安装Python3.13和pip
echo "安装Python3.13和pip..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt install python3.13 -y
sudo apt install python3-pip -y

# 安装git（如果尚未安装）
echo "安装Git..."
sudo apt install git -y

# 克隆项目仓库
echo "克隆IdeaSphere项目仓库..."
git clone https://github.com/IdeaSphere-team/IdeaSphere.git
cd IdeaSphere

# 创建并激活虚拟环境
echo "创建并激活虚拟环境..."
python3.13 -m venv myenv
source myenv/bin/activate

# 安装项目依赖
echo "安装项目依赖..."
pip install -r requirements.txt

# 安装和配置Nginx
echo "安装和配置Nginx..."
sudo apt update -y
sudo apt install nginx -y

# 创建Nginx配置文件
echo "创建Nginx配置文件..."
sudo tee /etc/nginx/sites-available/ideasphere <<EOF
server {
    listen 80;
    server_name your_server_ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 启用并重启Nginx
sudo ln -sf /etc/nginx/sites-available/ideasphere /etc/nginx/sites-enabled/
sudo systemctl restart nginx

echo "安装完成！"