# 🎬 视频转音频工具 - 专业版

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-7.1+-orange.svg)](https://ffmpeg.org/)
[![许可证](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个功能强大的视频转音频工具，基于PyQt5构建的精美GUI界面，专注于视频转MP3功能，支持批量处理和多种音质选择。
##✨ 功能特性

- 🎵 **视频转MP3**: 支持多种音质选择，默认保持原视频音质
- 📁 **批量处理**: 支持批量转换多个视频文件
- 🎨 **精美界面**: 现代化PyQt5界面设计
- 🔧 **智能检测**: 自动检测FFmpeg环境
- 📍 **智能输出**: 默认保存在原视频目录
- 🖱️ **拖拽支持**：支持文件拖拽操作，使用更便捷
- 🐍 **Python环境自动配置**: 智能检测和修复Python环境，注：手动安装需要勾选Add python.exe to PATH.    点击install now安装
![67tool-2025-09-01_19_33_57](https://github.com/user-attachments/assets/c6e66553-b5d1-4ec8-ac54-9b50b970c905)

## 🚀 快速开始

### 环境要求

- Windows 10/11
- 网络连接（首次运行需要下载Python）

###🎯 一键启动（推荐）

**最简单的方式：**
1. 下载并解压项目文件
2. 双击 ``启动.bat``
3. 脚本会自动：
   - 优先使用本地Python环境（如果存在）
   - 检测系统Python环境
   - 下载并配置Python（如果需要）
   - 安装必要的依赖包
   - 启动视频转音频工具

### 📦 手动安装

如果您喜欢手动控制，可以按以下步骤操作：

1. **安装Python**
   ```bash
   # 从 https://www.python.org/downloads/ 下载 Python 3.12+
   # 安装时请勾选"Add Python to PATH"
   ```

2. **安装依赖包**
   ```bash
   pip install PyQt5 ffmpeg-python python-ffmpeg pathlib2
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

##🎯 使用说明

### 单文件转换

1. 点击“选择视频文件”按钮或直接拖拽视频文件到指定区域
2. 选择输出目录（默认使用原视频目录）
3. 选择MP3音质（默认保持原音质）
4. 勾选"转换为MP3"
5. 点击“开始转换”按钮

### 批量转换

1. 切换到"批量转换"标签页
2. 选择包含视频文件的目录（支持拖拽文件夹）
3. 配置批量转换选项
4. 点击"开始批量转换"按钮

### 支持的视频格式

- **常见格式**: MP4, AVI, MKV, MOV, WMV, FLV
- **网络格式**: WebM, M4V, 3GP
- **其他格式**: RMVB, TS

## 🔧 技术架构

- **前端界面**: PyQt5 + QSS样式
- **核心转换**: FFmpeg命令行工具
- **多线程处理**: QThread异步转换
- **文件管理**: Python pathlib
- **环境管理**: 自动Python环境配置
- **拖拽支持**: Qt拖拽事件处理

## 📁 项目结构

```
视频转音频工具/
├── main.py                 # 主程序文件 (PyQt5 GUI)
├── README.md              # 项目详细说明文档
├── 启动.bat               # 一键启动脚本（推荐）
├── python-3.12.4-amd64.exe # Python安装包（已集成）
├── python-portable/        # 本地Python环境（自动创建）
│   ├── python.exe         # Python解释器
│   └── Scripts/           # 脚本目录
│       └── pip.exe        # pip包管理器
├── ffmpeg-7.1-essentials_build/  # FFmpeg工具包（已集成）
│   ├── bin/
│   │   ├── ffmpeg.exe     # 视频转换工具
│   │   ├── ffprobe.exe    # 媒体信息工具
│   │   └── ffplay.exe     # 媒体播放工具
│   ├── doc/                # 文档
│   └── presets/            # 预设文件
└── python_env_info.txt     # Python环境信息（自动创建）
```

## 🎨 界面预览

程序包含三个主要标签页：

1. **单文件转换**: 单个视频文件转换界面，支持文件拖拽
2. **批量转换**: 批量处理多个视频文件，支持文件夹拖拽
3. **设置**: FFmpeg状态检查和程序信息

## 🔍 常见问题

### Q: 第一次运行很慢？
A: 这是正常的，程序需要下载Python环境。后续运行会很快。

### Q: Python下载失败？
A: 检查网络连接，或手动下载Python安装包。

### Q: PyQt5安装失败？
A: 程序会自动尝试PySide2作为替代方案。

### Q: 程序启动失败？
A: 运行 `启动.bat` 来自动修复环境问题。

### Q: 如何完全重新安装Python环境？
A: 删除 `python-portable` 文件夹，然后运行 `启动.bat`。

### Q: 支持哪些操作系统？
A: 目前主要支持Windows 10/11，其他系统需要手动配置。

### Q: 本地Python环境有什么优势？
A: 本地环境完全独立，不会影响系统Python，更安全可靠。

## 📝 更新日志

### v1.1.0 (2024-01-01)
- ✨ 新增拖拽文件支持
- 🚀 新增Python环境自动配置
- 🔧 智能环境检测和修复
- 📦 自动依赖包管理
- 🎨 优化用户界面
- 🐍 集成本地Python环境

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- 🎵 支持视频转MP3（保持原音质）
- 📁 支持批量处理
- 🎨 精美PyQt5界面
- 🔧 集成FFmpeg 7.1

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 贡献方式

1. **Fork** 这个项目
2. **创建** 一个特性分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **打开** 一个Pull Request

### 问题反馈

如果您发现了bug或有功能建议，请：
1. 查看现有的 [Issues](../../issues)
2. 创建新的Issue，详细描述问题或建议

## 📄 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [FFmpeg](https://ffmpeg.org/) 项目组提供的强大视频处理工具
- [PyQt5](https://pypi.org/project/PyQt5/) 开发团队提供的优秀GUI框架
- [Python](https://www.python.org/) 社区提供的便携版Python
- 所有为项目做出贡献的开发者

## ⭐ 支持项目

如果这个项目对您有帮助，请给它一个⭐️！

---

**享受您的视频转音频体验！** 🎉 
