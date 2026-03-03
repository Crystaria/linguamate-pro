#  LinguaMate Pro

> **AI 驱动的智能语言学习平台** | AI-Powered Intelligent Language Learning Platform
> 
> 🚀 融合语言学理论与 AI 技术，为学习者提供个性化的语言学习体验
> 
> [🎬 使用指南](./DEMO_GUIDE.md) · [📖 API 文档](./docs/API.md) · [🏗️ 架构说明](./docs/ARCHITECTURE.md)

---

## 📸 项目预览

> *提示：以下为界面截图占位符，实际使用时请替换为真实截图*

![LinguaMate Pro 首页](./docs/screenshots/home.png)
*图 1：LinguaMate Pro 首页 - 简洁现代的设计，支持中英文切换*

![文本分析功能](./docs/screenshots/text-analysis.png)
*图 2：智能文本分析 - 深度语言学分析 + 个性化练习题*

![AI 对话练习](./docs/screenshots/chat.png)
*图 3：AI 对话练习 - 多场景模拟，真实语境练习*

---

## 🎯 项目简介

LinguaMate Pro 是一个基于人工智能的多模态语言学习平台，融合语言学理论和现代 AI 技术，为学习者提供个性化的语言学习体验。

**核心功能：**
- 🤖 **AI 驱动**：智能文本分析、图片识别、对话练习
- 📚 **分级学习**：初级/中级/高级差异化内容
- 🌍 **多语言**：中英文界面无缝切换
- 🎨 **现代设计**：React + Tailwind CSS 构建的响应式界面
- ⚡ **快速部署**：一键启动脚本，支持 Docker 部署

**适用场景：**
- 📖 英语学习者自主练习
- 🎓 语言培训机构辅助教学
- 📱 小红书/社交媒体内容创作
- 💼 企业英语培训

---

## 🚀 快速开始

### 方式 1：一键启动（推荐）

```bash
git clone https://github.com/Crystaria/linguamate-pro.git
cd linguamate-pro
bash scripts/quick-start.sh
```

访问 http://localhost:3000 开始使用！

### 方式 2：分别启动

**后端：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main_local.py
```

**前端：**
```bash
cd frontend
npm install
npm start
```

### 方式 3：在线体验

> *在线版本部署中，敬请期待...*

---

## ✨ 核心功能

### 1️⃣ 智能文本分析

上传英文文本，AI 进行深度语言学分析，包括词汇、语法、语义分析，并生成个性化练习题。

**功能特点：**
- 🔍 词汇分析：词根词缀解析、难度评估
- 📊 语法结构：句子类型分析、复杂度评估
- 🎯 语义理解：主题识别、语境分析
- 📚 练习生成：分级选择题自动生成

![文本分析示例](./docs/screenshots/text-analysis-detail.png)
*图：文本分析结果展示 - 词汇、语法、语义全方位分析*

**使用示例：**
```
输入："The quick brown fox jumps over the lazy dog."

