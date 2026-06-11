<div align="center">

# 📚 Chaoxing Auto Evaluation

**超星学习通自动评教脚本 —— 告别手动评教，一键搞定！**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-yellow.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15%2B-green.svg)](https://www.selenium.dev/)

<br/>

> 每学期末都要花半小时评教？不存在的 ☕ 喝口水的功夫就搞定了

</div>

---

## ✨ 功能特性

- 🔐 **自动登录** — 输入账号密码，自动完成登录流程
- 📝 **全自动答题** — 自动处理单选、多选、文本题，一个不落
- 🎯 **智能选优** — 优先选择"无上述问题"，评语随机生成正面评价
- 🔄 **多栏目支持** — 常规评教、课程思政评教、专业认证评教全覆盖
- 📄 **自动翻页** — 评教列表有多页时自动翻页处理，不遗漏任何问卷
- 🛡️ **异常处理** — 自动跳过网页 Bug 导致的重复问卷，断线不慌
- 🖥️ **Windows 一键启动** — 双击 `run.bat` 即可运行，零门槛

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Google Chrome 浏览器
- 网络连接

### 安装与运行

**方式一：一键启动（推荐）**

```bash
# 双击 run.bat 即可，自动安装依赖并运行
run.bat
```

**方式二：手动运行**

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行脚本
python auto_evaluate.py
```

运行后按提示输入超星学习通的账号密码即可。

## 📁 项目结构

```
chaoxing_evaluation/
├── auto_evaluate.py    # 核心脚本
├── run.bat             # Windows 一键启动器
├── requirements.txt    # Python 依赖
├── LICENSE             # MIT 开源许可证
└── README.md           # 项目说明
```

## ⚙️ 工作流程

```
启动浏览器 → 自动登录 → 进入评教页面
    → 遍历评教栏目
        → 查找「待评价」课程（自动翻页遍历所有页）
        → 自动填写问卷（单选 / 多选 / 文本）
        → 提交并确认
    → 全部完成 🎉
```

## 📦 依赖说明

| 依赖 | 版本 | 用途 |
|------|------|------|
| `selenium` | ≥ 4.15.0 | 浏览器自动化 |
| `webdriver-manager` | ≥ 4.0.1 | 自动管理 ChromeDriver |

> 脚本会自动下载匹配的 ChromeDriver，无需手动配置。

## ⚠️ 注意事项

- 首次运行会自动下载 ChromeDriver，请确保网络通畅
- 如遇到验证码，脚本会暂停并提示你在浏览器中手动完成
- 本脚本仅供学习交流使用，请勿用于违规用途

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<div align="center">

**如果觉得有用，点个 ⭐ Star 支持一下叭~**

<br/>

Made with ❤️ by a student who also doesn't like filling out evaluations

</div>
