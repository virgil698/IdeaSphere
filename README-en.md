<br />

<div align="center">
  <a href="https://github.com/IdeaSphere-team/IdeaSphere/">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">IdeaSphere</h3>

<p align="center">
  A forum software focusing on simplicity, practicality and easy configuration, built with Python3.
</p>

[![GitHub forks](https://img.shields.io/github/forks/IdeaSphere-team/IdeaSphere.svg?style=for-the-badge)](https://github.comIdeaSphere-team/IdeaSphere/network)
[![Stars](https://img.shields.io/github/stars/IdeaSphere-team/IdeaSphere.svg?style=for-the-badge)](https://github.com/IdeaSphere-team/IdeaSphere/stargazers)  
[![GitHub license](https://img.shields.io/github/license/IdeaSphere-team/IdeaSphere.svg?style=for-the-badge)](https://github.com/IdeaSphere-team/IdeaSphere/blob/main/LICENSE)
[![Python version](https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/downloads/release/python-3110/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-blueviolet?style=for-the-badge)](https://pypi.org/project/Flask/)
[![Discord](https://img.shields.io/discord/1349304044723765258?style=for-the-badge&logo=discord)](https://discord.gg/eyn9GC88XP)

<p align="center">
  <a href="https://github.com/IdeaSphere-team/IdeaSphere/">简体中文</a> | English
</p>

</div>


## 📖 Project introduction

`IdeaSphere` is a simple and useful forum program based on Python 3.11 and Flask framework. It is easy to configure and suitable for quickly setting up a lightweight forum system.

## 🌟 Core feature

- **Easy to use** : Simple interface, practical functions, easy to use.
- **Easy to configure** : Most of the configuration can be done through the `config.yml` file.
- **Lightweight** : Based on Flask framework development, high performance.
- **Modular design** : Clear code structure, easy to expand and maintain.

## 🌟 Realization function

| task overview | Current status | implementation version |
|---|---|---|
| **⌨️ Login** | ✅ | v0.1.0 |
| **⌨️ Registration** | ✅ | v0.1.0 |
| **⌨️ Post Creation** | ✅ | v0.1.0 |
| **🖼 Super Administrator** | ✅ | v0.1.0 |
| **🖼 Moderator Administrator** | ✅ | v0.1.0 |
| **👤 Like Functionality** | ✅ | v0.1.0 |
| **🧱 Reporting System** | ✅ | v0.1.0 |
| **📦 Online Users** | ✅ | v0.1.0 |
| **⭐ Post Replies** | ✅ | v0.1.0 |
| **🔬 Search** | ✅ | v0.1.5 |
| **👤 Site Statistics** | ✅ | v0.1.5 |
| **🚀 Admin Panel** | ✅ | v0.2.0 |
| **📦 Emoji Support** | ✅ | v0.2.0 |
| **🔬 Post Deletion** | ✅ | v0.2.5 |
| **👤 Permission Groups** | ✅ | v0.2.5 |
| **👤 Full Permission Group Implementation** | 🚧 | |
| **⭐ ICenter (For details, see [here](https://github.com/IdeaSphere-team/IdeaSphere/issues/5))** | 🚧 | |
| **⭐ Content Replies** | 🚧 | |
| **⭐ Content Reactions** | 🚧 | |
| **🎈 Rich Text Editor** | 🚧 | |
| **🎈 Post Sections** | 🚧 | |
| **👤 Post Creation Time and Like Count Sorting** | 🚧 | |
| **👤 Reply Time and Like Count Sorting** | 🚧 | |
| **📦 Private Messaging System** | ⏳ | |
| **📦 User Customization Settings** | ⏳ | |
| **📦 User Profile Page** | ⏳ | |
| **🔐 Email Registration and Password Reset** | ⏳ | |
| **🔌 Templates** | ⏳ | |
| **🔌 Plugins** | ⏳ | |
| **🔐 Data Security** | ⏳ | |
| **🔐 SEO Optimization** | ⏳ | |

Here is the translation of the legend for your reference:

- ✅: Task completed. Great job! 🎉
- 🚧: Task in progress. We're working hard! 💪
- ⏳: Task upcoming. Something exciting is coming soon! 🌠

## 🛠️ Installation Guide

1. Environmental requirements

- **Python version** : 3.11 or higher
- **Operating system**: Windows, Linux, macOS

2. Download the project

```bash
git clone https://github.com/IdeaSphere-team/IdeaSphere.git
cd IdeaSphere
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set parameters

Modify the `config.yml` file to fit your environment:

(In fact, this file is generated automatically the first time you start the program.)

```bash
port: 5000 # program run port
```

5. Start the program

```bash
python app.py
```

The default access address is `http://localhost:5000`

## 🎯 Instructions for use

1. Install the wizard

When you visit the forum for the first time, the installation wizard page ( `/install` ) is automatically displayed and the installation is completed as prompted.

2. User registration and login

Users can register a new account through the `/register` page. After registration is complete, login using the `/login` page.

3. Post and comment

Once logged in, the user can visit the `/post` page to post a new post. In the post details page ( `/view_post` ), users can comment.

4. Manage the background

Administrators can manage users, posts, and comments through the `/admin` page.

## ⬆️ Submit a contribution

To participate in the development of IdeaSphere, you need to submit your contributions in the following ways

1. Fork the repository to your GitHub account
2. Clone the warehouse of your account to a local directory
   `git clone https://github.com/yourusername/IdeaSphere.git`
3. Make changes in the local warehouse and build a document test, then push it to your own warehouse
4. Go back to the repository and launch the PR by clicking Pull requests -> New pull request

## 📞 Contact us

If you have any questions or suggestions, you can contact us at:

- [GitHub Issues](https://github.com/IdeaSphere-team/IdeaSphere/issues/new/choose)
- QQ Communication group：[![QQ](https://img.shields.io/badge/QQ%E4%BA%A4%E6%B5%81%E7%BE%A4-1036347298-20B2AA?style=for-the-badge)](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=0S7iEPBCDpSWgvzARFqxM_zyIlnQ2-km&authKey=AiX0JpNVU8d%2BIjMocMxVhE0OcxbdOaQAt1wnnekYg%2BYQ0GZfOy3KXuSFTBZ2pDD2&noverify=0&group_code=1036347298)
- Discode：[![Discord](https://img.shields.io/discord/1349304044723765258?style=for-the-badge&logo=discord)](https://discord.gg/eyn9GC88XP)

## 🤝 Contributor

[![Contrib](https://contrib.rocks/image?repo=IdeaSphere-team/IdeaSphere)](https://github.com/IdeaSphere-team/IdeaSphere/graphs/contributors)

## ⭐ Star history chart

[![Stargazers over time](https://starchart.cc/IdeaSphere-team/IdeaSphere.svg?variant=adaptive)](https://starchart.cc/IdeaSphere-team/IdeaSphere)

## 😊 Disclaimer

This project is for study and reference purposes only. In the process of use, please ensure that you comply with the relevant laws and regulations and the terms of service of the website.

## 🎫 License

This project is licensed under the `MIT License`. See the `LICENSE` file for more information.

```
MIT License

Copyright (c) 2025 IdeaSphere-team

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
