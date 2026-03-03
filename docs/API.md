# 📖 LinguaMate Pro API 文档

> 完整的 API 接口说明

**Base URL:** `http://localhost:8000`

**API 文档:** `http://localhost:8000/docs` (Swagger UI)

---

## 🔑 认证

当前版本无需认证，后续版本可能添加。

---

## 📝 文本分析

### POST /upload/text

分析上传的文本内容。

**请求：**
```http
POST /upload/text
Content-Type: application/json

{
  "text": "Learning English is fun and rewarding.",
  "level": "beginner",
  "language": "en"
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | ✅ | 要分析的文本内容 |
| level | string | ✅ | 学习等级：`beginner` \| `intermediate` \| `advanced` |
| language | string | ✅ | 语言：`en` \| `zh` |

**响应：**
```json
{
  "id": "analysis_123",
  "text": "Learning English is fun and rewarding.",
  "level": "beginner",
  "analysis": {
    "vocabulary": [
      {
        "word": "Learning",
        "pos": "verb",
        "root": "learn",
        "difficulty": "easy"
      }
    ],
    "grammar": {
      "sentence_type": "declarative",
      "complexity": "simple"
    },
    "semantics": {
      "topic": "education",
      "sentiment": "positive"
    }
  },
  "exercises": [
    {
      "question": "What is the root form of 'Learning'?",
      "options": ["learn", "learns", "learned", "learning"],
      "answer": "learn"
    }
  ],
  "created_at": "2026-03-03T12:00:00Z"
}
```

---

## 🖼️ 图片分析

### POST /upload/image

分析上传的图片内容（OCR + 语言学分析）。

**请求：**
```http
POST /upload/image
Content-Type: multipart/form-data

file: <image_file>
level: "intermediate"
language: "en"
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | ✅ | 图片文件（JPG/PNG） |
| level | string | ✅ | 学习等级 |
| language | string | ✅ | 语言 |

**响应：**
```json
{
  "id": "analysis_456",
  "type": "image",
  "ocr_text": "The quick brown fox jumps over the lazy dog.",
  "analysis": {
    "vocabulary": [...],
    "grammar": {...},
    "semantics": {...}
  },
  "exercises": [...],
  "created_at": "2026-03-03T12:00:00Z"
}
```

---

## 💬 AI 对话

### POST /chat

与 AI 进行对话练习。

**请求：**
```http
POST /chat
Content-Type: application/json

{
  "message": "Hello, I want to order a coffee.",
  "scenario": "restaurant",
  "level": "beginner",
  "conversation_history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! Welcome to our cafe."}
  ],
  "custom_scenario_name": "My Custom Scenario",
  "custom_scenario_description": "A custom dialogue scenario"
}
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | ✅ | 用户消息 |
| scenario | string | ❌ | 预设场景：`restaurant` \| `shopping` \| `directions` \| `introduction` |
| level | string | ✅ | 学习等级 |
| conversation_history | array | ❌ | 对话历史 |
| custom_scenario_name | string | ❌ | 自定义场景名称 |
| custom_scenario_description | string | ❌ | 自定义场景描述 |

**响应：**
```json
{
  "message": "Great! What kind of coffee would you like?",
  "scenario": "restaurant",
  "conversation_history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! Welcome to our cafe."},
    {"role": "user", "content": "Hello, I want to order a coffee."},
    {"role": "assistant", "content": "Great! What kind of coffee would you like?"}
  ],
  "suggestions": [
    "I'd like a latte, please.",
    "Can I have a cappuccino?",
    "What coffee do you recommend?"
  ]
}
```

---

## 📚 学习记录

### GET /learning-records

获取所有学习记录。

**请求：**
```http
GET /learning-records
```

**响应：**
```json
{
  "records": [
    {
      "id": "analysis_123",
      "type": "text",
      "level": "beginner",
      "created_at": "2026-03-03T12:00:00Z"
    },
    {
      "id": "analysis_456",
      "type": "image",
      "level": "intermediate",
      "created_at": "2026-03-03T13:00:00Z"
    }
  ],
  "total": 2
}
```

---

### DELETE /learning-records

清除所有学习记录。

**请求：**
```http
DELETE /learning-records
```

**响应：**
```json
{
  "message": "All learning records deleted.",
  "deleted_count": 2
}
```

---

## 🏥 健康检查

### GET /health

检查服务状态。

**请求：**
```http
GET /health
```

**响应：**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-03-03T12:00:00Z"
}
```

---

## ❌ 错误响应

### 通用错误格式

```json
{
  "detail": "Error message here",
  "status_code": 400
}
```

### 常见错误码

| 状态码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 413 | 文件过大 |
| 415 | 不支持的文件类型 |
| 500 | 服务器内部错误 |

---

## 🧪 测试示例

### 使用 curl 测试

```bash
# 文本分析
curl -X POST http://localhost:8000/upload/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "level": "beginner", "language": "en"}'

# 图片分析
curl -X POST http://localhost:8000/upload/image \
  -F "file=@test.jpg" \
  -F "level=intermediate" \
  -F "language=en"

# AI 对话
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "scenario": "restaurant", "level": "beginner"}'

# 获取学习记录
curl http://localhost:8000/learning-records

# 清除学习记录
curl -X DELETE http://localhost:8000/learning-records
```

---

## 📝 使用示例（前端）

```javascript
// 文本分析
async function analyzeText(text, level) {
  const response = await fetch('http://localhost:8000/upload/text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: text,
      level: level,
      language: 'en'
    })
  });
  return await response.json();
}

// AI 对话
async function chat(message, scenario, level, history) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      scenario: scenario,
      level: level,
      conversation_history: history
    })
  });
  return await response.json();
}
```

---

*最后更新：2026-03-03*
