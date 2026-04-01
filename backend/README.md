# LinguaMate AI Backend

这是LinguaMate AI的后端FastAPI服务，提供智能语言学习和分析功能。

## 功能特性

- 📝 **文本分析**: 深度语言学分析和等级化处理
- 🖼️ **图片分析**: OCR识别和图片内容分析
- 💬 **AI对话练习**: 自然对话生成和场景模拟
- 📚 **学习记录**: 学习历史记录和管理
- 🎯 **个性化练习**: 根据学习等级生成不同难度的练习题
- 🌍 **多语言支持**: 中英文双语处理

## 技术栈

- FastAPI - 现代、快速的Web框架
- Uvicorn - ASGI服务器
- Pydantic - 数据验证
- Pillow - 图像处理
- Pytesseract - OCR文字识别
- Python 3.8+

## 安装和运行

### 前置要求

- Python 3.8+
- Tesseract OCR (用于图片文字识别)

### 创建虚拟环境

```bash
python -m venv venv
```

### 激活虚拟环境

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
python main_local.py
```

服务将在 http://localhost:8000 启动

## API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要端点

### 文本分析
- `POST /upload/text` - 上传文本进行分析
- `POST /generate-exercises` - 生成练习题

### 图片分析
- `POST /upload/image` - 上传图片进行OCR分析

### AI对话
- `POST /chat` - 与AI进行对话练习

### 学习记录
- `GET /learning-records` - 获取学习记录
- `DELETE /learning-records` - 清除所有记录

## 配置文件

### 环境变量

创建 `.env` 文件（可选，用于外部API配置）：

```env
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### Tesseract OCR配置

**Windows:**
- 下载并安装 Tesseract OCR
- 确保 `tesseract.exe` 在系统PATH中
- 或修改代码中的路径配置

**Linux:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim  # 中文支持
```

## 项目结构

```
backend/
├── main_local.py          # 本地 AI 版本（推荐用于开发和演示）
├── main_simple.py         # 简化版本（基础功能）
├── main_deepseek.py       # DeepSeek API 版本（使用 DeepSeek 模型）
├── main.py               # OpenAI API 版本（使用 GPT 模型）
├── requirements.txt      # Python 依赖
└── README.md            # 说明文档
```

### 各版本说明

| 文件 | 适用场景 | API 密钥 | 推荐度 |
|------|----------|----------|--------|
| `main_local.py` | 本地开发、演示、无网络环境 | 不需要 | ⭐⭐⭐⭐⭐ 推荐 |
| `main_simple.py` | 快速测试、最小化功能 | 不需要 | ⭐⭐⭐ |
| `main_deepseek.py` | 生产环境（国内） | DeepSeek API Key | ⭐⭐⭐⭐ |
| `main.py` | 生产环境（国际） | OpenAI API Key | ⭐⭐⭐⭐ |

**推荐使用 `main_local.py`** - 无需配置 API 密钥，适合大多数开发和演示场景。

## 开发指南

### 添加新功能

1. 在相应的main_*.py文件中添加新的端点
2. 定义Pydantic模型进行数据验证
3. 添加错误处理和日志记录
4. 更新API文档

### 本地AI vs 外部API

- **main_local.py**: 使用本地模拟AI，无需API密钥，适合开发和演示
- **main.py**: 使用OpenAI API，需要API密钥
- **main_deepseek.py**: 使用DeepSeek API，需要API密钥

### 测试

```bash
# 测试文本分析
curl -X POST "http://localhost:8000/upload/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "level": "beginner", "language": "en"}'

# 测试AI对话
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "context": "introduction", "level": "beginner"}'
```

## 部署

### Docker部署

```bash
docker build -t linguamate-backend .
docker run -p 8000:8000 linguamate-backend
```

### 生产环境

推荐使用Gunicorn或Uvicorn作为WSGI服务器：

```bash
uvicorn main_local:app --host 0.0.0.0 --port 8000 --workers 4
```

## 故障排除

### 常见问题

1. **Tesseract未找到**: 确保Tesseract已安装并在PATH中
2. **端口被占用**: 修改端口号或停止占用端口的进程
3. **依赖安装失败**: 确保Python版本兼容，尝试升级pip

### 日志

服务运行时会输出详细的日志信息，包括请求处理、错误信息等。


