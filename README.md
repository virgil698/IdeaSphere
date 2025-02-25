<br />

<div align="center">
<h3 align="center">HelloBBS</h3>

<p align="center">
  主打简单实用易于配置的论坛程序，基于python3完成
</p>

[![GitHub stars](https://img.shields.io/github/stars/virgil698/hellobbs.svg)](https://github.com/virgil698/hellobbs/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/virgil698/hellobbs.svg)](https://github.com/virgil698/hellobbs/network)
[![GitHub license](https://img.shields.io/github/license/virgil698/hellobbs.svg)](https://github.com/virgil698/hellobbs/blob/main/LICENSE)
[![Python version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/release/python-3110/)
[![Flask](https://img.shields.io/badge/Flask-1.1.4-blueviolet)](https://pypi.org/project/Flask/)
[![SQLite3](https://img.shields.io/badge/SQLite3-3.35.0-orange)](https://www.sqlite.org/index.html)

</div>


## 📖 项目介绍

`hellobbs` 是一个基于 Python 3.11 和 Flask 框架开发的简单实用的论坛程序。它易于配置，适合快速搭建一个轻量级的论坛系统。

## 🌟 核心特点

- **简单易用**：界面简洁，功能实用，易于上手。
- **易于配置**：通过 `config.yml` 文件即可完成大部分配置。
- **轻量级**：基于 Flask 框架开发，性能高效。
- **模块化设计**：代码结构清晰，方便扩展和维护。

## 🌟 实现功能

| 任务大概 | 目前情况 | 实现版本  |
|---|---|---|
| **🔌 登录** | ✅ | v0.1.0 |
| **⌨️ 注册** | ✅ | v0.1.0 |
| **🔐 发帖** | ✅ | v0.1.0 |
| **🎈 超级管理员**  | ✅ | v0.1.0 |
| **🖼 版主管理员** | ✅ | v0.1.0 |
| **👤 点赞** | ✅ | v0.1.0 |
| **🧱 举报系统** | ✅ | v0.1.0 |
| **📦 在线用户** | ✅ | v0.1.0 |
| **⭐ 帖子回复** | ✅ | v0.1.0 |
| **⭐ 内容回复** | 🚧 |        |
| **🔬 内容反应** | 🚧 |        |
| **🚀 搜索** | 🚧 |        |
| **🚀 私信** | ⏳ |        |
| **🚀 富文本编辑器** | ⏳ |        |
| **🚀 帖子板块** | ⏳ |        |
| **🚀 帖子发布时间、点赞数量排列** | ⏳ |        |
| **🚀 回复时间、点赞数量排列** | ⏳ |        |
| **🚀 私信系统** | ⏳ |        |
| **🚀 站点统计** | ⏳ |        |
| **🚀 用户自定义头像与用户名** | ⏳ |        |
| **🚀 用户页面** | ⏳ |        |
| **🚀 邮箱注册、重置密码** | ⏳ |        |
| **🚀 模板** | ⏳ |        |
| **🚀 插件** | ⏳ |        |
| **🚀 SEO优化** | ⏳ |        |

以下是图例的翻译，供您参考：

- ✅：任务已完成。太棒了！🎉
- 🚧：任务正在进行中。我们正在努力！💪
- ⏳：任务即将开始。令人期待的事情即将到来！🌠



## 📚 项目结构
```bash
hellobbs/
├── instance/
│   └── forum.db                # SQLite3 数据库文件
├── templates/
│   ├── admin_panel.html        # 管理后台页面
│   ├── base.html               # 基础模板
│   ├── index.html              # 首页
│   ├── install.html            # 安装页面
│   ├── login.html              # 登录页面
│   ├── online_users.html       # 在线用户页面
│   ├── post.html               # 发帖页面
│   ├── register.html           # 注册页面
│   ├── report_comment.html     # 举报评论页面
│   ├── report_post.html        # 举报帖子页面
│   └── view_post.html          # 查看帖子页面
├── app.py                      # 主程序入口
├── config.yml                  # 配置文件
└── requirements.txt            # 依赖文件
```

## 🛠️ 安装指南

1. 环境要求

- **Python 版本**：3.11 或更高
- **操作系统**：Windows, Linux, macOS

2. 下载项目

```bash
git clone https://github.com/virgil698/hellobbs.git
cd hellobbs
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置参数

修改 `config.yml` 文件以适配您的环境：

```bash
port: 5000  # 程序运行端口
```

5. 启动程序

```bash
python app.py
```

默认访问地址为：`http://localhost:5000`

## 🎯 使用说明

1. 安装向导

首次访问论坛时，会自动进入安装向导页面（`install.html`），按照提示完成安装。

2. 用户注册与登录

用户可以通过 `/registe`r 页面注册新账号。注册完成后，使用 `/login` 页面登录。

3. 发布帖子与评论

登录后，用户可以访问 `/post` 页面发布新帖子。在帖子详情页（`/view_post`），用户可以发表评论。

4. 管理后台

管理员可以通过 `/admin` 页面管理用户、帖子和评论。

## 🤝 贡献指南

欢迎参与 HelloBBS 的开发，您需要通过以下方式提交你的贡献

1. Fork 此仓库至自己的 GitHub 账户下
2. 将自己账户下的仓库克隆至本地
   `git clone https://github.com/你的用户名/hellobbs.git`
3. 在本地仓库中进行修改并构建文档测试,无误后 push 至自己的仓库
4. 回到此仓库,点击 Pull requests -> New pull request 发起 PR

如果您有任何问题或建议，可以通过以下方式联系我们：

- 提交 GitHub Issues
- 邮箱：virgil698@231s.net

[![Contrib](https://contrib.rocks/image?repo=virgil698/hellobbs)](https://github.com/virgil698/hellobbs/graphs/contributors)

## ⭐ 历史图

[![Stargazers over time](https://starchart.cc/virgil698/hellobbs.svg?variant=adaptive)](https://starchart.cc/virgil698/hellobbs)

## 😊 免责声明

本项目仅供学习和参考使用。在使用过程中，请确保遵守相关法律法规和网站服务条款。

## 🎫 许可证

本项目采用 `MIT License` 许可证。有关详细信息，请参阅 `LICENSE` 文件。

```
MIT License

Copyright (c) 2025 virgil698

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
