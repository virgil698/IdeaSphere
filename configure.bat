@echo off
echo 正在安装IdeaSphere所需环境...

:: 安装Python3.13
echo 安装Python3.13...
winget install --id Python.Python.3.13 --source winget

:: 添加Python到环境变量（如果安装时未自动添加）
setx PATH "%PATH%;C:\Python313;C:\Python313\Scripts"

:: 安装git（如果尚未安装）
echo 安装Git...
winget install --id Git.Git --source winget

:: 克隆项目仓库
echo 克隆IdeaSphere项目仓库...
git clone https://github.com/IdeaSphere-team/IdeaSphere.git
cd IdeaSphere

:: 创建并激活虚拟环境
echo 创建并激活虚拟环境...
python -m venv myenv
myenv\Scripts\activate

:: 安装项目依赖
echo 安装项目依赖...
pip install -r requirements.txt

:: 配置Nginx（如果需要）
echo 配置Nginx...
winget install --id nginx.nginx --source winget
cd ..
cd nginx/conf
echo server {> nginx.conf
echo     listen 80;>> nginx.conf
echo     server_name your_server_ip;>> nginx.conf
echo.>> nginx.conf
echo     location / {>> nginx.conf
echo         proxy_pass http://127.0.0.1:5000;>> nginx.conf
echo         proxy_set_header Host $host;>> nginx.conf
echo         proxy_set_header X-Real-IP $remote_addr;>> nginx.conf
echo         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;>> nginx.conf
echo         proxy_set_header X-Forwarded-Proto $scheme;>> nginx.conf
echo     }>> nginx.conf
echo }>> nginx.conf
cd bin
nginx.exe -s reload

echo 安装完成！
pause