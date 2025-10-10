# LinguaMate AI - 智能语言学习平台 | Intelligent Language Learning Platform

[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118.2-green.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.3.2-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 项目概述 | Project Overview

**LinguaMate AI** 是一个基于人工智能的多模态语言学习平台，融合语言学理论和现代AI技术，为学习者提供个性化的语言学习体验。

**LinguaMate AI** is an AI-powered multimodal language learning platform that combines linguistic theories with modern AI technology to provide personalized language learning experiences.

### 🎯 核心特色 | Core Features

- 🌍 **多语言支持** | **Multilingual Support**: 中英文界面无缝切换
- 📝 **智能文本分析** | **Intelligent Text Analysis**: 深度语言学分析和个性化练习生成
- 🖼️ **图片内容识别** | **Image Content Recognition**: OCR识别和图片语言分析
- 💬 **AI对话练习** | **AI Conversation Practice**: 真实场景对话练习和自定义场景
- 📚 **学习历史追踪** | **Learning History Tracking**: 完整的学习记录和进度管理
- 🎓 **分级学习系统** | **Graded Learning System**: 初级/中级/高级差异化内容

---

## 🚀 快速开始 | Quick Start

### 📋 环境要求 | Prerequisites

- **Node.js** 16+ 
- **Python** 3.8+
- **Tesseract OCR** (用于图片文字识别 | for image text recognition)

### 🛠️ 安装步骤 | Installation Steps

#### 1. 克隆项目 | Clone Repository
```bash
git clone https://github.com/Crystaria/linguamate-ai.git
cd linguamate-ai
```

#### 2. 后端配置 | Backend Setup
```bash
cd backend

# 创建虚拟环境 | Create virtual environment
python -m venv venv

# 激活虚拟环境 | Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖 | Install dependencies
pip install -r requirements.txt

# 启动后端服务 | Start backend service
python main_local.py
```

#### 3. 前端配置 | Frontend Setup
```bash
cd frontend

# 安装依赖 | Install dependencies
npm install

# 启动前端服务 | Start frontend service
npm start
```

#### 4. 访问应用 | Access Application
- **前端应用** | **Frontend**: http://localhost:3000
- **后端API** | **Backend API**: http://localhost:8000
- **API文档** | **API Documentation**: http://localhost:8000/docs

---

## ✨ 功能详解 | Features Overview

### 📝 文本分析 | Text Analysis

**功能描述** | **Description**: 上传英文文本，AI进行深度语言学分析，包括词汇、语法、语义分析，并生成个性化的练习题。

**主要特性** | **Key Features**:
- 🔍 词汇分析：词根词缀解析、词汇难度评估
- 📊 语法结构：句子类型分析、语法复杂度评估  
- 🎯 语义理解：主题识别、语境分析
- 📚 练习生成：根据学习等级生成不同难度的选择题

### 🖼️ 图片分析 | Image Analysis

**功能描述** | **Description**: 上传教材截图或包含文字的图片，系统自动识别文字内容并进行语言学分析。

**主要特性** | **Key Features**:
- 🔤 OCR文字识别：支持中英文文字提取
- 📖 内容分析：图片文字的语言学分析
- 🎨 智能识别：根据图片类型提供相应的分析
- 📝 练习生成：基于图片内容生成相关练习题

### 💬 AI对话练习 | AI Conversation Practice

**功能描述** | **Description**: 与AI进行自然对话，模拟真实场景，提升语言实际运用能力。

**主要特性** | **Key Features**:
- 🍽️ 预设场景：餐厅点餐、购物、问路、自我介绍
- 🎭 自定义场景：用户可以创建个性化的对话场景
- 🧠 上下文记忆：AI记住对话历史，保持连贯性
- 📈 分级对话：根据学习等级调整对话难度

### 📚 学习历史 | Learning History

**功能描述** | **Description**: 记录所有学习活动，包括文本分析、图片分析、对话练习等，提供学习进度追踪。

**主要特性** | **Key Features**:
- 📊 学习记录：完整的活动历史记录
- 🎯 进度追踪：学习成果和得分统计
- 🗑️ 数据管理：一键清除历史记录功能

---

## 🎓 学习等级系统 | Learning Level System

### 🔰 初级 | Beginner
- **文本分析** | **Text Analysis**: 简单词汇、基础语法、清晰指导
- **图片分析** | **Image Analysis**: 基础文字识别、简单句子分析
- **对话练习** | **Conversation**: 日常交流、简单问答

### 🔶 中级 | Intermediate  
- **文本分析** | **Text Analysis**: 复合句型、推理分析、扩展词汇
- **图片分析** | **Image Analysis**: 复杂文本分析、语法结构解析
- **对话练习** | **Conversation**: 引导式复杂问题、多领域话题

### 🔥 高级 | Advanced
- **文本分析** | **Text Analysis**: 复杂语法、批判思维、学术表达
- **图片分析** | **Image Analysis**: 深度文化背景分析、文学性内容
- **对话练习** | **Conversation**: 真实问题解决、高级语言技能

---

## 🏗️ 技术架构 | Technical Architecture

### 前端技术栈 | Frontend Stack
- **React 18** - 现代前端框架
- **React Router** - 路由管理
- **Tailwind CSS** - 样式框架
- **Lucide React** - 图标库
- **Axios** - HTTP客户端
- **Context API** - 状态管理

### 后端技术栈 | Backend Stack
- **FastAPI** - 现代Python Web框架
- **Uvicorn** - ASGI服务器
- **Pydantic** - 数据验证
- **Pillow** - 图像处理
- **Pytesseract** - OCR文字识别

### AI能力 | AI Capabilities
- **本地AI模拟** | **Local AI Simulation**: 无需API密钥，完全免费
- **智能语言检测** | **Intelligent Language Detection**: 自动识别输入语言
- **场景化对话** | **Scenario-based Conversation**: 基于场景的自然对话生成
- **个性化分析** | **Personalized Analysis**: 根据学习等级调整内容难度

---

## 📁 项目结构 | Project Structure

```
eduhacks-ai-fest-2025/
├── frontend/                 # React前端应用
│   ├── src/
│   │   ├── components/      # 可复用组件
│   │   ├── contexts/        # React Context
│   │   ├── locales/         # 国际化文件
│   │   ├── pages/           # 页面组件
│   │   ├── App.js           # 主应用
│   │   └── index.js         # 入口文件
│   ├── public/              # 静态文件
│   ├── package.json         # 前端依赖
│   ├── tailwind.config.js   # Tailwind配置
│   └── README.md           # 前端说明
├── backend/                 # FastAPI后端服务
│   ├── main_local.py       # 本地AI版本（推荐）
│   ├── main_simple.py      # 简化版本
│   ├── main_deepseek.py    # DeepSeek API版本
│   ├── main.py             # OpenAI API版本
│   ├── requirements.txt    # Python依赖
│   ├── env_example.txt     # 环境变量示例
│   └── README.md           # 后端说明
├── scripts/                # 工具脚本
├── deployment/             # 部署配置
├── database/               # 数据库相关
└── README.md              # 项目总体说明
```

---

## 🔧 配置说明 | Configuration

### 环境变量 | Environment Variables

创建 `.env` 文件（可选，用于外部API配置）：

```env
# OpenAI API配置（可选）
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# DeepSeek API配置（可选）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Tesseract OCR配置（Windows）
TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
```

### OCR配置 | OCR Configuration

#### 快速安装（推荐）| Quick Installation (Recommended)
```bash
# 运行自动安装脚本
install_tesseract.bat
```

#### 手动安装 | Manual Installation
- **Windows**: 下载安装 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

详细安装指南请查看：`TESSERACT_INSTALLATION_GUIDE.md`

---

## 🚀 部署指南 | Deployment Guide

### GitHub Pages部署 | GitHub Pages Deployment
```bash
cd frontend
npm run build
npm run deploy
```

### Docker部署 | Docker Deployment
```bash
docker-compose up -d
```

### 生产环境 | Production Environment
```bash
# 使用Gunicorn部署
uvicorn main_local:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🎯 API接口 | API Endpoints

### 文本分析 | Text Analysis
```http
POST /upload/text
Content-Type: application/json

{
  "text": "Learning text content",
  "level": "beginner|intermediate|advanced",
  "language": "en|zh"
}
```

### 图片分析 | Image Analysis
```http
POST /upload/image
Content-Type: multipart/form-data

{
  "file": "image_file",
  "level": "beginner|intermediate|advanced",
  "language": "en|zh"
}
```

### 练习生成 | Exercise Generation
```http
POST /generate-exercises
Content-Type: application/json

{
  "text": "analysis_text",
  "analysis": "linguistic_analysis",
  "level": "beginner|intermediate|advanced"
}
```

### AI对话 | AI Chat
```http
POST /chat
Content-Type: application/json

{
  "message": "user_message",
  "context": "scenario_context",
  "level": "beginner|intermediate|advanced",
  "conversation_history": [],
  "custom_scenario_name": "optional_custom_scenario",
  "custom_scenario_description": "optional_description"
}
```

### 学习记录 | Learning Records
```http
GET /learning-records
DELETE /learning-records
```

---

## 🏆 竞赛信息 | Competition Information

- **竞赛名称** | **Competition**: EduHacks AI Fest 2025
- **竞赛时间** | **Date**: September 27 - October 11, 2025
- **竞赛主题** | **Theme**: Personalized Learning
- **竞赛赛道** | **Track**: AI-driven Personalized Learning Systems

---

## 👥 团队成员 | Team Members

- **Crystaria** - 全栈开发 / 产品设计 / 语言学研究
- **Crystaria** - Full-stack Development / Product Design / Linguistics Research

---

## 🛠️ 开发路线图 | Development Roadmap

- [x] 项目架构设计 | Project architecture design
- [x] 后端API开发 | Backend API development  
- [x] 前端界面开发 | Frontend interface development
- [x] AI功能集成 | AI functionality integration
- [x] 国际化支持 | Internationalization support
- [x] 学习等级系统 | Learning level system
- [x] 自定义场景功能 | Custom scenario functionality
- [x] 部署配置 | Deployment configuration
- [ ] 性能优化 | Performance optimization
- [ ] 单元测试 | Unit testing
- [ ] 用户反馈系统 | User feedback system

---

## 📄 许可证 | License

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 贡献指南 | Contributing

我们欢迎任何形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

We welcome contributions of all kinds! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for how to get involved.

---

## 📞 联系方式 | Contact

如有问题或建议，请联系：

For questions or suggestions, please contact:

- **GitHub**: [Crystaria](https://github.com/Crystaria)
- **项目地址** | **Project URL**: https://github.com/Crystaria/linguamate-ai-1
- **在线演示** | **Live Demo**: https://crystaria.github.io/linguamate-ai-1

---

## 🙏 致谢 | Acknowledgments

感谢我的努力！

Thanks to myself for working solo!

---

<div align="center">
  <strong>⭐ 如果这个项目对您有帮助，请给我们一个星标！</strong><br>
  <strong>⭐ If this project helps you, please give us a star!</strong>
</div>