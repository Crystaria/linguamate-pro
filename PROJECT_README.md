# LinguaMate AI - 智能语言学习平台

LinguaMate AI是一个基于AI的智能语言学习平台，提供文本分析、图片识别、AI对话练习等多种学习功能。

## 🌟 主要功能

### 📝 文本分析
- 深度语言学分析
- 根据学习等级调整分析复杂度
- 个性化练习生成
- 答案提交和反馈

### 🖼️ 图片分析
- OCR文字识别
- 图片内容分析
- 基于图片的练习生成
- 多语言支持

### 💬 AI对话练习
- 自然对话生成
- 多种预设场景（餐厅、购物、问路、自我介绍）
- 用户自定义场景
- 上下文记忆和连贯对话
- 根据学习等级调整对话难度

### 📚 学习历史
- 记录所有学习活动
- 查看学习进度
- 一键清除历史记录

### 🌍 多语言支持
- 中英文界面切换
- 智能语言检测
- 双语学习支持

## 🏗️ 技术架构

### 前端 (React)
- **框架**: React 18 + React Router
- **样式**: Tailwind CSS
- **图标**: Lucide React
- **HTTP客户端**: Axios
- **国际化**: 自定义Context API

### 后端 (FastAPI)
- **框架**: FastAPI + Uvicorn
- **数据验证**: Pydantic
- **图像处理**: Pillow
- **OCR**: Pytesseract
- **AI处理**: 本地模拟 + 外部API支持

## 📁 项目结构

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

## 🚀 快速开始

### 环境要求
- Node.js 16+
- Python 3.8+
- Tesseract OCR

### 1. 克隆项目
```bash
git clone https://github.com/Crystaria/linguamate-ai.git
cd linguamate-ai
```

### 2. 启动后端服务
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python main_local.py
```

### 3. 启动前端服务
```bash
cd frontend
npm install
npm start
```

### 4. 访问应用
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 🎯 功能特色

### 学习等级差异化
- **初级**: 简单词汇、基础语法、清晰指导
- **中级**: 复合句型、推理分析、扩展词汇
- **高级**: 复杂语法、批判思维、学术表达

### 自定义场景
- 用户可创建个性化对话场景
- 支持场景描述和角色设定
- 动态场景管理和删除

### 智能分析
- 基于内容的练习生成
- 上下文感知的AI对话
- 多维度语言分析

## 🔧 配置说明

### 环境变量
后端支持多种配置方式：
- 本地AI模式（无需API密钥）
- OpenAI API模式
- DeepSeek API模式

### OCR配置
- Windows: 安装Tesseract OCR
- Linux: `sudo apt-get install tesseract-ocr`
- 支持中英文文字识别

## 📱 部署

### GitHub Pages (前端)
```bash
cd frontend
npm run build
npm run deploy
```

### Docker部署
```bash
docker-compose up -d
```

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License

## 🙏 致谢

感谢所有贡献者和开源社区的支持！

---

**访问地址**: https://crystaria.github.io/linguamate-ai


