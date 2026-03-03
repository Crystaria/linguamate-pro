# 🏗️ LinguaMate Pro 技术架构

> 本文档详细说明 LinguaMate Pro 的技术架构设计决策和实现细节

---

## 📐 系统架构概览

```
┌─────────────────────────────────────────────────────────┐
│                     用户层                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │
│  │  Web 端  │  │  移动端  │  │  API 调用 │                 │
│  └────┬────┘  └────┬────┘  └────┬────┘                 │
└───────┼───────────┼───────────┼─────────────────────────┘
        │           │           │
        └───────────┼───────────┘
                    │
        ┌───────────▼───────────┐
        │     前端层 (React)     │
        │  - 组件化开发          │
        │  - 状态管理            │
        │  - 路由管理            │
        └───────────┬───────────┘
                    │ HTTP/REST API
        ┌───────────▼───────────┐
        │    后端层 (FastAPI)    │
        │  - API 路由            │
        │  - 业务逻辑            │
        │  - 数据验证            │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │     服务层             │
        │  - AI 分析服务         │
        │  - OCR 服务            │
        │  - 对话服务            │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │     数据层             │
        │  - 本地存储            │
        │  - 文件系统            │
        └───────────────────────┘
```

---

## 🎨 前端架构

### 技术选型

| 技术 | 版本 | 选择理由 |
|------|------|----------|
| React | 18 | 组件化开发，生态丰富 |
| React Router | 6 | 声明式路由管理 |
| Tailwind CSS | 3 | 原子化 CSS，快速开发 |
| Axios | 1.x | 简洁的 HTTP 客户端 |
| Context API | - | 轻量级状态管理 |

### 目录结构

```
frontend/src/
├── components/          # 可复用组件
│   ├── common/         # 通用组件
│   ├── analysis/       # 分析相关组件
│   └── chat/           # 对话相关组件
├── pages/              # 页面组件
│   ├── Home.js
│   ├── TextAnalysis.js
│   ├── ImageAnalysis.js
│   └── Chat.js
├── contexts/           # React Context
│   └── AppContext.js
├── locales/            # 国际化文件
│   ├── zh.json
│   └── en.json
├── demo-data/          # 演示数据
│   └── samples.js
├── utils/              # 工具函数
├── App.js
└── index.js
```

### 状态管理

使用 Context API 进行全局状态管理：

```javascript
// AppContext.js
const AppContext = createContext();

function AppProvider({ children }) {
  const [language, setLanguage] = useState('zh');
  const [level, setLevel] = useState('beginner');
  const [learningHistory, setLearningHistory] = useState([]);
  
  const value = {
    language,
    setLanguage,
    level,
    setLevel,
    learningHistory,
    setLearningHistory
  };
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}
```

---

## 🔧 后端架构

### 技术选型

| 技术 | 版本 | 选择理由 |
|------|------|----------|
| FastAPI | 0.100+ | 高性能，自动 API 文档 |
| Uvicorn | 0.23+ | 异步 ASGI 服务器 |
| Pydantic | 2.x | 数据验证和序列化 |
| Pillow | 10.x | 图像处理 |
| Pytesseract | 0.3+ | OCR 文字识别 |

### 目录结构

```
backend/
├── main_local.py       # 主入口（本地 AI）
├── demo_mode.py        # 演示模式
├── requirements.txt    # 依赖
├── routers/            # API 路由
│   ├── text.py        # 文本分析
│   ├── image.py       # 图片分析
│   ├── chat.py        # 对话
│   └── records.py     # 学习记录
├── services/           # 业务服务
│   ├── analysis.py    # 分析服务
│   ├── ocr.py         # OCR 服务
│   └── chat.py        # 对话服务
├── models/             # 数据模型
│   └── schemas.py     # Pydantic 模型
└── utils/              # 工具函数
```

### API 设计

遵循 RESTful 规范：

```python
# 文本分析
POST /upload/text
GET /analysis/{id}

# 图片分析
POST /upload/image
GET /analysis/{id}

# 对话
POST /chat
GET /chat/history

# 学习记录
GET /learning-records
DELETE /learning-records
```

---

## 🤖 AI 服务架构

### 本地 AI 模拟

为了降低使用门槛，项目使用本地 AI 模拟：

