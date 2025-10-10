# LinguaMate AI Frontend

这是LinguaMate AI的前端React应用，提供智能语言学习功能。

## 功能特性

- 🌍 **多语言支持**: 中文/英文界面切换
- 📝 **文本分析**: 深度文本语言学分析
- 🖼️ **图片分析**: OCR识别和图片内容分析
- 💬 **AI对话练习**: 自然对话练习和场景模拟
- 📚 **学习历史**: 记录和查看学习进度
- 🎯 **个性化练习**: 根据学习等级生成练习题

## 技术栈

- React 18
- React Router
- Tailwind CSS
- Lucide React (图标)
- Axios (HTTP客户端)

## 安装和运行

### 前置要求

- Node.js 16+ 
- npm 或 yarn

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm start
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

### 部署到GitHub Pages

```bash
npm run deploy
```

## 项目结构

```
src/
├── components/          # 可复用组件
│   ├── Header.js       # 页面头部
│   └── LanguageToggle.js # 语言切换
├── contexts/           # React Context
│   └── LanguageContext.js # 语言上下文
├── locales/           # 国际化文件
│   ├── en.js         # 英文翻译
│   └── zh.js         # 中文翻译
├── pages/            # 页面组件
│   ├── Home.js       # 首页
│   ├── TextAnalysis.js # 文本分析
│   ├── ImageAnalysis.js # 图片分析
│   ├── ChatPractice.js # AI对话练习
│   └── LearningHistory.js # 学习历史
├── App.js            # 主应用组件
├── App.css           # 应用样式
├── index.js          # 入口文件
└── index.css         # 全局样式
```

## 环境配置

确保后端API服务运行在 http://localhost:8000

## 开发指南

### 添加新页面

1. 在 `src/pages/` 创建新组件
2. 在 `App.js` 中添加路由
3. 在语言文件中添加翻译

### 添加新语言

1. 在 `src/locales/` 创建新的语言文件
2. 在 `LanguageContext.js` 中添加语言选项
3. 在 `LanguageToggle.js` 中添加切换选项

## 部署

项目已配置GitHub Pages自动部署。每次推送到main分支时，会自动构建并部署到GitHub Pages。

访问地址: https://crystaria.github.io/linguamate-ai


