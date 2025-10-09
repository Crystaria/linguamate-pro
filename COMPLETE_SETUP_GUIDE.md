# LinguaMate AI 完整设置指南

## 🛠️ 必要工具安装

### 1. 安装Git
1. 访问 [Git官网](https://git-scm.com/download/win)
2. 下载Windows版本
3. 运行安装程序，使用默认设置
4. 安装完成后重启命令行

### 2. 安装Node.js
1. 访问 [Node.js官网](https://nodejs.org/)
2. 下载LTS版本（推荐18.x或20.x）
3. 运行安装程序
4. 安装完成后重启命令行

### 3. 验证安装
打开新的命令行窗口，运行：
```bash
git --version
node --version
npm --version
python --version
```

## 🚀 项目测试步骤

### 第一步：配置环境变量

1. **编辑后端环境变量**
   ```bash
   # 使用记事本或任何文本编辑器打开
   notepad backend\.env
   ```

2. **填入以下内容**（替换为您的实际密钥）：
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_ANON_KEY=your_supabase_anon_key_here
   DEBUG=True
   ```

### 第二步：启动后端服务

```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn main:app --reload
```

**成功标志**：看到类似以下输出
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 第三步：启动前端服务

**新开一个命令行窗口**：
```bash
# 进入前端目录
cd frontend

# 安装Node.js依赖
npm install

# 启动前端服务
npm start
```

**成功标志**：看到类似以下输出
```
Compiled successfully!

You can now view lingua-mate-ai-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### 第四步：测试网页

1. **打开浏览器**
   - 访问 http://localhost:3000
   - 应该看到LinguaMate AI主页

2. **测试功能**
   - 点击"文本分析"测试文本分析功能
   - 点击"图片分析"测试图片上传功能
   - 点击"对话练习"测试AI对话功能

## 📤 GitHub上传步骤

### 第一步：创建GitHub仓库

1. 访问 [GitHub.com](https://github.com)
2. 登录您的账号
3. 点击右上角 "+" → "New repository"
4. 仓库名称：`lingua-mate-ai`
5. 描述：`LinguaMate AI - 多模态语言学习伴侣 for EduHacks AI Fest 2025`
6. 选择 Public
7. 点击 "Create repository"

### 第二步：上传代码

```bash
# 在项目根目录（eduhacks-ai-fest-2025）运行以下命令

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 创建第一次提交
git commit -m "Initial commit: LinguaMate AI - 多模态语言学习伴侣"

# 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/lingua-mate-ai.git

# 推送到GitHub
git push -u origin main
```

## 🔧 常见问题解决

### 问题1：Node.js未安装
**错误**：'npm' is not recognized
**解决**：安装Node.js并重启命令行

### 问题2：Git未安装
**错误**：'git' is not recognized
**解决**：安装Git并重启命令行

### 问题3：Python依赖安装失败
**错误**：pip install失败
**解决**：
```bash
# 升级pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt
```

### 问题4：前端启动失败
**错误**：npm install失败
**解决**：
```bash
# 清除npm缓存
npm cache clean --force

# 删除node_modules文件夹
rmdir /s node_modules

# 重新安装
npm install
```

### 问题5：API调用失败
**错误**：401 Unauthorized
**解决**：检查.env文件中的API密钥是否正确

## 📋 测试清单

### 功能测试
- [ ] 主页加载正常
- [ ] 文本分析功能正常
- [ ] 图片分析功能正常
- [ ] 对话练习功能正常
- [ ] 学习记录功能正常

### 技术测试
- [ ] 后端API响应正常
- [ ] 前端界面显示正常
- [ ] 数据库连接正常
- [ ] AI功能调用正常

### 部署测试
- [ ] 代码成功上传到GitHub
- [ ] 仓库信息完整
- [ ] README文档清晰
- [ ] 演示视频准备就绪

## 🎯 下一步操作

1. **完成功能测试**
   - 确保所有功能正常工作
   - 记录任何问题并修复

2. **准备演示材料**
   - 录制演示视频
   - 准备项目截图
   - 完善项目文档

3. **提交竞赛**
   - 上传到GitHub
   - 提交到EduHacks平台
   - 准备答辩材料

## 📞 获取帮助

如果遇到问题：
1. 查看错误信息并搜索解决方案
2. 检查环境配置是否正确
3. 参考项目文档和指南
4. 在GitHub Issues中提问

## 🏆 竞赛提交清单

- [ ] 项目代码完整上传到GitHub
- [ ] README.md文档详细完整
- [ ] 演示视频录制完成
- [ ] 项目截图准备就绪
- [ ] 技术文档完善
- [ ] 团队信息填写完整
- [ ] 竞赛平台提交完成