```python
# demo_mode.py
def analyze_text(text, level):
    """根据等级生成不同深度的分析"""
    if level == 'beginner':
        return simple_analysis(text)
    elif level == 'intermediate':
        return medium_analysis(text)
    else:
        return advanced_analysis(text)

def generate_chat_response(message, context, level):
    """根据场景和等级生成对话响应"""
    # 基于规则和模板的响应生成
    pass
```

### 扩展性设计

支持轻松切换到真实 AI API：

```python
# 配置选项
AI_MODE = 'local'  # 或 'openai', 'deepseek'

if AI_MODE == 'openai':
    from services.openai_service import analyze_text
elif AI_MODE == 'deepseek':
    from services.deepseek_service import analyze_text
else:
    from services.local_service import analyze_text
```

---

## 📊 数据流设计

### 文本分析流程

```
用户输入文本
    ↓
前端验证
    ↓
POST /upload/text
    ↓
后端接收 + 验证
    ↓
AI 分析服务
    ↓
生成练习题
    ↓
返回分析结果
    ↓
前端展示 + 存储历史记录
```

### 图片分析流程

```
用户上传图片
    ↓
前端压缩 + 验证
    ↓
POST /upload/image
    ↓
后端接收
    ↓
OCR 识别（Tesseract）
    ↓
文本分析
    ↓
返回分析结果
    ↓
前端展示 + 存储历史记录
```

---

## 🔐 安全设计

### 前端安全

- ✅ 输入验证（客户端）
- ✅ XSS 防护（React 自动转义）
- ✅ CORS 配置
- ✅ 敏感信息不存储

### 后端安全

- ✅ 输入验证（Pydantic）
- ✅ 文件大小限制
- ✅ 文件类型白名单
- ✅ 错误信息不泄露
- ✅ 速率限制（可扩展）

---

## 🚀 性能优化

### 前端优化

| 优化项 | 实现方式 |
|--------|----------|
| 代码分割 | React.lazy + Suspense |
| 图片优化 | 压缩 + WebP 格式 |
| 缓存策略 | Service Worker |
| 按需加载 | 懒加载组件 |

### 后端优化

| 优化项 | 实现方式 |
|--------|----------|
| 异步处理 | FastAPI async/await |
| 响应压缩 | Gzip |
| 连接池 | 数据库连接池 |
| 缓存 | Redis（可选） |

---

## 🧪 测试策略

### 测试金字塔

```
        /\
       /  \
      / E2E \     端到端测试（10%）
     /______\
    /        \
   / Integration\  集成测试（20%）
  /______________\
 /                \
/    Unit Tests    \ 单元测试（70%）
--------------------
```

### 测试覆盖

- **前端**：Jest + React Testing Library
- **后端**：Pytest
- **E2E**：Playwright（可选）

---

## 📦 部署架构

### 开发环境

```
本地运行
├── 前端：localhost:3000
└── 后端：localhost:8000
```

### 生产环境

```
Vercel (前端)
    ↓ HTTPS
Railway (后端)
    ↓
外部 API（可选）
```

### Docker 部署

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  backend:
    build: ./backend
    ports:
      - "8000:8000"
```

---

## 🎯 设计决策

### 为什么选 React？

- ✅ 组件化开发，代码复用
- ✅ 生态丰富，解决问题快
- ✅ 就业市场需求大

### 为什么选 FastAPI？

- ✅ 性能好（基于 Starlette）
- ✅ 自动生成 API 文档
- ✅ 类型安全（Pydantic）
- ✅ 异步支持

### 为什么本地 AI 模拟？

- ✅ 无需 API 密钥，降低门槛
- ✅ 完全免费，适合演示
- ✅ 可扩展到真实 API

---

## 📈 扩展计划

### 短期（1-3 个月）

- [ ] 添加真实数据库（PostgreSQL）
- [ ] 用户认证系统
- [ ] 更多 AI 模型支持

### 中期（3-6 个月）

- [ ] 移动端应用（React Native）
- [ ] 学习社区功能
- [ ] 付费订阅模式

### 长期（6-12 个月）

- [ ] 多语言学习支持
- [ ] AI 个性化推荐
- [ ] 教育机构合作

---

*最后更新：2026-03-03*
