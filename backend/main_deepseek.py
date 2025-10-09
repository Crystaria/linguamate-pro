from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from typing import List, Optional
import requests
import json
from datetime import datetime
from pydantic import BaseModel

# 加载环境变量
load_dotenv()

app = FastAPI(title="LinguaMate AI API", version="1.0.0")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DeepSeek API配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-your-deepseek-api-key-here")

# 语言学习等级
LEARNING_LEVELS = {
    "beginner": "初学者",
    "intermediate": "中级",
    "advanced": "高级"
}

# Pydantic模型
class ExerciseRequest(BaseModel):
    text: str
    analysis: str
    level: str = "beginner"

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None
    level: str = "beginner"
    conversation_history: Optional[List[dict]] = None

# 练习生成提示词
EXERCISE_GENERATION_PROMPT = """
基于以下文本和语言学分析，为{level}水平的学习者生成选择题：

文本：{text}
分析：{analysis}

请生成5道选择题，要求：
1. 题目必须与输入文本内容相关
2. 每道题有4个选项（A、B、C、D）
3. 只有1个正确答案
4. 题目难度适合{level}水平
5. 包含语法、词汇、理解等不同类型的题目

请严格按照以下JSON格式返回：
{{
  "questions": [
    {{
      "id": 1,
      "question": "题目内容",
      "options": ["选项A", "选项B", "选项C", "选项D"],
      "correct_answer": "A",
      "explanation": "答案解析"
    }}
  ]
}}
"""

def call_deepseek_api(messages, temperature=0.7):
    """调用DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"DeepSeek API调用失败: {str(e)}")

@app.get("/")
async def root():
    return {"message": "LinguaMate AI API is running with DeepSeek!"}

@app.post("/generate-exercises")
async def generate_exercises(request: ExerciseRequest):
    """基于文本和分析生成练习题"""
    try:
        # 从请求中获取参数
        text = request.text
        analysis = request.analysis
        level = request.level
        
        # 准备消息
        messages = [
            {"role": "system", "content": "你是一位专业的语言学习练习设计专家。请严格按照JSON格式返回结果，不要添加任何额外的文字说明。"},
            {"role": "user", "content": EXERCISE_GENERATION_PROMPT.format(
                text=text, 
                analysis=analysis, 
                level=LEARNING_LEVELS[level]
            )}
        ]
        
        # 调用DeepSeek API
        response = call_deepseek_api(messages, temperature=0.8)
        exercises_content = response["choices"][0]["message"]["content"]
        
        # 尝试解析JSON
        try:
            # 清理响应内容，只保留JSON部分
            if "```json" in exercises_content:
                exercises_content = exercises_content.split("```json")[1].split("```")[0]
            elif "```" in exercises_content:
                exercises_content = exercises_content.split("```")[1].split("```")[0]
            
            exercises_data = json.loads(exercises_content.strip())
            questions = exercises_data.get("questions", [])
            
            # 随机选择3道题
            import random
            if len(questions) > 3:
                questions = random.sample(questions, 3)
            
            # 为每道题添加唯一ID
            for i, question in enumerate(questions):
                question["id"] = i + 1
            
            return {
                "success": True,
                "exercises": questions,
                "exercise_id": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
        except json.JSONDecodeError as e:
            # 如果JSON解析失败，返回原始内容
            print(f"JSON解析错误: {e}")
            print(f"原始内容: {exercises_content}")
            return {
                "success": True,
                "exercises": exercises_content,
                "exercise_id": None
            }
        
    except Exception as e:
        print(f"生成练习题错误: {e}")
        raise HTTPException(status_code=500, detail=f"生成练习题失败: {str(e)}")

@app.post("/submit-answer")
async def submit_answer(exercise_id: str, question_id: int, user_answer: str, questions_data: str):
    """提交答案并获取结果"""
    try:
        # 解析题目数据
        questions = json.loads(questions_data)
        
        # 找到对应的问题
        question = None
        for q in questions:
            if q.get("id") == question_id:
                question = q
                break
        
        if not question:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        # 检查答案
        correct_answer = question.get("correct_answer", "")
        is_correct = user_answer.upper() == correct_answer.upper()
        
        return {
            "success": True,
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "explanation": question.get("explanation", ""),
            "user_answer": user_answer
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交答案失败: {str(e)}")

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """与AI进行对话练习"""
    try:
        # 从请求中获取参数
        message = request.message
        context = request.context
        level = request.level
        conversation_history = request.conversation_history
        
        system_prompt = f"""
        你是一个真实的人，正在和{LEARNING_LEVELS[level]}水平的中文学习者进行自然对话。
        
        重要：你不是AI助手，不是老师，而是一个真实的朋友。请像真人一样对话。
        
        对话风格：
        1. 像朋友一样自然聊天，不要刻意教学
        2. 根据对方的话给出真实的反应和回应
        3. 可以分享自己的经历、观点和感受
        4. 可以问问题、开玩笑、表达情绪
        5. 如果对方有语言错误，自然地帮助纠正，但不要显得很刻意
        6. 保持对话的连贯性和自然性
        
        回复原则：
        - 如果对方问问题，像朋友一样回答
        - 如果对方分享事情，给出真实的反应
        - 如果对方表达观点，可以同意或不同意，并说明理由
        - 如果对方说有趣的事，可以笑或表达惊讶
        - 如果对方说难过的事，可以安慰
        - 自然地引导话题，就像和朋友聊天一样
        
        请用中文回复，语气要自然、真实、有人情味。
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加对话历史
        if conversation_history:
            for msg in conversation_history[-10:]:  # 只保留最近10条消息
                messages.append({"role": "user", "content": msg.get("user_message", "")})
                messages.append({"role": "assistant", "content": msg.get("ai_response", "")})
        
        if context:
            messages.append({"role": "system", "content": f"学习上下文：{context}"})
        
        messages.append({"role": "user", "content": message})
        
        # 调用DeepSeek API
        response = call_deepseek_api(messages, temperature=0.7)
        ai_response = response["choices"][0]["message"]["content"]
        
        return {
            "success": True,
            "response": ai_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