分析结果：
- 词汇：quick (adj.) 快速的 | 难度：简单
- 语法：陈述句 | 一般现在时 | 简单句
- 语义：主题 - 动物/动作 | 情感 - 中性
- 练习：自动生成 3 道选择题
```

---

### 2️⃣ 图片内容识别

上传教材截图或包含文字的图片，系统自动识别文字内容并进行语言学分析。

**功能特点：**
- 🔤 OCR 文字识别：支持中英文
- 📖 内容分析：图片文字语言学分析
- 🎨 智能识别：根据图片类型提供分析
- 📝 练习生成：基于图片内容生成练习题

![图片分析示例](./docs/screenshots/image-analysis.png)
*图：图片分析 - OCR 识别 + 语言学分析一体化*

**使用场景：**
- 📸 拍摄教材页面，快速分析
- 🖼️ 分析英文海报、广告
- 📱 截图社交媒体英文内容
- 📰 分析新闻图片中的文字

---

### 3️⃣ AI 对话练习

与 AI 进行自然对话，模拟真实场景，提升语言实际运用能力。

**功能特点：**
- 🍽️ 预设场景：餐厅、购物、问路、自我介绍
- 🎭 自定义场景：用户创建个性化场景
- 🧠 上下文记忆：AI 记住对话历史
- 📈 分级对话：根据等级调整难度

![对话练习示例](./docs/screenshots/chat-detail.png)
*图：AI 对话练习 - 真实场景模拟 + 智能回复建议*

**预设场景：**
| 场景 | 描述 | 适合等级 |
|------|------|----------|
| 🍽️ 餐厅点餐 | 在餐厅点菜、询问菜品 | 初级 - 中级 |
| 🛍️ 购物 | 商店购物、询问价格 | 初级 - 中级 |
| 🗺️ 问路 | 询问方向、指路 | 初级 - 中级 |
| 👋 自我介绍 | 初次见面、介绍自己 | 初级 |
| 💼 面试 | 工作面试场景 | 中级 - 高级 |
| 🏥 就医 | 医院看病、描述症状 | 中级 - 高级 |

---

### 4️⃣ 学习历史追踪

记录所有学习活动，包括文本分析、图片分析、对话练习等，提供完整的学习进度管理。

**功能特点：**
- 📊 学习记录：完整活动历史
- 📈 进度追踪：可视化学习数据
- 🗑️ 数据管理：一键清除历史

---

## 🎮 演示模式

> **快速体验功能** - 无需注册，一键演示

LinguaMate Pro 内置演示模式，适合：
- 🎬 产品演示
- 📱 内容创作（小红书/抖音等）
- 🎓 教学展示
- 💼 商务洽谈

**使用方式：**

在各功能页面点击"**快速演示**"按钮，系统会自动：
1. 填充示例数据
2. 执行分析流程
3. 展示完整结果

**示例数据包括：**
- 文本分析：预设英文段落（名人名言、新闻片段等）
- 图片分析：预设示例图片
- AI 对话：预设对话场景

---

## 🏗️ 技术架构

### 前端技术栈

| 技术 | 用途 |
|------|------|
| React 18 | 前端框架 |
| React Router | 路由管理 |
| Tailwind CSS | 样式框架 |
| Lucide React | 图标库 |
| Axios | HTTP 客户端 |
| Context API | 状态管理 |

### 后端技术栈

| 技术 | 用途 |
|------|------|
| FastAPI | Web 框架 |
| Uvicorn | ASGI 服务器 |
| Pydantic | 数据验证 |
| Pillow | 图像处理 |
| Pytesseract | OCR 文字识别 |

### 工程化实践

| 实践 | 工具 |
|------|------|
| 代码规范 | ESLint + Prettier |
| 单元测试 | Jest + Pytest |
| CI/CD | GitHub Actions |
| 容器化 | Docker + Docker Compose |
| 部署 | Vercel + Railway |

---

## 📁 项目结构

```
linguamate-pro/
├── frontend/              # React 前端应用
│   ├── src/
│   │   ├── components/    # 可复用组件
│   │   ├── contexts/      # React Context
│   │   ├── locales/       # 国际化文件
│   │   ├── pages/         # 页面组件
│   │   ├── demo-data/     # 演示数据
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── README.md
├── backend/               # FastAPI 后端服务
│   ├── main_local.py      # 本地 AI 版本
│   ├── demo_mode.py       # 演示模式
│   ├── requirements.txt
│   └── README.md
├── scripts/               # 工具脚本
│   ├── quick-start.sh     # 一键启动
│   └── deploy.sh          # 一键部署
├── tests/                 # 测试用例
│   ├── frontend/
│   └── backend/
├── docs/                  # 项目文档
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── 功能演示.md
├── DEMO_GUIDE.md          # 使用指南
├── docker-compose.yml
└── README.md
```

---

## 🎓 学习等级系统

| 等级 | 文本分析 | 图片分析 | 对话练习 |
|------|----------|----------|----------|
| 🔰 初级 | 简单词汇、基础语法 | 基础文字识别 | 日常交流、简单问答 |
| 🔶 中级 | 复合句型、推理分析 | 复杂文本分析 | 引导式复杂问题 |
| 🔥 高级 | 复杂语法、批判思维 | 深度文化背景分析 | 真实问题解决 |

---

## 🧪 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

---

## 🚀 部署

### 前端部署（Vercel）

```bash
cd frontend
npm run build
vercel deploy
```

### 后端部署（Railway）

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 部署
cd backend
railway up
```

### Docker 部署

```bash
docker-compose up -d
```

---

## 📖 文档

- [🎬 使用指南](./DEMO_GUIDE.md) - 详细使用说明
- [📖 API 文档](./docs/API.md) - 完整 API 接口说明
- [🏗️ 架构说明](./docs/ARCHITECTURE.md) - 技术架构详解
- [📚 功能演示](./docs/功能演示.md) - 功能使用教程

---

## 🎬 演示视频

[观看演示视频](https://youtu.be/a9MqQiWWUL4)

---

## 👨‍💻 开发者

**Crystaria** - 全栈开发 / 产品设计 / 语言学研究

- GitHub: [@Crystaria](https://github.com/Crystaria)
- 项目：[LinguaMate Pro](https://github.com/Crystaria/linguamate-pro)

---

## 🙏 致谢

感谢所有使用和支持这个项目的用户！

特别感谢我的 AI 助理小爪陪我一起开发～ 🦞

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🌟 更新日志

### v1.0.0 (2026-03)
- ✨ 初始版本发布
- 🎨 文本分析、图片分析、AI 对话三大核心功能
- 📚 分级学习系统
- 🌍 中英文双语支持

---

**⭐ 如果这个项目对你有帮助，请给我一个星标！**

**💬 欢迎在 Issues 中提出建议或反馈！**
