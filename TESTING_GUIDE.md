# LinguaMate AI 测试指南

## 🚀 快速开始测试

### 第一步：安装必要工具

1. **安装Node.js**
   - 访问 [Node.js官网](https://nodejs.org/)
   - 下载并安装LTS版本（推荐18.x或20.x）
   - 安装完成后重启命令行

2. **验证安装**
   ```bash
   node --version
   npm --version
   python --version
   ```

### 第二步：配置API密钥

1. **获取OpenAI API密钥**
   - 访问 [OpenAI官网](https://platform.openai.com/)
   - 注册账号并获取API密钥
   - 复制API密钥备用

2. **获取Supabase配置**
   - 访问 [Supabase官网](https://supabase.com/)
   - 创建新项目
   - 获取项目URL和API密钥

3. **编辑环境变量文件**
   ```bash
   # 编辑 backend/.env 文件
   OPENAI_API_KEY=your_openai_api_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_ANON_KEY=your_supabase_anon_key_here
   DEBUG=True
   ```

### 第三步：设置数据库

1. **在Supabase中创建表**
   - 打开Supabase Dashboard
   - 进入SQL Editor
   - 复制 `database/schema.sql` 内容并执行

2. **验证数据库连接**
   - 确保表创建成功
   - 检查示例数据是否插入

### 第四步：启动后端服务

```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn main:app --reload
```

**预期输出：**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 第五步：启动前端服务

```bash
# 新开一个命令行窗口
cd frontend

# 安装Node.js依赖
npm install

# 启动前端服务
npm start
```

**预期输出：**
```
Compiled successfully!

You can now view lingua-mate-ai-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### 第六步：测试功能

1. **打开浏览器**
   - 访问 http://localhost:3000
   - 应该看到LinguaMate AI主页

2. **测试文本分析**
   - 点击"文本分析"
   - 输入示例文本："Learning a new language opens doors to new cultures."
   - 选择学习等级：中级
   - 点击"开始分析"
   - 查看AI分析结果

3. **测试图片分析**
   - 点击"图片分析"
   - 上传一张包含英文文字的图片
   - 查看OCR识别和AI分析结果

4. **测试对话练习**
   - 点击"对话练习"
   - 选择"餐厅点餐"场景
   - 与AI进行对话练习

5. **查看学习记录**
   - 点击"学习记录"
   - 查看之前的学习历史

## 🔧 故障排除

### 常见问题及解决方案

1. **后端启动失败**
   ```
   错误：ModuleNotFoundError: No module named 'fastapi'
   解决：pip install -r requirements.txt
   ```

2. **前端启动失败**
   ```
   错误：'npm' is not recognized
   解决：安装Node.js并重启命令行
   ```

3. **API调用失败**
   ```
   错误：401 Unauthorized
   解决：检查.env文件中的API密钥是否正确
   ```

4. **数据库连接失败**
   ```
   错误：Database connection failed
   解决：检查Supabase配置和网络连接
   ```

### 测试API接口

运行测试脚本：
```bash
cd backend
python test_api.py
```

**预期输出：**
```
🚀 开始 LinguaMate AI API 测试
==================================================
🔍 测试API连接...
✅ API连接成功
📝 测试文本分析...
✅ 文本分析成功
📚 测试练习生成...
✅ 练习生成成功
💬 测试对话功能...
✅ 对话功能成功
📊 测试学习记录获取...
✅ 学习记录获取成功
🎉 API测试完成！
```

## 🌐 访问地址

- **前端应用**：http://localhost:3000
- **后端API**：http://localhost:8000
- **API文档**：http://localhost:8000/docs
- **数据库管理**：Supabase Dashboard

## 📱 功能测试清单

- [ ] 主页加载正常
- [ ] 文本分析功能
- [ ] 图片分析功能
- [ ] 对话练习功能
- [ ] 学习记录功能
- [ ] 响应式设计
- [ ] 错误处理
- [ ] 加载状态显示

## 🎯 演示准备

1. **准备演示素材**
   - 英文教材截图
   - 示例对话场景
   - 测试文本内容

2. **录制演示视频**
   - 使用屏幕录制软件
   - 按照demo_script.md进行演示
   - 确保画面清晰，声音清楚

3. **测试演示流程**
   - 多次练习演示流程
   - 确保功能稳定
   - 准备备用方案
