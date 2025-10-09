# Git安装和GitHub上传指南

## 🚀 **快速开始**

### **方案一：安装Git for Windows（推荐）**

1. **下载Git for Windows**
   - 访问：https://git-scm.com/download/win
   - 点击"Download for Windows"下载安装程序
   - 运行下载的`.exe`文件

2. **安装配置**
   - 使用默认设置即可（一路点击Next）
   - 安装完成后，重新打开PowerShell或命令提示符

3. **验证安装**
   ```powershell
   git --version
   ```

4. **配置Git用户信息**
   ```powershell
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

5. **运行项目推送脚本**
   ```powershell
   # 方法1：运行PowerShell脚本
   powershell -ExecutionPolicy Bypass -File "git_setup.ps1"
   
   # 方法2：运行批处理脚本
   git_setup.bat
   ```

### **方案二：使用GitHub Desktop（图形界面）**

1. **下载GitHub Desktop**
   - 访问：https://desktop.github.com/
   - 下载并安装GitHub Desktop

2. **使用GitHub Desktop上传**
   - 打开GitHub Desktop
   - 点击"File" → "Add Local Repository"
   - 选择项目文件夹：`D:\Youlan\eduhacks-ai-fest-2025`
   - 点击"Publish repository"
   - 输入仓库名称：`linguamate-ai`
   - 选择可见性（公开或私有）
   - 点击"Publish repository"

### **方案三：使用Visual Studio Code**

1. **在VS Code中打开项目**
   - 打开VS Code
   - 打开文件夹：`D:\Youlan\eduhacks-ai-fest-2025`

2. **使用VS Code的Git功能**
   - 点击左侧的源代码管理图标（Git图标）
   - 点击"Initialize Repository"
   - 添加所有文件（点击文件旁边的"+"）
   - 输入提交信息：`Initial commit - LinguaMate AI`
   - 点击"✓"提交
   - 点击"Publish Branch"发布到GitHub

## 📋 **手动Git命令（如果已安装Git）**

```powershell
# 切换到项目目录
cd "D:\Youlan\eduhacks-ai-fest-2025"

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交第一次commit
git commit -m "Initial commit - LinguaMate AI with custom scenarios and learning levels"

# 设置主分支为main
git branch -M main

# 连接GitHub仓库
git remote add origin https://github.com/Crystaria/linguamate-ai.git

# 推送代码到GitHub
git push -u origin main
```

## 🔧 **故障排除**

### **Git认证问题**
如果遇到认证问题，可以使用以下方法：

1. **使用Personal Access Token**
   - 访问：https://github.com/settings/tokens
   - 生成新的token
   - 使用token作为密码

2. **使用GitHub CLI**
   ```powershell
   # 安装GitHub CLI
   winget install GitHub.cli
   
   # 登录GitHub
   gh auth login
   
   # 创建并推送仓库
   gh repo create linguamate-ai --public --source=. --remote=origin --push
   ```

### **网络问题**
如果遇到网络问题：
- 检查防火墙设置
- 尝试使用VPN
- 使用SSH而不是HTTPS（需要配置SSH密钥）

## 📁 **项目文件说明**

您的项目包含以下重要文件：
- `frontend/` - React前端应用
- `backend/` - FastAPI后端服务
- `README.md` - 项目说明文档
- `requirements.txt` - Python依赖
- `package.json` - Node.js依赖
- `.gitignore` - Git忽略文件配置

## ✅ **上传后的步骤**

1. **验证上传**
   - 访问：https://github.com/Crystaria/linguamate-ai
   - 确认所有文件都已上传

2. **设置README**
   - 在GitHub上编辑README.md
   - 添加项目描述和使用说明

3. **设置GitHub Pages（可选）**
   - 在仓库设置中启用GitHub Pages
   - 选择部署源为main分支

## 🎯 **推荐方案**

对于初学者，我推荐：
1. **GitHub Desktop** - 最简单，图形界面友好
2. **VS Code集成** - 如果您使用VS Code开发
3. **Git命令行** - 如果您想学习Git命令

选择最适合您的方法，然后按照相应步骤操作即可！

