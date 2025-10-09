# GitHub上传指南

## 🚀 上传到GitHub的步骤

### 第一步：创建GitHub仓库

1. **登录GitHub**
   - 访问 [GitHub.com](https://github.com)
   - 登录您的账号

2. **创建新仓库**
   - 点击右上角的 "+" 号
   - 选择 "New repository"
   - 仓库名称：`lingua-mate-ai` 或 `eduhacks-ai-fest-2025`
   - 描述：`LinguaMate AI - 多模态语言学习伴侣 for EduHacks AI Fest 2025`
   - 选择 Public（公开）
   - 不要勾选 "Add a README file"（我们已经有了）
   - 点击 "Create repository"

### 第二步：初始化本地Git仓库

```bash
# 进入项目目录
cd eduhacks-ai-fest-2025

# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 创建第一次提交
git commit -m "Initial commit: LinguaMate AI - 多模态语言学习伴侣"
```

### 第三步：连接远程仓库

```bash
# 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/lingua-mate-ai.git

# 推送到GitHub
git push -u origin main
```

### 第四步：创建.gitignore文件

在项目根目录创建 `.gitignore` 文件：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# React
/build
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# next.js build output
.next

# Nuxt.js build output
.nuxt

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/
```

### 第五步：完善仓库信息

1. **添加仓库描述**
   - 在GitHub仓库页面点击 "Settings"
   - 在 "About" 部分添加描述和标签

2. **创建Release**
   - 点击 "Releases" → "Create a new release"
   - Tag version: `v1.0.0`
   - Release title: `LinguaMate AI v1.0.0`
   - 描述项目功能和特色

### 第六步：添加项目徽章

在README.md顶部添加徽章：

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18.0+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![EduHacks](https://img.shields.io/badge/EduHacks-AI%20Fest%202025-orange.svg)
```

## 📋 提交信息规范

### 提交信息格式
```
类型(范围): 简短描述

详细描述（可选）

相关Issue: #123
```

### 常用类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例
```bash
git commit -m "feat: 添加图片分析功能

- 集成Tesseract OCR进行图片文字识别
- 添加图片上传和预览功能
- 实现图片到文本的转换流程

相关Issue: #5"
```

## 🔄 日常开发流程

### 1. 创建功能分支
```bash
git checkout -b feature/new-feature
# 开发功能
git add .
git commit -m "feat: 添加新功能"
git push origin feature/new-feature
```

### 2. 合并到主分支
```bash
git checkout main
git merge feature/new-feature
git push origin main
```

### 3. 删除功能分支
```bash
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

## 📊 仓库管理最佳实践

### 1. 保持仓库整洁
- 定期清理不需要的分支
- 及时删除临时文件
- 保持提交历史清晰

### 2. 文档维护
- 及时更新README
- 添加代码注释
- 维护API文档

### 3. 版本管理
- 使用语义化版本号
- 创建Release标签
- 维护CHANGELOG

## 🎯 竞赛提交准备

### 1. 确保仓库完整
- [ ] 所有源代码已上传
- [ ] README.md完整详细
- [ ] 环境配置说明清晰
- [ ] 演示脚本已准备

### 2. 添加竞赛信息
- [ ] 在README中标注竞赛信息
- [ ] 添加EduHacks徽章
- [ ] 说明项目背景和目标

### 3. 准备演示材料
- [ ] 录制演示视频
- [ ] 准备项目截图
- [ ] 编写项目介绍

## 🔗 有用的Git命令

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 撤销最后一次提交
git reset --soft HEAD~1

# 查看远程仓库
git remote -v

# 拉取最新代码
git pull origin main

# 强制推送（谨慎使用）
git push --force origin main
```

## 📞 获取帮助

如果遇到问题：
1. 查看GitHub官方文档
2. 搜索相关错误信息
3. 在项目Issues中提问
4. 联系项目维护者
