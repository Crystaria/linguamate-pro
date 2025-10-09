from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional
import json
from datetime import datetime

app = FastAPI(title="LinguaMate AI API", version="1.0.0")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 语言学习等级
LEARNING_LEVELS = {
    "beginner": "初学者",
    "intermediate": "中级", 
    "advanced": "高级"
}

# Pydantic模型
class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None
    level: str = "beginner"

class TextAnalysisRequest(BaseModel):
    text: str
    level: str = "beginner"

class ExerciseRequest(BaseModel):
    record_id: str
    level: str = "beginner"

@app.get("/")
async def root():
    return {"message": "LinguaMate AI API is running!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "LinguaMate AI"}

@app.post("/upload/text")
async def upload_text(request: TextAnalysisRequest):
    """处理文本输入并进行语言学分析"""
    try:
        # 验证学习等级
        if request.level not in LEARNING_LEVELS:
            raise HTTPException(status_code=400, detail="无效的学习等级")
        
        # 模拟AI分析（实际应用中需要调用OpenAI API）
        analysis = f"""
        ## 语言学分析结果
        
        **文本内容**: {request.text}
        **学习等级**: {LEARNING_LEVELS[request.level]}
        
        ### 词汇分析
        - 主要词汇: {', '.join(request.text.split()[:5])}
        - 词汇难度: 适合{LEARNING_LEVELS[request.level]}水平
        
        ### 语法结构
        - 句子类型: 陈述句
        - 语法点: 基本语法结构
        
        ### 学习建议
        - 建议重点学习词汇搭配
        - 可以练习造句
        - 适合进行对话练习
        """
        
        # 模拟保存学习记录
        record_id = f"record_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "success": True,
            "analysis": analysis,
            "record_id": record_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...), level: str = Form("beginner")):
    """处理图片输入，进行OCR识别和语言学分析"""
    try:
        # 验证文件类型
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="请上传图片文件")
        
        # 模拟OCR识别（实际应用中需要Tesseract OCR）
        extracted_text = "This is a sample text extracted from the uploaded image. It contains English words and sentences for language learning."
        
        # 模拟AI分析
        analysis = f"""
        ## 图片分析结果
        
        **识别文本**: {extracted_text}
        **学习等级**: {LEARNING_LEVELS[level]}
        
        ### OCR识别
        - 识别准确率: 95%
        - 识别文字: {extracted_text}
        
        ### 语言学分析
        - 词汇分析: 包含常用词汇
        - 语法结构: 简单句结构
        - 学习建议: 适合{LEARNING_LEVELS[level]}水平练习
        """
        
        # 模拟保存学习记录
        record_id = f"image_record_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "success": True,
            "extracted_text": extracted_text,
            "analysis": analysis,
            "record_id": record_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片处理失败: {str(e)}")

@app.post("/generate-exercises")
async def generate_exercises(request: ExerciseRequest):
    """基于学习记录生成练习题"""
    try:
        # 模拟生成练习题
        exercises = {
            "multiple_choice": [
                {
                    "question": "What is the main topic of the text?",
                    "options": ["Language learning", "Technology", "Science", "History"],
                    "correct": 0
                },
                {
                    "question": "Which word means 'to understand'?",
                    "options": ["comprehend", "confuse", "complicate", "complete"],
                    "correct": 0
                }
            ],
            "fill_blank": [
                {
                    "sentence": "Learning a new language _____ doors to new cultures.",
                    "answer": "opens"
                },
                {
                    "sentence": "Practice makes _____.",
                    "answer": "perfect"
                }
            ],
            "sentence_building": [
                {
                    "words": ["language", "learning", "fun", "is"],
                    "correct_order": "Language learning is fun"
                }
            ],
            "dialogue_completion": {
                "scenario": "Restaurant ordering",
                "dialogue": [
                    {"speaker": "Waiter", "text": "Good evening! Welcome to our restaurant. How many people?"},
                    {"speaker": "Customer", "text": "_____, please.", "answer": "Table for two"}
                ]
            }
        }
        
        return {
            "success": True,
            "exercises": exercises,
            "level": request.level
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成练习题失败: {str(e)}")

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """与AI进行对话练习"""
    try:
        # 模拟AI对话响应
        responses = {
            "beginner": [
                "That's great! Can you tell me more about that?",
                "I understand. What would you like to learn next?",
                "Good job! Let's practice some more.",
                "That's interesting! Can you give me an example?"
            ],
            "intermediate": [
                "Excellent point! How do you think this applies to other situations?",
                "I see what you mean. What's your perspective on this?",
                "That's a thoughtful response. Let's explore this further.",
                "Good observation! Can you elaborate on that?"
            ],
            "advanced": [
                "That's a sophisticated analysis. What are the implications of this?",
                "Interesting perspective. How does this relate to broader concepts?",
                "Excellent reasoning. What other factors should we consider?",
                "That's insightful. Can you provide more nuanced examples?"
            ]
        }
        
        import random
        ai_response = random.choice(responses.get(request.level, responses["beginner"]))
        
        return {
            "success": True,
            "response": ai_response,
            "level": request.level
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")

@app.get("/learning-records")
async def get_learning_records(user_id: str = "demo_user", limit: int = 10):
    """获取学习记录"""
    try:
        # 模拟学习记录数据
        records = [
            {
                "id": "record_001",
                "content_type": "text",
                "content": "Learning a new language opens doors to new cultures.",
                "level": "intermediate",
                "created_at": "2025-09-28T10:00:00Z",
                "analysis_summary": "Text analysis completed"
            },
            {
                "id": "record_002", 
                "content_type": "image",
                "content": "Sample text from image",
                "level": "beginner",
                "created_at": "2025-09-28T09:30:00Z",
                "analysis_summary": "Image analysis completed"
            }
        ]
        
        return {
            "success": True,
            "records": records[:limit]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取记录失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
