import os
from pathlib import Path

from flask import current_app


def init_footer(app):
    @app.context_processor
    def inject_footer():
        footer_enabled = current_app.config.get("FOOTER_ENABLED", False)
        footer_content = ""

        if footer_enabled:
            config_path = Path("config")
            other_path = config_path / "other"
            foot_file = other_path / "index_foot.html"

            # 检查 config 文件夹是否存在
            if not config_path.exists():
                os.makedirs(config_path, exist_ok=True)

            # 检查 other 文件夹是否存在
            if not other_path.exists():
                os.makedirs(other_path, exist_ok=True)

            # 检查 index_foot.html 文件是否存在
            if not foot_file.exists():
                # 创建默认的 index_foot.html 文件
                default_foot_content = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Footer</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .footer {
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 20px 40px;
            background-color: var(--border-color);
            color: var(--primary-color);
            font-size: 14px;
            line-height: 1.5;
            border-radius: 8px;
            margin: 20px;
        }
        .footer-left {
            display: flex;
            gap: 25px;
        }
        .footer-right {
            text-align: right;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        .footer a {
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.3s;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .footer a:hover {
            color: var(--primary-color);
        }
        .rss-icon {
            width: 24px;
            height: 24px;
            background-color: var(--border-color);
            display: flex;
            justify-content: center;
            align-items: center;
            margin-left: 10px;
        }
        .rss-icon svg {
            fill: #ff6b00;
        }
        .scroll-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background-color: var(--primary-color);
            color: var(--border-color);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            opacity: 0.8;
            transition: opacity 0.3s;
        }
        .scroll-to-top:hover {
            opacity: 1;
        }
        @media (max-width: 768px) {
            .footer {
                flex-direction: column;
                gap: 20px;
            }
            .footer-left {
                flex-direction: column;
                gap: 10px;
            }
            .footer-right {
                text-align: left;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="footer">
        <div class="footer-left">
            <a href="/about">
                <i class="fas fa-info-circle"></i>
                关于本站
            </a>
            <a href="/faq">
                <i class="fas fa-balance-scale"></i>
                论坛准则
            </a>
            <a href="/tos">
                <i class="fas fa-file-contract"></i>
                服务条款
            </a>
            <a href="/privacy">
                <i class="fas fa-shield-alt"></i>
                隐私政策
            </a>
        </div>
        <div class="footer-right">
            <div>IdeaSphere® © 2025 IdeaSphere-team</div>
            <div><i class="fas fa-rss"></i> | Server Status: Online</div>
        </div>
    </div>

    <div class="scroll-to-top" onclick="scrollToTop()">
        <i class="fas fa-chevron-up"></i>
    </div>

    <script>
        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        // Show/hide scroll to top button
        window.addEventListener('scroll', function() {
            const button = document.querySelector('.scroll-to-top');
            if (window.scrollY > 300) {
                button.style.display = 'flex';
            } else {
                button.style.display = 'none';
            }
        });
        
        // Initially hide the button
        document.querySelector('.scroll-to-top').style.display = 'none';
    </script>
</body>
</html>
                """
                with open(foot_file, "w", encoding="utf-8") as f:
                    f.write(default_foot_content)

            # 读取页脚文件内容
            with open(foot_file, "r", encoding="utf-8") as f:
                footer_content = f.read()

        return {"footer_enabled": footer_enabled, "footer_content": footer_content}