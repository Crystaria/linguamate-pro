from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from typing import List, Optional
import json
from datetime import datetime
from pydantic import BaseModel
import random
from PIL import Image
import pytesseract
import io
import logging

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('linguamate.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 设置 Tesseract 路径 - 使用环境变量优先
TESSERACT_CMD = os.getenv('TESSERACT_CMD', '')
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
elif os.name == 'nt':  # Windows
    # 尝试常见安装路径
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]
    for path in common_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            logger.info(f"Tesseract configured: {path}")
            break
    else:
        logger.warning("Tesseract not found. Set TESSERACT_CMD env var if needed.")

# 加载环境变量
load_dotenv()

# 学习记录存储（简单内存存储，实际项目中应使用数据库）
learning_records = []

# 全局对话历史存储（内存存储）
conversation_history = []

logger.info("Linguamate Pro Local Backend starting...")



def shuffle_options_and_correct_answer(options: list, correct_answer: str):
    """随机打乱选项并返回新的正确答案位置"""
    # 创建选项和答案的映射
    option_map = {
        "A": options[0],
        "B": options[1], 
        "C": options[2],
        "D": options[3]
    }
    
    # 获取正确答案的文本
    correct_text = option_map[correct_answer]
    
    # 随机打乱所有选项
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    
    # 找到正确答案的新位置
    new_correct_answer = None
    for i, option in enumerate(shuffled_options):
        if option == correct_text:
            new_correct_answer = ["A", "B", "C", "D"][i]
            break
    
    return shuffled_options, new_correct_answer

def save_learning_record(record_type: str, level: str, content: str, analysis: str = None, exercises: List[dict] = None, score: int = None, language: str = "zh", context: str = None):
    """保存学习记录"""
    record_id = f"{record_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(learning_records)}"
    
    record = {
        "id": record_id,
        "type": record_type,
        "level": level,
        "content": content,
        "analysis": analysis,
        "exercises": exercises,
        "score": score,
        "timestamp": datetime.now().isoformat(),
        "language": language,
        "context": context
    }
    
    learning_records.append(record)
    return record_id

app = FastAPI(title="Linguamate Pro API", version="1.0.0")

# CORS 设置 - 支持本地开发和 Vercel 部署
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://linguamate-pro.vercel.app",
        "https://linguamate-pro-production.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # 支持所有 Vercel 预览域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 语言学习等级
LEARNING_LEVELS = {
    "beginner": {"zh": "初学者", "en": "Beginner"},
    "intermediate": {"zh": "中级", "en": "Intermediate"},
    "advanced": {"zh": "高级", "en": "Advanced"}
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
    custom_scenario_name: Optional[str] = None
    custom_scenario_description: Optional[str] = None

# 新的简化聊天请求模型，符合您的要求
class SimpleChatRequest(BaseModel):
    message: str

class LearningRecord(BaseModel):
    id: str
    type: str  # "text_analysis", "image_analysis", "chat_practice"
    level: str
    content: str
    analysis: Optional[str] = None
    exercises: Optional[List[dict]] = None
    score: Optional[int] = None
    timestamp: str
    language: str = "zh"

# 智能AI对话回复
def get_ai_response(message: str, level: str, conversation_history: List[dict] = None, context: str = None):
    """根据输入语言和场景智能回复"""
    
    # 检测输入语言 - 改进检测逻辑
    message_lower = message.lower()
    
    # 计算英文字符比例
    english_chars = sum(1 for char in message if char.isalpha() and ord(char) < 128)
    total_chars = sum(1 for char in message if char.isalpha())
    
    # 如果英文字符占80%以上，认为是英文
    is_english = total_chars > 0 and english_chars / total_chars > 0.8
    
    # 特殊情况：如果包含明显的英文关键词，强制识别为英文
    english_keywords = ["hello", "hi", "how", "what", "where", "when", "why", "thank", "goodbye", "bye", "sorry", "help", "trouble", "homework", "weather", "feeling", "sad", "today", "like", "later", "see", "you"]
    if any(word in message_lower for word in english_keywords):
        is_english = True
    
    # 如果包含中文字符，强制识别为中文
    if any('\u4e00' <= char <= '\u9fff' for char in message):
        is_english = False
    
    # 分析对话上下文
    analyzed_context = analyze_conversation_context(message, conversation_history)
    
    if is_english:
        return generate_english_response(message, message_lower, analyzed_context, level, conversation_scenario=context)
    else:
        return generate_chinese_response(message, message_lower, analyzed_context, level, conversation_scenario=context)

def generate_scenario_based_response(message: str, message_lower: str, scenario: str, level: str):
    """根据对话场景生成场景化回复"""
    
    # 餐厅点餐场景
    if "restaurant" in scenario.lower() or "ordering" in scenario.lower():
        if any(word in message_lower for word in ["hello", "hi", "good", "evening", "afternoon", "morning"]):
            return "Good evening! Welcome to our restaurant. I'm your server today. Would you like to see our menu, or do you have any questions about our dishes?"
        elif any(word in message_lower for word in ["menu", "food", "dish", "eat", "hungry"]):
            return "Great! We have a wonderful selection today. Our chef's special is the grilled salmon, and we also have excellent pasta dishes. What type of cuisine are you in the mood for?"
        elif any(word in message_lower for word in ["pasta", "pizza", "salad", "soup", "meat", "fish", "chicken"]):
            return "Excellent choice! That's one of our most popular dishes. Would you like to know about our daily specials, or do you have any dietary preferences I should know about?"
        elif any(word in message_lower for word in ["price", "cost", "expensive", "cheap", "budget"]):
            return "Our prices are very reasonable! Most of our main dishes range from $15 to $25. Would you like me to recommend something within a specific budget?"
        elif any(word in message_lower for word in ["drink", "beverage", "wine", "beer", "water", "coffee"]):
            return "We have a great selection of beverages! We offer fresh juices, coffee, tea, and a nice wine selection. What would you like to drink?"
        elif any(word in message_lower for word in ["ready", "order", "take", "want"]):
            return "Perfect! I'm ready to take your order. What would you like to start with? An appetizer, or shall we go straight to the main course?"
        else:
            return "I'm here to help you with your dining experience! Is there anything specific you'd like to know about our menu or restaurant?"
    
    # 购物场景
    elif "shopping" in scenario.lower():
        if any(word in message_lower for word in ["hello", "hi", "help", "looking"]):
            return "Hello! Welcome to our store! I'm here to help you find exactly what you're looking for. What brings you in today?"
        elif any(word in message_lower for word in ["shirt", "dress", "pants", "shoes", "jacket", "clothes", "clothing"]):
            return "Great choice! We have a wonderful selection of clothing. What size are you looking for? And do you have a particular color or style in mind?"
        elif any(word in message_lower for word in ["price", "cost", "expensive", "cheap", "budget", "how much"]):
            return "Our prices are very competitive! Most of our items are on sale this week. What's your budget range? I can show you some great options within your price range."
        elif any(word in message_lower for word in ["size", "small", "medium", "large", "fit"]):
            return "Let me help you find the right size! We have sizes from XS to XXL. Would you like to try something on? Our fitting rooms are right over there."
        elif any(word in message_lower for word in ["color", "red", "blue", "green", "black", "white"]):
            return "We have that in several colors! What's your favorite color? I can show you all the available options."
        elif any(word in message_lower for word in ["buy", "purchase", "take", "get"]):
            return "Excellent! I'll help you with that. Would you like to pay by card or cash? And do you need a bag for your purchase?"
        else:
            return "I'm here to help you find the perfect item! What are you looking for today? We have clothing, accessories, and much more!"
    
    # 问路场景
    elif "direction" in scenario.lower() or "asking" in scenario.lower():
        if any(word in message_lower for word in ["excuse", "sorry", "help", "lost", "where"]):
            return "Of course! I'd be happy to help you with directions. Where are you trying to go? I know this area quite well."
        elif any(word in message_lower for word in ["station", "train", "bus", "airport", "hotel", "restaurant", "mall", "hospital"]):
            return "I can definitely help you get there! Are you walking, driving, or taking public transportation? That will help me give you the best route."
        elif any(word in message_lower for word in ["walking", "walk", "foot"]):
            return "Perfect! It's about a 10-minute walk from here. Go straight down this street for two blocks, then turn left at the traffic light. You'll see it on your right."
        elif any(word in message_lower for word in ["driving", "car", "drive"]):
            return "If you're driving, take the main road for about 5 minutes, then turn right at the second intersection. There's parking available right in front of the building."
        elif any(word in message_lower for word in ["bus", "public", "transport"]):
            return "You can take bus number 15 from the stop right across the street. It will take you directly there in about 20 minutes. The bus comes every 10 minutes."
        elif any(word in message_lower for word in ["far", "distance", "long", "time"]):
            return "It's not too far! About 15 minutes by foot, or 5 minutes if you're driving. Would you like me to show you on a map?"
        else:
            return "I'm happy to help with directions! What's your destination? I can give you the best route to get there."
    
    # 自我介绍场景
    elif "introduction" in scenario.lower() or "self" in scenario.lower():
        if any(word in message_lower for word in ["hello", "hi", "nice", "meet", "name"]):
            return "Hello! It's so nice to meet you! My name is Alex, and I'm originally from New York. What's your name? And where are you from?"
        elif any(word in message_lower for word in ["work", "job", "do", "profession"]):
            return "I work as a software engineer at a tech company downtown. I really enjoy what I do! What about you? What do you do for work?"
        elif any(word in message_lower for word in ["hobby", "interest", "like", "enjoy", "fun"]):
            return "I love reading books and playing guitar in my free time. I also enjoy hiking on weekends. What are your hobbies? I'd love to hear about what you enjoy doing!"
        elif any(word in message_lower for word in ["family", "parents", "siblings", "brother", "sister"]):
            return "I have a wonderful family! I have two younger sisters and we're very close. Do you have any siblings? Family is so important to me."
        elif any(word in message_lower for word in ["age", "old", "young"]):
            return "I'm 28 years old. How about you? Age is just a number, but it's always interesting to learn about people's life experiences!"
        elif any(word in message_lower for word in ["live", "home", "house", "apartment"]):
            return "I live in a cozy apartment near the city center. I love the neighborhood because it's close to everything. Where do you live? Do you like your area?"
        else:
            return "I'm really enjoying our conversation! Tell me more about yourself. What's something interesting about you that most people don't know?"
    
    return None  # 如果没有匹配的场景，返回None让通用逻辑处理

def analyze_conversation_context(message: str, conversation_history: List[dict] = None):
    """分析对话上下文和场景"""
    context = {
        "topic": "general",
        "mood": "neutral", 
        "intent": "chat",
        "urgency": "normal"
    }
    
    message_lower = message.lower()
    
    # 分析话题
    if any(word in message_lower for word in ["weather", "sunny", "rainy", "cloudy", "hot", "cold", "天气", "下雨", "晴天", "阴天"]):
        context["topic"] = "weather"
    elif any(word in message_lower for word in ["study", "learn", "practice", "homework", "exam", "test", "school", "class", "学习", "练习", "作业", "考试", "学校"]):
        context["topic"] = "education"
    elif any(word in message_lower for word in ["work", "job", "career", "office", "工作", "职业", "办公室"]):
        context["topic"] = "work"
    elif any(word in message_lower for word in ["food", "eat", "restaurant", "cook", "食物", "吃", "餐厅", "做饭"]):
        context["topic"] = "food"
    elif any(word in message_lower for word in ["travel", "trip", "vacation", "旅游", "旅行", "假期"]):
        context["topic"] = "travel"
    elif any(word in message_lower for word in ["family", "friend", "relationship", "家庭", "朋友", "关系"]):
        context["topic"] = "relationship"
    
    # 分析情绪
    if any(word in message_lower for word in ["happy", "excited", "great", "wonderful", "amazing", "开心", "高兴", "兴奋", "棒"]):
        context["mood"] = "positive"
    elif any(word in message_lower for word in ["sad", "tired", "angry", "worried", "nervous", "难过", "累", "生气", "担心", "紧张"]):
        context["mood"] = "negative"
    elif any(word in message_lower for word in ["help", "problem", "issue", "trouble", "帮助", "问题", "麻烦"]):
        context["mood"] = "seeking_help"
        context["urgency"] = "high"
    
    # 分析意图
    if "?" in message or "？" in message:
        context["intent"] = "question"
    elif any(word in message_lower for word in ["thank", "thanks", "谢谢", "感谢"]):
        context["intent"] = "gratitude"
    elif any(word in message_lower for word in ["sorry", "apologize", "对不起", "抱歉"]):
        context["intent"] = "apology"
    elif any(word in message_lower for word in ["goodbye", "bye", "see you", "再见", "拜拜"]):
        context["intent"] = "farewell"
    
    return context

def generate_english_response(message: str, message_lower: str, context: dict, level: str, conversation_scenario: str = None):
    """生成更自然的英文回复，模拟人类对话"""
    
    # 根据对话场景生成场景化回复
    if conversation_scenario:
        scenario_response = generate_scenario_based_response(message, message_lower, conversation_scenario, level)
        if scenario_response:
            return scenario_response
    
    # 根据场景和上下文生成回复
    if context["intent"] == "question":
        if context["topic"] == "education":
            responses = [
                "Oh, homework can be tricky sometimes! What subject are you working on? Maybe I can help you figure it out.",
                "I remember struggling with homework too when I was learning. What's giving you trouble?",
                "Homework stress is real! What are you working on? I might have some tips that could help."
            ]
        elif context["topic"] == "work":
            responses = [
                "Work stuff can be complicated, right? What's going on? I'm all ears.",
                "Oh, work questions! I've been there. What's the situation? Maybe we can brainstorm together.",
                "Work can be challenging sometimes. What's on your mind? I'd love to help if I can."
            ]
        else:
            responses = [
                "Hmm, that's interesting! What made you think of that?",
                "Good question! I'm curious about your thoughts on this. What's your take?",
                "That's something I've wondered about too! What do you think?"
            ]
        return random.choice(responses)
    
    elif context["intent"] == "gratitude":
        responses = [
            "No problem at all! I'm happy I could help. What else is on your mind?",
            "You're so welcome! That's what friends are for, right? Anything else you want to chat about?",
            "My pleasure! I enjoy our conversations. What's next on your mind?"
        ]
        return random.choice(responses)
    
    elif context["intent"] == "apology":
        responses = [
            "Hey, no worries at all! We all have those moments. Everything okay?",
            "Don't even think about it! Is everything alright? You seem a bit stressed.",
            "No need to apologize! What's going on? You seem like something's bothering you."
        ]
        return random.choice(responses)
    
    elif context["intent"] == "farewell":
        responses = [
            "Take care! It was great talking with you. Chat again soon!",
            "Bye! I really enjoyed our conversation. Talk to you later!",
            "See you later! Thanks for the great chat. Take care of yourself!"
        ]
        return random.choice(responses)
    
    elif context["mood"] == "positive":
        if context["topic"] == "education":
            responses = [
                "That's awesome! I love seeing people excited about learning. What's got you so pumped up?",
                "That's fantastic! Learning new things is the best feeling. What did you discover?",
                "I'm so happy for you! There's nothing like that 'aha!' moment. What clicked for you?"
            ]
        elif context["topic"] == "work":
            responses = [
                "That's amazing news! Success at work feels incredible. What happened? I want to hear all about it!",
                "Congratulations! I'm so happy for you. What went well? Tell me everything!",
                "That's wonderful! Work wins are the best. What made this happen?"
            ]
        else:
            responses = [
                "That's so great to hear! Your happiness is contagious. What's making you feel so good?",
                "I love your positive energy! What's got you in such a good mood today?",
                "That's wonderful! I'm smiling just hearing about it. What's the good news?"
            ]
        return random.choice(responses)
    
    elif context["mood"] == "negative":
        if context["urgency"] == "high":
            responses = [
                "Oh no, I can tell you're really going through it. What's happening? I'm here for you.",
                "I'm worried about you. You seem really upset. What's going on? You can tell me anything.",
                "Hey, I can sense something's really bothering you. What's on your mind? I'm listening."
            ]
        else:
            responses = [
                "I can tell you're having a rough time. What's been going on? Sometimes talking helps.",
                "You seem a bit down today. What's bothering you? I'm here to listen.",
                "I notice you seem a bit off. What's on your mind? Want to talk about it?"
            ]
        return random.choice(responses)
    
    elif context["topic"] == "weather":
        responses = [
            "Right? Weather totally affects my mood too! What are you thinking of doing today?",
            "I know, right? Weather can make or break a day. Any fun plans?",
            "Absolutely! Weather is so mood-dependent. What's your day looking like?"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "education":
        responses = [
            "Learning is such a journey, isn't it? What are you working on these days?",
            "I love talking about learning! What's your current focus? I'm curious about your progress.",
            "Education is so important! What are you studying or working on? I'd love to hear about it."
        ]
        return random.choice(responses)
    
    elif context["topic"] == "work":
        responses = [
            "Work life can be so interesting! How's your day going? Any exciting projects?",
            "I'm always curious about people's work! What do you do? How's it going?",
            "Work can be such a mixed bag, right? How are things at your job?"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "food":
        responses = [
            "Food is life! Are you cooking something amazing or trying somewhere new?",
            "I love talking about food! What's your food situation today?",
            "Food always makes everything better! What are you eating or planning to eat?"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "travel":
        responses = [
            "Travel is the best! Are you planning something exciting or just daydreaming?",
            "I'm always up for travel talk! What's your travel situation? Planning anything?",
            "Travel stories are my favorite! What's your travel vibe right now?"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "relationship":
        responses = [
            "Relationships are so important! Are you talking about family, friends, or something else?",
            "I love hearing about people's relationships! What's going on in that area of your life?",
            "Relationships can be so complex! What's on your mind about this?"
        ]
        return random.choice(responses)
    
    else:
        # 默认回复，更自然的对话
        responses = [
            "That's really interesting! Tell me more about that.",
            "Oh, that's cool! I'd love to hear more about your thoughts on this.",
            "That's fascinating! What made you think of that?",
            "I'm curious about that! Can you tell me more?",
            "That's a great point! What's your perspective on this?",
            "Interesting! I hadn't thought about it that way. What else is on your mind?",
            "That's so true! I can relate to that. What's your experience been like?",
            "I love that! What's your take on this whole thing?"
        ]
        return random.choice(responses)

def generate_chinese_scenario_response(message: str, message_lower: str, scenario: str, level: str):
    """根据对话场景生成中文场景化回复"""
    
    # 餐厅点餐场景
    if "restaurant" in scenario.lower() or "ordering" in scenario.lower():
        if any(word in message_lower for word in ["你好", "您好", "晚上好", "下午好", "早上好"]):
            return "您好！欢迎光临我们餐厅。我是今天的服务员。您想看看菜单吗，还是对我们的菜品有什么问题？"
        elif any(word in message_lower for word in ["菜单", "食物", "菜", "吃", "饿"]):
            return "太好了！我们今天有很多美味的菜品。主厨推荐是烤三文鱼，我们还有很棒的意大利面。您想吃什么类型的菜？"
        elif any(word in message_lower for word in ["意大利面", "披萨", "沙拉", "汤", "肉", "鱼", "鸡肉"]):
            return "很好的选择！这是我们最受欢迎的菜品之一。您想了解我们的每日特色菜吗，或者有什么饮食偏好需要我了解？"
        elif any(word in message_lower for word in ["价格", "多少钱", "贵", "便宜", "预算"]):
            return "我们的价格很合理！大部分主菜在15到25美元之间。您想让我推荐一些特定预算范围内的菜品吗？"
        elif any(word in message_lower for word in ["饮料", "酒", "啤酒", "水", "咖啡", "茶"]):
            return "我们有很棒的饮料选择！我们提供鲜榨果汁、咖啡、茶和不错的葡萄酒。您想喝什么？"
        elif any(word in message_lower for word in ["点菜", "要", "想"]):
            return "好的！我准备好为您点菜了。您想从什么开始？开胃菜，还是直接点主菜？"
        else:
            return "我很乐意为您的用餐体验提供帮助！您对我们的菜单或餐厅有什么特别想了解的吗？"
    
    # 购物场景
    elif "shopping" in scenario.lower():
        if any(word in message_lower for word in ["你好", "您好", "帮助", "看"]):
            return "您好！欢迎来到我们商店！我来帮您找到您想要的东西。您今天来买什么呢？"
        elif any(word in message_lower for word in ["衬衫", "裙子", "裤子", "鞋子", "外套", "衣服"]):
            return "很好的选择！我们有很棒的衣服选择。您需要什么尺码？有什么特定的颜色或风格偏好吗？"
        elif any(word in message_lower for word in ["价格", "多少钱", "贵", "便宜", "预算"]):
            return "我们的价格很有竞争力！这周大部分商品都在打折。您的预算是多少？我可以为您推荐一些在您价格范围内的好选择。"
        elif any(word in message_lower for word in ["尺码", "小", "中", "大", "合身"]):
            return "让我帮您找到合适的尺码！我们有从XS到XXL的尺码。您想试穿一下吗？试衣间就在那边。"
        elif any(word in message_lower for word in ["颜色", "红色", "蓝色", "绿色", "黑色", "白色"]):
            return "我们有几种颜色！您最喜欢什么颜色？我可以给您看所有可用的选择。"
        elif any(word in message_lower for word in ["买", "购买", "要", "拿"]):
            return "太好了！我来帮您处理。您想用卡还是现金支付？需要袋子装您的购买物品吗？"
        else:
            return "我很乐意帮您找到完美的商品！您今天在找什么？我们有衣服、配饰等等！"
    
    # 问路场景
    elif "direction" in scenario.lower() or "asking" in scenario.lower():
        if any(word in message_lower for word in ["打扰", "对不起", "帮助", "迷路", "哪里"]):
            return "当然！我很乐意帮您指路。您要去哪里？我对这个地区很熟悉。"
        elif any(word in message_lower for word in ["车站", "火车", "公交", "机场", "酒店", "餐厅", "商场", "医院"]):
            return "我绝对可以帮您到那里！您是步行、开车还是坐公共交通？这样我可以给您最好的路线。"
        elif any(word in message_lower for word in ["步行", "走路", "走"]):
            return "很好！从这里步行大约10分钟。沿着这条街直走两个街区，然后在红绿灯处左转。您会在右边看到它。"
        elif any(word in message_lower for word in ["开车", "车", "驾驶"]):
            return "如果您开车，沿着主干道行驶大约5分钟，然后在第二个十字路口右转。建筑物前面有停车位。"
        elif any(word in message_lower for word in ["公交", "公共", "交通"]):
            return "您可以乘坐街对面的15路公交车。大约20分钟就能直接到达。公交车每10分钟一班。"
        elif any(word in message_lower for word in ["远", "距离", "时间"]):
            return "不太远！步行大约15分钟，开车5分钟。您想让我在地图上给您指出来吗？"
        else:
            return "我很乐意帮您指路！您的目的地是哪里？我可以给您最好的路线。"
    
    # 自我介绍场景
    elif "introduction" in scenario.lower() or "self" in scenario.lower():
        if any(word in message_lower for word in ["你好", "您好", "认识", "名字"]):
            return "您好！很高兴认识您！我叫小明，我来自北京。您叫什么名字？您来自哪里？"
        elif any(word in message_lower for word in ["工作", "职业", "做什么"]):
            return "我在市中心的科技公司做软件工程师。我真的很喜欢我的工作！您呢？您做什么工作？"
        elif any(word in message_lower for word in ["爱好", "兴趣", "喜欢", "享受", "乐趣"]):
            return "我业余时间喜欢读书和弹吉他。周末我也喜欢徒步旅行。您的爱好是什么？我很想听听您喜欢做什么！"
        elif any(word in message_lower for word in ["家庭", "父母", "兄弟姐妹", "兄弟", "姐妹"]):
            return "我有一个很棒的家庭！我有两个妹妹，我们关系很亲密。您有兄弟姐妹吗？家庭对我来说很重要。"
        elif any(word in message_lower for word in ["年龄", "多大", "年轻"]):
            return "我28岁。您呢？年龄只是个数字，但了解人们的生活经历总是很有趣的！"
        elif any(word in message_lower for word in ["住", "家", "房子", "公寓"]):
            return "我住在市中心附近的一个舒适的公寓里。我喜欢这个社区，因为它离一切都很近。您住在哪里？您喜欢您所在的地区吗？"
        else:
            return "我真的很享受我们的对话！告诉我更多关于您的事情。您有什么有趣的事情是大多数人不知道的吗？"
    
    return None  # 如果没有匹配的场景，返回None让通用逻辑处理

def generate_chinese_response(message: str, message_lower: str, context: dict, level: str, conversation_scenario: str = None):
    """生成更自然的中文回复，模拟人类对话"""
    
    # 根据对话场景生成场景化回复
    if conversation_scenario:
        scenario_response = generate_chinese_scenario_response(message, message_lower, conversation_scenario, level)
        if scenario_response:
            return scenario_response
    
    # 根据场景和上下文生成回复
    if context["intent"] == "question":
        if context["topic"] == "education":
            responses = [
                "哦，作业确实有时候挺难的！你在学什么科目？也许我能帮你想想办法。",
                "我记得我学习的时候也经常为作业发愁。哪道题难住你了？",
                "作业压力确实很大！你在做什么题目？我可能有一些小技巧能帮到你。"
            ]
        elif context["topic"] == "work":
            responses = [
                "工作上的事情确实挺复杂的，对吧？发生什么了？我听着呢。",
                "哦，工作问题！我也遇到过。什么情况？也许我们可以一起想想办法。",
                "工作有时候确实挺有挑战性的。你在想什么？我很乐意帮忙。"
            ]
        else:
            responses = [
                "嗯，这挺有意思的！你怎么想到这个的？",
                "好问题！我对你的想法很好奇。你觉得呢？",
                "这个问题我也想过！你觉得怎么样？"
            ]
        return random.choice(responses)
    
    elif context["intent"] == "gratitude":
        responses = [
            "不用谢！能帮到你我很开心。还有什么想聊的吗？",
            "别客气！朋友之间互相帮助是应该的，对吧？还想聊点什么？",
            "我的荣幸！我很喜欢我们的对话。接下来想聊什么？"
        ]
        return random.choice(responses)
    
    elif context["intent"] == "apology":
        responses = [
            "嘿，完全不用道歉！我们都有这样的时候。一切都还好吗？",
            "别想那么多！你看起来有点压力，没事吧？",
            "不需要道歉！发生什么了？你看起来有什么心事。"
        ]
        return random.choice(responses)
    
    elif context["intent"] == "farewell":
        responses = [
            "保重！和你聊天很开心。下次再聊！",
            "拜拜！我真的很享受我们的对话。回头聊！",
            "再见！谢谢你的精彩对话。照顾好自己！"
        ]
        return random.choice(responses)
    
    elif context["mood"] == "positive":
        if context["topic"] == "education":
            responses = [
                "太棒了！我喜欢看到人们对学习这么有热情。什么让你这么兴奋？",
                "太棒了！学习新东西的感觉最棒了。你发现了什么？",
                "我真为你高兴！那种'恍然大悟'的感觉最棒了。你明白了什么？"
            ]
        elif context["topic"] == "work":
            responses = [
                "这消息太棒了！工作上的成功感觉太棒了。发生什么了？我想听听！",
                "恭喜你！我真为你高兴。什么进展顺利？快告诉我！",
                "太棒了！工作上的胜利最棒了。是什么促成了这个结果？"
            ]
        else:
            responses = [
                "听到这个太棒了！你的快乐很有感染力。什么让你感觉这么好？",
                "我喜欢你的正能量！今天什么让你心情这么好？",
                "太棒了！光是听到我就很开心。有什么好消息？"
            ]
        return random.choice(responses)
    
    elif context["mood"] == "negative":
        if context["urgency"] == "high":
            responses = [
                "哦不，我能看出来你真的很不好受。发生什么了？我在这里陪着你。",
                "我很担心你。你看起来真的很沮丧。怎么了？你可以告诉我任何事情。",
                "嘿，我能感觉到有什么在困扰你。你在想什么？我在听。"
            ]
        else:
            responses = [
                "我能看出来你最近不太好过。发生什么了？有时候说出来会好受一些。",
                "你今天看起来有点低落。什么在困扰你？我在这里听你说。",
                "我注意到你看起来有点不对劲。你在想什么？想聊聊吗？"
            ]
        return random.choice(responses)
    
    elif context["topic"] == "weather":
        responses = [
            "对吧？天气真的会影响我的心情！你今天打算做什么？",
            "我知道，对吧？天气真的能决定一天的好坏。有什么有趣的计划吗？",
            "绝对是这样！天气真的很影响心情。你今天怎么安排？"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "education":
        responses = [
            "学习真是一段旅程，对吧？你最近在学什么？",
            "我喜欢聊学习！你现在的重点是什么？我对你的进展很好奇。",
            "教育真的很重要！你在学什么或者在做什么？我很想听听。"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "work":
        responses = [
            "工作生活真的很有趣！你今天过得怎么样？有什么有趣的项目吗？",
            "我总是对人们的工作很好奇！你做什么工作？怎么样？",
            "工作真的是一把双刃剑，对吧？你工作怎么样？"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "food":
        responses = [
            "食物就是生活！你在做什么好吃的还是想尝试新餐厅？",
            "我喜欢聊食物！你今天吃什么？",
            "食物总是能让一切变得更好！你在吃什么或者打算吃什么？"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "travel":
        responses = [
            "旅行最棒了！你在计划什么有趣的还是只是在幻想？",
            "我总是喜欢聊旅行！你的旅行情况怎么样？在计划什么吗？",
            "旅行故事是我的最爱！你现在的旅行心情怎么样？"
        ]
        return random.choice(responses)
    
    elif context["topic"] == "relationship":
        responses = [
            "人际关系真的很重要！你在说家庭、朋友还是别的什么？",
            "我喜欢听人们的人际关系故事！你生活中这方面怎么样？",
            "人际关系可能很复杂！你在想什么？"
        ]
        return random.choice(responses)
    
    else:
        # 默认回复，更自然的对话
        responses = [
            "这真的很有趣！告诉我更多关于这个的。",
            "哦，这很酷！我很想听听你对这个的更多想法。",
            "这很吸引人！你怎么想到这个的？",
            "我对这个很好奇！你能告诉我更多吗？",
            "这是个很好的观点！你对这个怎么看？",
            "有趣！我没想到这个角度。你还想什么？",
            "这很对！我能理解。你的经历是什么样的？",
            "我喜欢这个！你对整个事情怎么看？"
        ]
        return random.choice(responses)

# 生成基于内容的练习题
def generate_content_based_exercises(text: str, analysis: str, level: str):
    """根据学习等级生成不同难度的练习题"""
    
    # 分析文本内容
    words = text.lower().split()
    sentences = text.split('.')
    
    # 提取关键词汇
    key_words = []
    for word in words:
        if len(word) > 3 and word.isalpha():
            key_words.append(word)
    
    # 去重并限制数量
    key_words = list(set(key_words))[:10]
    
    # 根据学习等级生成不同难度的题目
    if level == "beginner":
        return generate_beginner_exercises(text, key_words, sentences)
    elif level == "intermediate":
        return generate_intermediate_exercises(text, key_words, sentences)
    else:  # advanced
        return generate_advanced_exercises(text, key_words, sentences)

def generate_beginner_exercises(text: str, key_words: list, sentences: list) -> list:
    """生成初级水平的练习题"""
    questions = []
    
    # 题目1：词汇选择题 - 基于实际词汇含义
    if key_words:
        target_word = random.choice(key_words)
        # 根据词汇生成合理的选项
        if target_word.lower() in ['learn', 'learning', 'study', 'studying']:
            options = [
                "To gain knowledge or skills",
                "To forget information",
                "To teach others",
                "To make mistakes"
            ]
            correct_text = "To gain knowledge or skills"
        elif target_word.lower() in ['important', 'significant', 'crucial']:
            options = [
                "Very necessary or valuable",
                "Not necessary at all",
                "Only sometimes useful",
                "Completely useless"
            ]
            correct_text = "Very necessary or valuable"
        elif target_word.lower() in ['practice', 'practicing']:
            options = [
                "To do something repeatedly to improve",
                "To do something only once",
                "To avoid doing something",
                "To stop doing something"
            ]
            correct_text = "To do something repeatedly to improve"
        elif target_word.lower() in ['communication', 'communicate']:
            options = [
                "To exchange information with others",
                "To keep secrets",
                "To avoid talking",
                "To listen only"
            ]
            correct_text = "To exchange information with others"
        else:
            # 通用词汇选项
            options = [
                f"The word '{target_word}' is used in this context",
                f"Something completely unrelated to '{target_word}'",
                f"The opposite meaning of '{target_word}'",
                f"A word that sounds similar to '{target_word}'"
            ]
            correct_text = f"The word '{target_word}' is used in this context"
        
        shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
        questions.append({
            "id": 1,
            "question": f"What does the word '{target_word}' mean in this text?",
            "options": shuffled_options,
            "correct_answer": new_correct,
            "explanation": f"The word '{target_word}' is used appropriately in the context of the text."
        })
    
    # 题目2：文本主题题
    options = [
        "Learning and education",
        "Food and cooking",
        "Travel and adventure",
        "Sports and games"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 2,
        "question": "What is the main topic of this text?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The text focuses on educational and learning topics."
    })
    
    # 题目3：理解题
    options = [
        "Basic information that is easy to understand",
        "Complex scientific theories",
        "Advanced mathematical concepts",
        "Difficult technical procedures"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 3,
        "question": "What level of information does this text provide?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "This text presents basic, easy-to-understand information suitable for beginners."
    })
    
    return questions

def generate_intermediate_exercises(text: str, key_words: list, sentences: list) -> list:
    """生成中级水平的练习题"""
    questions = []
    
    # 题目1：词汇分析题 - 更合理的选项
    if key_words:
        target_word = random.choice(key_words)
        # 根据词汇生成更合理的选项
        if target_word.lower() in ['effective', 'efficient', 'successful']:
            options = [
                "Working well and producing good results",
                "Working slowly and inefficiently",
                "Not working at all",
                "Working but with many problems"
            ]
            correct_text = "Working well and producing good results"
        elif target_word.lower() in ['develop', 'development', 'developing']:
            options = [
                "To grow or improve over time",
                "To stay the same",
                "To get worse",
                "To disappear completely"
            ]
            correct_text = "To grow or improve over time"
        elif target_word.lower() in ['method', 'approach', 'technique']:
            options = [
                "A way of doing something",
                "A random attempt",
                "A mistake",
                "A problem"
            ]
            correct_text = "A way of doing something"
        else:
            # 通用词汇分析
            options = [
                f"The word '{target_word}' has a specific meaning in this context",
                f"The word '{target_word}' is used incorrectly",
                f"The word '{target_word}' is not important",
                f"The word '{target_word}' is a typo"
            ]
            correct_text = f"The word '{target_word}' has a specific meaning in this context"
        
        shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
        questions.append({
            "id": 1,
            "question": f"What does the word '{target_word}' mean in this context?",
            "options": shuffled_options,
            "correct_answer": new_correct,
            "explanation": f"The word '{target_word}' is used with its proper meaning in this educational context."
        })
    
    # 题目2：语法结构分析题
    options = [
        "A mix of simple and complex sentences",
        "Only very short sentences",
        "Only very long sentences",
        "Only questions"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 2,
        "question": "What sentence structure does this text use?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The text uses a variety of sentence structures to present information clearly."
    })
    
    # 题目3：作者意图题
    options = [
        "To provide educational information",
        "To tell a fictional story",
        "To sell a product",
        "To complain about something"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 3,
        "question": "What is the author trying to do in this text?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The author's main goal is to share educational information with readers."
    })
    
    # 题目4：推理题
    options = [
        "The topic is valuable for learning",
        "The topic is too difficult",
        "The topic is not useful",
        "The topic is only for experts"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 4,
        "question": "What can we conclude about this topic from the text?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The text shows that this topic has educational value and is worth learning."
    })
    
    return questions

def generate_advanced_exercises(text: str, key_words: list, sentences: list) -> list:
    """生成高级水平的练习题"""
    questions = []
    
    # 题目1：高级词汇分析题 - 更合理的选项
    if key_words:
        target_word = random.choice(key_words)
        # 根据词汇生成更合理的选项
        if target_word.lower() in ['sophisticated', 'complex', 'advanced']:
            options = [
                "Highly developed and intellectually challenging",
                "Simple and easy to understand",
                "Outdated and irrelevant",
                "Too basic for serious study"
            ]
            correct_text = "Highly developed and intellectually challenging"
        elif target_word.lower() in ['comprehensive', 'thorough', 'complete']:
            options = [
                "Covering all aspects completely",
                "Covering only basic aspects",
                "Missing important information",
                "Incomplete and fragmented"
            ]
            correct_text = "Covering all aspects completely"
        elif target_word.lower() in ['fundamental', 'essential', 'basic']:
            options = [
                "Of primary importance or necessity",
                "Of secondary importance",
                "Not necessary at all",
                "Completely optional"
            ]
            correct_text = "Of primary importance or necessity"
        else:
            # 通用高级词汇分析
            options = [
                f"The word '{target_word}' carries significant meaning in this academic context",
                f"The word '{target_word}' is used casually without much thought",
                f"The word '{target_word}' is inappropriate for this context",
                f"The word '{target_word}' is a technical error"
            ]
            correct_text = f"The word '{target_word}' carries significant meaning in this academic context"
        
        shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
        questions.append({
            "id": 1,
            "question": f"What is the significance of the word '{target_word}' in this text?",
            "options": shuffled_options,
            "correct_answer": new_correct,
            "explanation": f"The word '{target_word}' is carefully chosen to convey precise meaning in this educational context."
        })
    
    # 题目2：文体分析题
    options = [
        "The writing demonstrates academic rigor and scholarly precision",
        "The writing is too casual for educational content",
        "The writing is overly complex and confusing",
        "The writing lacks any clear structure"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 2,
        "question": "How would you characterize the writing style of this text?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The text employs academic writing conventions with precise language and logical structure."
    })
    
    # 题目3：批判性思维题
    options = [
        "The text presents a well-reasoned argument with supporting evidence",
        "The text makes claims without any supporting evidence",
        "The text contains logical fallacies and contradictions",
        "The text presents only personal opinions without analysis"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 3,
        "question": "How effective is the argument presented in this text?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The text demonstrates strong argumentative structure with logical reasoning and evidence."
    })
    
    # 题目4：综合理解题
    options = [
        "The text integrates multiple concepts to create a comprehensive understanding",
        "The text focuses on only one simple idea",
        "The text presents disconnected information",
        "The text avoids complex topics entirely"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 4,
        "question": "How does this text approach its subject matter?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The text demonstrates sophisticated integration of multiple concepts and perspectives."
    })
    
    # 题目5：高级推理题
    options = [
        "The ideas have important implications for educational practice",
        "The ideas have no relevance beyond this text",
        "The ideas contradict established educational principles",
        "The ideas are too narrow to be meaningful"
    ]
    shuffled_options, new_correct = shuffle_options_and_correct_answer(options, "A")
    questions.append({
        "id": 5,
        "question": "What broader significance do the ideas in this text have?",
        "options": shuffled_options,
        "correct_answer": new_correct,
        "explanation": "The text presents ideas that have meaningful implications for educational theory and practice."
    })
    
    return questions

@app.get("/")
async def root():
    return {"message": "Linguamate Pro API is running with Local AI!"}

@app.post("/upload/text")
async def upload_text(request: dict):
    """处理文本输入并进行语言学分析"""
    try:
        # 从请求中获取参数
        text = request.get("text", "")
        level = request.get("level", "beginner")
        language = request.get("language", "zh")  # 添加语言参数
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="文本内容不能为空")
        
        # 生成模拟的语言学分析
        analysis = generate_mock_analysis(text, level, language)
        
        # 保存学习记录
        record_id = save_learning_record("text_analysis", level, text, analysis, language=language)
        
        return {
            "success": True,
            "analysis": analysis,
            "record_id": record_id
        }
        
    except Exception as e:
        print(f"文本分析错误: {e}")
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")

def generate_mock_analysis(text: str, level: str, language: str = "zh"):
    """生成模拟的语言学分析 - 根据学习等级调整分析深度和复杂度"""
    # 基本文本统计
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    avg_sentence_length = word_count / len(sentences) if sentences else 0
    
    # 根据学习等级调整分析深度
    if level == "beginner":
        return generate_beginner_analysis(text, word_count, char_count, sentences, avg_sentence_length)
    elif level == "intermediate":
        return generate_intermediate_analysis(text, word_count, char_count, sentences, avg_sentence_length)
    else:  # advanced
        return generate_advanced_analysis(text, word_count, char_count, sentences, avg_sentence_length)

def generate_beginner_analysis(text: str, word_count: int, char_count: int, sentences: list, avg_sentence_length: float) -> str:
    """生成初级水平的分析报告"""
    words = text.split()
    
    # 简单词汇分析
    import re
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'there', 'here', 'where', 'when', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose'}
    
    filtered_words = []
    for word in words:
        clean_word = re.sub(r'[^a-zA-Z]', '', word.lower())
        if clean_word and len(clean_word) > 2 and clean_word not in stop_words:
            filtered_words.append(clean_word)
    
    common_words = filtered_words[:min(5, len(filtered_words))]
    
    return f"""Linguistic Analysis Report (Beginner Level)

📝 Basic Text Information:
- Character count: {char_count}
- Word count: {word_count}
- Sentence count: {len(sentences)}
- Average sentence length: {avg_sentence_length:.1f} words
- Learning level: Beginner

🔍 Simple Vocabulary Analysis:
- Main word types: Common nouns, basic verbs, simple adjectives
- Vocabulary difficulty: Basic level appropriate
- Key vocabulary: {', '.join(common_words) if common_words else 'No significant vocabulary detected'}
- Text complexity: Simple and clear for beginners

📚 Basic Grammar Structure:
- Sentence types: Simple sentences with basic structure
- Grammar features: Subject-verb-object pattern
- Grammar complexity: Basic level structures
- Syntactic patterns: Simple English sentence patterns

💡 Simple Meaning Analysis:
- Topic: Basic informational content
- Context: Everyday language learning material
- Cultural background: Simple English expressions
- Meaning coherence: Clear and straightforward text

🎯 Beginner Learning Recommendations:
- Focus areas: Basic vocabulary and simple grammar
- Practice suggestions: Reading simple sentences and basic vocabulary
- Extended learning: Common words and phrases
- Skill development: Basic reading comprehension

📖 Simple Reading Practice:
Recommended: Practice with similar basic level texts to build confidence."""

def generate_intermediate_analysis(text: str, word_count: int, char_count: int, sentences: list, avg_sentence_length: float) -> str:
    """生成中级水平的分析报告"""
    words = text.split()
    
    # 中级词汇分析
    import re
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'there', 'here', 'where', 'when', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose'}
    
    filtered_words = []
    for word in words:
        clean_word = re.sub(r'[^a-zA-Z]', '', word.lower())
        if clean_word and len(clean_word) > 2 and clean_word not in stop_words:
            filtered_words.append(clean_word)
    
    common_words = filtered_words[:min(8, len(filtered_words))]
    
    return f"""Linguistic Analysis Report (Intermediate Level)

📝 Comprehensive Text Information:
- Character count: {char_count}
- Word count: {word_count}
- Sentence count: {len(sentences)}
- Average sentence length: {avg_sentence_length:.1f} words
- Learning level: Intermediate

🔍 Detailed Vocabulary Analysis:
- Main word types: Nouns, verbs, adjectives, adverbs, prepositions
- Vocabulary difficulty: Intermediate level with some complex terms
- Key vocabulary: {', '.join(common_words) if common_words else 'No significant vocabulary detected'}
- Text complexity: Moderate complexity suitable for intermediate learners
- Word formation patterns: Compound words and common prefixes/suffixes

📚 Intermediate Grammar Structure:
- Sentence types: Simple, compound, and some complex sentences
- Grammar features: Subject-verb-object structure with modifiers and clauses
- Grammar complexity: Intermediate level structures including conditionals
- Syntactic patterns: Standard English with some advanced constructions
- Verb tenses: Present, past, future with perfect and continuous forms

💡 Contextual Meaning Analysis:
- Topic: Educational or professional content
- Context: Intermediate level reading material
- Cultural background: Standard English expressions and idioms
- Meaning coherence: Well-structured with clear logical flow
- Inference requirements: Some implied meanings and context clues

🎯 Intermediate Learning Recommendations:
- Focus areas: Expanding vocabulary and complex grammar structures
- Practice suggestions: Reading comprehension with inference questions
- Extended learning: Academic vocabulary and writing skills
- Skill development: Critical thinking and text analysis

📖 Advanced Reading Practice:
Recommended: Engage with intermediate-level articles and short stories to develop analytical skills."""

def generate_advanced_analysis(text: str, word_count: int, char_count: int, sentences: list, avg_sentence_length: float) -> str:
    """生成高级水平的分析报告"""
    words = text.split()
    
    # 高级词汇分析
    import re
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'there', 'here', 'where', 'when', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose'}
    
    filtered_words = []
    for word in words:
        clean_word = re.sub(r'[^a-zA-Z]', '', word.lower())
        if clean_word and len(clean_word) > 2 and clean_word not in stop_words:
            filtered_words.append(clean_word)
    
    common_words = filtered_words[:min(12, len(filtered_words))]
    
    return f"""Comprehensive Linguistic Analysis Report (Advanced Level)

📝 Detailed Text Statistics:
- Character count: {char_count}
- Word count: {word_count}
- Sentence count: {len(sentences)}
- Average sentence length: {avg_sentence_length:.1f} words
- Learning level: Advanced

🔍 Sophisticated Vocabulary Analysis:
- Main word types: Complex nouns, sophisticated verbs, nuanced adjectives, literary adverbs
- Vocabulary difficulty: Advanced level with academic and specialized terminology
- Key vocabulary: {', '.join(common_words) if common_words else 'No significant vocabulary detected'}
- Text complexity: High complexity requiring advanced comprehension skills
- Word formation: Advanced morphological patterns, Latin/Greek roots, technical terminology
- Register analysis: Formal to academic register with stylistic variation

📚 Advanced Grammar Structure:
- Sentence types: Complex sentences with multiple clauses and sophisticated constructions
- Grammar features: Advanced syntax including subordination, nominalization, and passive voice
- Grammar complexity: Advanced structures including conditional perfects, subjunctive mood
- Syntactic patterns: Sophisticated English with literary and academic constructions
- Discourse markers: Advanced connectors and transitional phrases
- Stylistic devices: Metaphor, alliteration, and other rhetorical techniques

💡 Sophisticated Semantic Analysis:
- Topic: Complex academic, professional, or literary content
- Context: Advanced reading material with cultural and historical references
- Cultural background: Nuanced cultural expressions and contextual implications
- Meaning coherence: Sophisticated logical structure with implicit meanings
- Inference requirements: Complex implied meanings, cultural allusions, and contextual nuances
- Pragmatic analysis: Speaker intention, implicature, and contextual appropriateness

🎯 Advanced Learning Recommendations:
- Focus areas: Academic vocabulary, complex grammar, and critical analysis
- Practice suggestions: Advanced reading comprehension with critical thinking questions
- Extended learning: Research skills, academic writing, and literary analysis
- Skill development: Advanced analytical thinking and sophisticated communication
- Cultural competence: Understanding cultural context and implicit meanings

📖 Advanced Reading Practice:
Recommended: Engage with academic papers, literature, and complex texts to develop sophisticated language skills and critical thinking abilities."""

@app.post("/generate-exercises")
async def generate_exercises(request: ExerciseRequest):
    """基于文本和分析生成练习题"""
    try:
        # 从请求中获取参数
        text = request.text
        analysis = request.analysis
        level = request.level
        
        # 生成基于内容的练习题
        questions = generate_content_based_exercises(text, analysis, level)
        
        # 保存学习记录（练习生成）
        record_id = save_learning_record("exercise_generation", level, text, analysis, questions)
        
        return {
            "success": True,
            "exercises": questions,
            "exercise_id": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "record_id": record_id
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
        
        # 获取选项列表
        options = question.get("options", [])
        correct_answer_letter = question.get("correct_answer", "")
        
        # 将用户选择的选项内容转换为选项字母
        user_answer_letter = ""
        for i, option in enumerate(options):
            if option == user_answer:
                user_answer_letter = chr(65 + i)  # A, B, C, D
                break
        
        # 获取正确答案的选项内容
        correct_answer_content = ""
        if correct_answer_letter and len(correct_answer_letter) == 1:
            letter_index = ord(correct_answer_letter.upper()) - 65
            if 0 <= letter_index < len(options):
                correct_answer_content = options[letter_index]
        
        # 检查答案是否正确
        is_correct = user_answer_letter.upper() == correct_answer_letter.upper()
        
        return {
            "success": True,
            "is_correct": is_correct,
            "correct_answer": correct_answer_content,
            "explanation": question.get("explanation", ""),
            "user_answer": user_answer
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交答案失败: {str(e)}")

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """与AI进行自然对话练习 - 支持上下文记忆和角色扮演"""
    try:
        # 从请求中获取参数
        message = request.message
        context = request.context  # 对话场景 (restaurant, shopping, direction, introduction, custom_xxx)
        level = request.level
        conversation_history = request.conversation_history or []
        custom_scenario_name = request.custom_scenario_name
        custom_scenario_description = request.custom_scenario_description
        
        # 生成AI回复（使用改进的自然对话逻辑）
        ai_response = generate_natural_ai_response(
            message=message,
            scenario=context,
            level=level,
            conversation_history=conversation_history,
            custom_scenario_name=custom_scenario_name,
            custom_scenario_description=custom_scenario_description
        )
        
        # 保存学习记录（AI对话）
        conversation_content = f"User: {message}\nAI: {ai_response}"
        record_id = save_learning_record("chat_practice", level, conversation_content, context=context)
        
        return {
            "success": True,
            "response": ai_response,
            "record_id": record_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")

@app.post("/chat-simple")
async def chat_with_ai_simple(request: SimpleChatRequest):
    """
    优化的AI聊天接口 - 符合您的要求
    
    特性：
    1. 上下文记忆功能：维护conversation_history列表
    2. 英语口语练习场景：友好的餐厅服务员角色
    3. 接口设计：接受{ "message": "用户输入" }，返回{ "reply": "AI回复" }
    4. 安全与健壮性：对话历史截断和异常处理
    5. 使用本地模型：不依赖外部API
    """
    global conversation_history
    
    try:
        user_message = request.message.strip()
        
        if not user_message:
            return {
                "reply": "I'm here to help you practice English! Please share something with me."
            }
        
        # 将用户消息添加到对话历史
        conversation_history.append({
            "user_message": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # 如果对话历史超过20轮，截取最近10轮
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-10:]
        
        # 生成AI回复（使用优化的本地AI逻辑）
        ai_reply = generate_optimized_ai_response(user_message, conversation_history)
        
        # 将AI回复添加到对话历史
        conversation_history.append({
            "ai_response": ai_reply,
            "timestamp": datetime.now().isoformat()
        })
        
        # 保存学习记录
        conversation_content = f"User: {user_message}\nAI: {ai_reply}"
        save_learning_record("chat_practice", "beginner", conversation_content, context="restaurant_waiter")
        
        return {
            "reply": ai_reply
        }
        
    except Exception as e:
        # 异常处理，防止程序崩溃
        print(f"Chat error: {e}")
        return {
            "reply": "I'm sorry, I encountered an issue. Could you please try again? I'm here to help you practice English!"
        }

# 图片上传和OCR识别
@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...), level: str = "beginner", language: str = "zh"):
    """上传图片并进行OCR识别"""
    try:
        # 检查文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        
        # 读取图片数据
        image_data = await file.read()
        
        # 使用PIL打开图片
        image = Image.open(io.BytesIO(image_data))
        
        # 进行OCR识别
        try:
            # 使用pytesseract进行OCR (只使用英文)
            extracted_text = pytesseract.image_to_string(image, lang='eng')
            
            # 清理文本
            extracted_text = extracted_text.strip()
            
            if not extracted_text:
                error_msg = "No text content detected, please try another image" if language == "en" else "未检测到文本内容，请尝试其他图片"
                return {
                    "success": False,
                    "error": error_msg
                }
            
            # 生成语言学分析
            analysis = generate_mock_analysis(extracted_text, level, language)
            
            # 保存学习记录
            record_id = save_learning_record("image_analysis", level, extracted_text, analysis, language=language)
            
            return {
                "success": True,
                "extracted_text": extracted_text,
                "analysis": analysis,
                "filename": file.filename,
                "record_id": record_id
            }
            
        except Exception as ocr_error:
            # 如果OCR失败，提供更真实的模拟文本
            print(f"OCR Error: {ocr_error}")
            
            # 根据文件名和语言生成更真实的模拟文本
            filename = file.filename.lower() if file.filename else ""
            
            if language == "en":
                if "textbook" in filename or "book" in filename:
                    mock_text = "Chapter 1: Introduction to Language Learning\n\nLanguage learning is a complex process that involves multiple cognitive skills. Students need to develop vocabulary, grammar, and communication skills through various methods including reading, writing, listening, and speaking practice."
                elif "document" in filename or "paper" in filename:
                    mock_text = "Document Analysis\n\nThis document contains important information about language acquisition theories and practical applications in educational settings. The content covers various methodologies and approaches to language teaching."
                elif "test" in filename or "exam" in filename:
                    mock_text = "Test Questions\n\n1. What is the main purpose of this text?\n2. Identify the key vocabulary words.\n3. Explain the grammar structure used.\n4. Summarize the main ideas presented."
                else:
                    mock_text = "Sample Text from Image\n\nThis is text content that would normally be extracted from the uploaded image using OCR technology. The text appears to contain educational or informational content suitable for language analysis."
                
                note_msg = "Note: Tesseract OCR engine is not installed. This is simulated text for demonstration purposes. To enable real OCR, please install Tesseract OCR engine. See TESSERACT_INSTALLATION_GUIDE.md for detailed installation instructions."
            else:
                if "textbook" in filename or "book" in filename:
                    mock_text = "第一章：语言学习入门\n\n语言学习是一个复杂的过程，涉及多种认知技能。学生需要通过阅读、写作、听力和口语练习等多种方法发展词汇、语法和交际技能。"
                elif "document" in filename or "paper" in filename:
                    mock_text = "文档分析\n\n本文档包含关于语言习得理论和教育实践应用的重要信息。内容涵盖各种语言教学的方法和途径。"
                elif "test" in filename or "exam" in filename:
                    mock_text = "测试题目\n\n1. 这段文本的主要目的是什么？\n2. 识别关键词汇。\n3. 解释使用的语法结构。\n4. 总结主要观点。"
                else:
                    mock_text = "图片中的示例文本\n\n这是通常使用OCR技术从上传图片中提取的文本内容。文本似乎包含适合语言分析的教育或信息内容。"
                
                note_msg = "注意：Tesseract OCR引擎未安装。这是用于演示的模拟文本。要启用真实OCR，请安装Tesseract OCR引擎。详细安装说明请查看TESSERACT_INSTALLATION_GUIDE.md文件。"
            
            mock_analysis = generate_mock_analysis(mock_text, level, language)
            
            # 保存学习记录
            record_id = save_learning_record("image_analysis", level, mock_text, mock_analysis, language=language)
            
            return {
                "success": True,
                "extracted_text": mock_text,
                "analysis": mock_analysis,
                "filename": file.filename,
                "note": note_msg,
                "record_id": record_id
            }
        
    except Exception as e:
        error_msg = f"Image processing failed: {str(e)}" if language == "en" else f"图片处理失败: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/learning-records")
async def create_learning_record(
    record_type: str,
    level: str,
    content: str,
    analysis: str = None,
    exercises: str = None,
    score: int = None,
    language: str = "zh",
    context: str = None
):
    """保存学习记录"""
    try:
        import json
        exercises_data = None
        if exercises:
            try:
                exercises_data = json.loads(exercises)
            except:
                exercises_data = exercises

        record_id = save_learning_record(
            record_type=record_type,
            level=level,
            content=content,
            analysis=analysis,
            exercises=exercises_data,
            score=score,
            language=language,
            context=context
        )

        return {
            "success": True,
            "record_id": record_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存学习记录失败：{str(e)}")

@app.get("/learning-records")
async def get_learning_records():
    """获取学习记录"""
    try:
        # 按时间倒序排列（最新的在前）
        sorted_records = sorted(learning_records, key=lambda x: x['timestamp'], reverse=True)
        
        return {
            "success": True,
            "records": sorted_records,
            "total": len(sorted_records)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取学习记录失败: {str(e)}")

@app.get("/learning-records/{record_id}")
async def get_learning_record(record_id: str):
    """获取特定学习记录"""
    try:
        record = next((r for r in learning_records if r['id'] == record_id), None)
        if not record:
            raise HTTPException(status_code=404, detail="学习记录不存在")
        
        return {
            "success": True,
            "record": record
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取学习记录失败: {str(e)}")

@app.delete("/learning-records")
async def clear_all_learning_records():
    """清除所有学习记录"""
    try:
        global learning_records
        cleared_count = len(learning_records)
        learning_records.clear()
        
        return {
            "success": True,
            "message": f"Successfully cleared {cleared_count} learning records" if cleared_count > 0 else "No records to clear",
            "cleared_count": cleared_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除学习记录失败: {str(e)}")

@app.delete("/chat-history")
async def clear_chat_history():
    """清除对话历史"""
    try:
        global conversation_history
        cleared_count = len(conversation_history)
        conversation_history.clear()
        
        return {
            "success": True,
            "message": f"Successfully cleared {cleared_count} conversation records" if cleared_count > 0 else "No conversation history to clear",
            "cleared_count": cleared_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清除对话历史失败: {str(e)}")

@app.get("/chat-history")
async def get_chat_history():
    """获取当前对话历史"""
    try:
        global conversation_history
        return {
            "success": True,
            "conversation_history": conversation_history,
            "total_turns": len(conversation_history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取对话历史失败: {str(e)}")

def generate_optimized_ai_response(user_message: str, conversation_history: List[dict]) -> str:
    """
    生成优化的AI回复 - 符合您的要求
    
    角色设定：友好的餐厅服务员，帮助学生练习英文口语对话
    特性：
    - 自然、简短（2-3句），语气友好
    - 轻微语法纠正提示
    - 基于对话历史保持上下文连贯性
    - 使用本地模型，无需外部API
    """
    message_lower = user_message.lower()
    
    # 分析对话历史和用户情绪
    context = analyze_conversation_context(conversation_history, user_message, True)  # 强制英文
    
    # 检测语法错误并提供轻微纠正
    grammar_hint = detect_grammar_issues(user_message)
    
    # 生成餐厅服务员角色的回复
    ai_reply = generate_restaurant_waiter_response(user_message, message_lower, context, conversation_history)
    
    # 如果有语法错误，在回复末尾添加轻微纠正提示
    if grammar_hint:
        ai_reply += f" {grammar_hint}"
    
    return ai_reply

def detect_grammar_issues(message: str) -> str:
    """检测语法错误并提供轻微纠正提示"""
    message_lower = message.lower()
    
    # 检测常见语法错误
    if "i am" in message_lower and not any(word in message_lower for word in ["happy", "tired", "hungry", "excited"]):
        return "(Just a small tip: 'I am' is usually followed by an adjective or noun. For example: 'I am hungry' or 'I am a student')"
    
    if "i have" in message_lower and not any(word in message_lower for word in ["a", "an", "some", "many", "much"]):
        return "(Quick tip: 'I have' is usually followed by 'a/an/some'. For example: 'I have a question')"
    
    if "i want" in message_lower and not any(word in message_lower for word in ["to", "a", "an", "some"]):
        return "(Small correction: 'I want' is usually followed by 'to' + verb or 'a/an/some' + noun. For example: 'I want to eat' or 'I want some water')"
    
    if "i like" in message_lower and not any(word in message_lower for word in ["to", "a", "an", "some", "very"]):
        return "(Tip: 'I like' is usually followed by 'to' + verb or 'a/an/some' + noun. For example: 'I like to read' or 'I like pizza')"
    
    # 检查时态一致性
    if any(word in message_lower for word in ["yesterday", "last week", "last month"]) and "ed" not in message_lower:
        return "(Quick tip: When talking about the past, use past tense verbs. For example: 'I went' instead of 'I go')"
    
    return ""

def generate_restaurant_waiter_response(message: str, message_lower: str, context: dict, conversation_history: List[dict]) -> str:
    """生成餐厅服务员角色的回复"""
    
    # 分析对话长度和上下文
    conversation_length = len([item for item in conversation_history if "user_message" in item])
    
    # 根据用户输入生成情境化回复
    if any(word in message_lower for word in ["hello", "hi", "good morning", "good afternoon", "good evening"]):
        responses = [
            "Good evening! Welcome to our restaurant. I'm your server today. How can I help you?",
            "Hello there! Welcome! I'm here to make your dining experience wonderful. What can I do for you?",
            "Hi! Great to see you! I'm your waiter today. How are you doing this evening?"
        ]
    
    elif any(word in message_lower for word in ["menu", "food", "eat", "hungry", "order"]):
        responses = [
            "Great! I'd love to tell you about our menu. We have wonderful pasta, fresh seafood, and delicious steaks. What sounds good to you?",
            "Perfect! Our chef's special today is amazing. We also have excellent vegetarian options. What type of food are you in the mood for?",
            "Wonderful! Our menu features fresh, local ingredients. Do you prefer something light or hearty tonight?"
        ]
    
    elif any(word in message_lower for word in ["recommend", "suggest", "best", "popular"]):
        responses = [
            "I'd highly recommend our signature pasta dish - it's absolutely delicious! Would you like to try it?",
            "Our grilled salmon is very popular and always fresh. How does that sound to you?",
            "If you like spicy food, our curry is fantastic! What's your spice preference?"
        ]
    
    elif any(word in message_lower for word in ["price", "cost", "expensive", "cheap", "budget"]):
        responses = [
            "Our prices are very reasonable! Most entrees are between $15-25. Would you like to see our menu?",
            "We have great value meals tonight! Our lunch specials are particularly good deals. Interested?",
            "I can show you our budget-friendly options too. What's your price range?"
        ]
    
    elif any(word in message_lower for word in ["drink", "beverage", "wine", "beer", "water", "coffee", "tea"]):
        responses = [
            "We have a wonderful selection of beverages! Fresh juices, coffee, tea, and a nice wine list. What would you like to drink?",
            "Great question! We offer fresh local juices, imported wines, and craft beers. What's your preference?",
            "I'd recommend our house wine - it's excellent! Or we have fresh lemonade if you prefer something lighter."
        ]
    
    elif any(word in message_lower for word in ["thank", "thanks", "appreciate"]):
        responses = [
            "You're so welcome! I'm happy to help. Is there anything else I can do for you?",
            "My pleasure! That's what I'm here for. How's everything tasting so far?",
            "You're very welcome! I love making sure our guests have a great experience. Anything else?"
        ]
    
    elif any(word in message_lower for word in ["delicious", "good", "great", "amazing", "wonderful", "excellent"]):
        responses = [
            "I'm so glad you're enjoying it! That makes me happy. Would you like to try our dessert menu?",
            "Wonderful! I love hearing that. Our chef will be pleased. How's everything else?",
            "Fantastic! You made a great choice. Is there anything else I can bring you?"
        ]
    
    elif any(word in message_lower for word in ["problem", "issue", "wrong", "bad", "cold", "hot"]):
        responses = [
            "Oh no! I'm so sorry about that. Let me fix this right away. What exactly is the issue?",
            "I apologize for that! Let me take care of this immediately. Can you tell me what's wrong?",
            "I'm sorry to hear that! Let me make this right for you. What can I do to help?"
        ]
    
    elif any(word in message_lower for word in ["bill", "check", "pay", "payment", "done", "finished"]):
        responses = [
            "Of course! I'll bring your check right away. How was everything tonight?",
            "Absolutely! Let me get that for you. I hope you had a wonderful dining experience!",
            "Sure thing! I'll be right back with your bill. Thank you for choosing our restaurant!"
        ]
    
    elif any(word in message_lower for word in ["bye", "goodbye", "see you", "leaving"]):
        responses = [
            "Thank you so much for coming! Have a wonderful evening and we hope to see you again soon!",
            "It was a pleasure serving you tonight! Take care and come back to see us again!",
            "Goodbye! Thank you for choosing our restaurant. We look forward to welcoming you back!"
        ]
    
    else:
        # 基于对话历史的通用回复
        if conversation_length == 0:
            responses = [
                "Hello! Welcome to our restaurant. I'm your server today. How can I help you this evening?",
                "Good evening! I'm here to make your dining experience wonderful. What brings you in tonight?",
                "Hi there! Welcome! I'm your waiter. How are you doing today?"
            ]
        elif conversation_length < 3:
            responses = [
                "That's interesting! Tell me more about that. Are you ready to order, or do you have any questions?",
                "I'd love to help with that! Is there anything specific you'd like to know about our menu?",
                "Great! I'm here to help. What would you like to explore on our menu tonight?"
            ]
        else:
            responses = [
                "I'm really enjoying our conversation! How can I continue to help you tonight?",
                "You're so interesting to talk to! Is there anything else you'd like to know about our restaurant?",
                "I love chatting with you! What else can I help you with this evening?"
            ]
    
    # 根据用户情绪调整回复
    mood = context.get("mood", "neutral")
    if mood == "positive":
        # 在积极回复前加上热情回应
        positive_prefixes = ["That's wonderful!", "I'm so happy to hear that!", "Fantastic!"]
        return f"{random.choice(positive_prefixes)} {random.choice(responses)}"
    elif mood == "negative":
        # 在消极回复前加上同情回应
        empathetic_prefixes = ["I'm sorry to hear that.", "That sounds tough.", "I understand how you feel."]
        return f"{random.choice(empathetic_prefixes)} {random.choice(responses)}"
    else:
        return random.choice(responses)

def generate_natural_ai_response(message: str, scenario: str, level: str, conversation_history: List[dict], custom_scenario_name: str = None, custom_scenario_description: str = None) -> str:
    """
    生成自然的AI回复 - 支持上下文记忆、角色扮演和自定义场景
    
    优化特性：
    1. 保存并使用最近5轮对话上下文
    2. 角色化系统提示，模拟真实对话伙伴
    3. 人性化回复，有情感表达和自然语气
    4. 简洁回复（不超过80字）
    5. 场景化角色扮演
    
    Args:
        message: 用户消息
        scenario: 对话场景 (restaurant, shopping, direction, introduction, custom_xxx)
        level: 用户语言水平 (beginner, intermediate, advanced)
        conversation_history: 对话历史记录
        custom_scenario_name: 自定义场景名称
        custom_scenario_description: 自定义场景描述
    
    Returns:
        自然的AI回复
    """
    # 检测用户输入语言
    message_lower = message.lower()
    is_english = detect_language(message)
    
    # 构建对话上下文（最近5轮对话）
    recent_history = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
    
    # 分析对话历史和用户情绪
    conversation_context = analyze_conversation_context(recent_history, message, is_english)
    
    # 生成角色化的系统提示
    system_prompt = generate_enhanced_system_prompt(scenario, level, is_english, custom_scenario_name, custom_scenario_description)
    
    # 生成自然回复
    if is_english:
        return generate_enhanced_english_response(message, message_lower, scenario, level, conversation_context, custom_scenario_name, custom_scenario_description)
    else:
        return generate_enhanced_chinese_response(message, message_lower, scenario, level, conversation_context, custom_scenario_name, custom_scenario_description)

def analyze_conversation_context(conversation_history: List[dict], current_message: str, is_english: bool) -> dict:
    """
    分析对话上下文，包括用户情绪、话题变化、对话节奏等
    
    Args:
        conversation_history: 对话历史
        current_message: 当前用户消息
        is_english: 是否为英文
    
    Returns:
        包含上下文信息的字典
    """
    context = {
        "mood": "neutral",
        "topic": "general",
        "urgency": "normal",
        "conversation_length": len(conversation_history),
        "is_first_message": len(conversation_history) == 0,
        "recent_topics": [],
        "user_engagement": "medium"
    }
    
    message_lower = current_message.lower()
    
    # 分析用户情绪
    if is_english:
        positive_words = ["happy", "excited", "great", "wonderful", "amazing", "love", "enjoy", "fantastic", "awesome"]
        negative_words = ["sad", "tired", "angry", "worried", "nervous", "frustrated", "upset", "disappointed"]
        urgent_words = ["help", "urgent", "emergency", "problem", "issue", "trouble", "asap"]
    else:
        positive_words = ["开心", "高兴", "兴奋", "棒", "喜欢", "享受", "太棒了", "很好"]
        negative_words = ["难过", "累", "生气", "担心", "紧张", "沮丧", "失望", "烦恼"]
        urgent_words = ["帮助", "紧急", "问题", "麻烦", "急", "快"]
    
    if any(word in message_lower for word in positive_words):
        context["mood"] = "positive"
    elif any(word in message_lower for word in negative_words):
        context["mood"] = "negative"
    elif any(word in message_lower for word in urgent_words):
        context["urgency"] = "high"
    
    # 分析话题
    if is_english:
        topic_keywords = {
            "food": ["food", "eat", "restaurant", "cook", "meal", "hungry", "taste", "delicious"],
            "weather": ["weather", "sunny", "rainy", "cloudy", "hot", "cold", "temperature"],
            "work": ["work", "job", "career", "office", "meeting", "project", "boss"],
            "study": ["study", "learn", "practice", "homework", "exam", "test", "school", "class"],
            "travel": ["travel", "trip", "vacation", "holiday", "flight", "hotel", "destination"],
            "family": ["family", "parent", "mother", "father", "sister", "brother", "child"]
        }
    else:
        topic_keywords = {
            "food": ["食物", "吃", "餐厅", "做饭", "饭", "饿", "味道", "美味"],
            "weather": ["天气", "晴天", "下雨", "阴天", "热", "冷", "温度"],
            "work": ["工作", "职业", "办公室", "会议", "项目", "老板"],
            "study": ["学习", "练习", "作业", "考试", "测试", "学校", "课堂"],
            "travel": ["旅行", "旅游", "假期", "航班", "酒店", "目的地"],
            "family": ["家庭", "父母", "母亲", "父亲", "姐妹", "兄弟", "孩子"]
        }
    
    for topic, keywords in topic_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            context["topic"] = topic
            break
    
    # 分析对话长度和参与度
    if len(conversation_history) > 10:
        context["user_engagement"] = "high"
    elif len(conversation_history) < 3:
        context["user_engagement"] = "low"
    
    return context

def generate_enhanced_system_prompt(scenario: str, level: str, is_english: bool, custom_scenario_name: str = None, custom_scenario_description: str = None) -> str:
    """
    生成增强的系统提示，定义AI角色和对话风格
    
    Args:
        scenario: 对话场景
        level: 用户语言水平
        is_english: 是否为英文
        custom_scenario_name: 自定义场景名称
        custom_scenario_description: 自定义场景描述
    
    Returns:
        系统提示字符串
    """
    
    # 处理自定义场景
    if scenario and scenario.startswith('custom_') and custom_scenario_name and custom_scenario_description:
        if is_english:
            base_prompt = f"You are a friendly and helpful conversation partner in a {custom_scenario_name.lower()} scenario. {custom_scenario_description}. You are practicing natural conversation with the user."
        else:
            base_prompt = f"你是在{custom_scenario_name}场景中的一名友好的对话伙伴。{custom_scenario_description}。你正在与用户进行自然对话练习。"
    else:
        # 预定义场景
        if scenario == "restaurant":
            if is_english:
                base_prompt = "You are a friendly waiter/waitress at a nice restaurant. You're helping the customer with their order and making them feel welcome. Keep the conversation natural and helpful."
            else:
                base_prompt = "你是一家餐厅的友好服务员。你正在帮助顾客点餐并让他们感到受欢迎。保持对话自然和有用。"
        elif scenario == "shopping":
            if is_english:
                base_prompt = "You are a helpful sales assistant in a store. You're assisting the customer with their shopping needs and providing friendly service. Be enthusiastic but not pushy."
            else:
                base_prompt = "你是一家商店的销售助手。你正在帮助顾客购物需求并提供友好服务。要热情但不要过于推销。"
        elif scenario == "direction":
            if is_english:
                base_prompt = "You are a helpful local person who knows the area well. You're giving directions to someone who's lost or needs help finding a place. Be patient and clear."
            else:
                base_prompt = "你是一个熟悉当地的热心人。你正在为迷路或需要找地方的人指路。要耐心和清晰。"
        elif scenario == "introduction":
            if is_english:
                base_prompt = "You are meeting someone new for the first time. You're friendly, curious about them, and want to get to know them better. Ask questions and share about yourself too."
            else:
                base_prompt = "你正在第一次见到一个新朋友。你很友好，对他们感到好奇，想要更好地了解他们。要问问题，也分享你自己的情况。"
        else:
            if is_english:
                base_prompt = "You are a friendly English conversation partner helping the user practice natural conversation. Stay in character, ask small questions back, and keep a casual, natural tone."
            else:
                base_prompt = "你是一个友好的中文对话伙伴，帮助用户练习自然对话。保持角色，问一些小问题，保持随意的自然语调。"
    
    # 根据语言水平调整
    if level == "beginner":
        if is_english:
            base_prompt += " Use simple vocabulary and clear sentences suitable for beginners. Keep responses under 60 words."
        else:
            base_prompt += " 使用简单的词汇和清晰的句子，适合初学者。回复不超过60字。"
    elif level == "intermediate":
        if is_english:
            base_prompt += " Use intermediate-level vocabulary and slightly more complex sentences. Keep responses under 80 words."
        else:
            base_prompt += " 使用中级词汇和稍微复杂的句子。回复不超过80字。"
    else:  # advanced
        if is_english:
            base_prompt += " Use advanced vocabulary and complex sentence structures when appropriate. Keep responses under 100 words but make them sophisticated."
        else:
            base_prompt += " 适当使用高级词汇和复杂句式。回复不超过100字，但要使其更复杂。"
    
    # 添加通用指导原则
    if is_english:
        base_prompt += " Be empathetic, show genuine interest, and respond naturally as a human would. Ask follow-up questions to keep the conversation flowing."
    else:
        base_prompt += " 要富有同理心，表现出真正的兴趣，像人类一样自然地回应。问后续问题来保持对话流畅。"
    
    return base_prompt

def detect_language(message: str) -> bool:
    """检测消息语言 - True为英文，False为中文"""
    # 计算英文字符比例
    english_chars = sum(1 for char in message if char.isalpha() and ord(char) < 128)
    total_chars = sum(1 for char in message if char.isalpha())
    
    # 如果英文字符占80%以上，认为是英文
    is_english = total_chars > 0 and english_chars / total_chars > 0.8
    
    # 特殊情况：如果包含明显的英文关键词，强制识别为英文
    english_keywords = ["hello", "hi", "how", "what", "where", "when", "why", "thank", "goodbye", "bye", "sorry", "help", "trouble", "homework", "weather", "feeling", "sad", "today", "like", "later", "see", "you", "good", "nice", "great", "yes", "no", "please"]
    if any(word in message.lower() for word in english_keywords):
        is_english = True
    
    # 如果包含中文字符，强制识别为中文
    if any('\u4e00' <= char <= '\u9fff' for char in message):
        is_english = False
    
    return is_english

def generate_system_prompt(scenario: str, level: str, is_english: bool, custom_scenario_name: str = None, custom_scenario_description: str = None) -> str:
    """根据场景生成角色化的系统提示"""
    
    # 处理自定义场景
    if scenario and scenario.startswith('custom_') and custom_scenario_name and custom_scenario_description:
        if is_english:
            base_prompt = f"You are a helpful assistant in a {custom_scenario_name.lower()} scenario. {custom_scenario_description}. Keep responses natural, engaging, and under 80 words. Ask follow-up questions to help the user practice effectively."
        else:
            base_prompt = f"你是在{custom_scenario_name}场景中的一名助手。{custom_scenario_description}。保持回复自然、引人入胜，不超过80字。提出问题来帮助用户有效练习。"
    else:
        # 预定义场景
        if is_english:
            prompts = {
                "restaurant": "You are a friendly and professional restaurant server. You're helping a customer with their dining experience. Keep responses natural, warm, and under 80 words. Ask follow-up questions to engage the customer.",
                "shopping": "You are a helpful and enthusiastic store assistant. You're helping a customer find what they need. Be friendly, ask about their preferences, and keep responses under 80 words.",
                "direction": "You are a helpful local person giving directions. You're familiar with the area and want to help someone find their way. Be clear, friendly, and keep responses under 80 words.",
                "introduction": "You are a friendly person meeting someone new. You're interested in getting to know them better. Be warm, ask questions, and keep responses under 80 words."
            }
        else:
            prompts = {
                "restaurant": "你是一名友好专业的餐厅服务员。你正在帮助顾客用餐体验。保持回复自然、温暖，不超过80字。提出问题来与顾客互动。",
                "shopping": "你是一名乐于助人且热情的商店助手。你正在帮助顾客找到他们需要的东西。要友好，询问他们的偏好，回复不超过80字。",
                "direction": "你是一名乐于助人的当地人，正在指路。你对这个地区很熟悉，想帮助别人找到路。要清晰、友好，回复不超过80字。",
                "introduction": "你是一个友好的人，正在认识新朋友。你想更好地了解他们。要温暖，提出问题，回复不超过80字。"
            }
        
        base_prompt = prompts.get(scenario, prompts.get("introduction", ""))
    
    # 根据语言水平调整
    if level == "beginner" and is_english:
        base_prompt += " Use simple vocabulary and clear sentences suitable for beginners."
    elif level == "beginner" and not is_english:
        base_prompt += " 使用简单的词汇和清晰的句子，适合初学者。"
    
    return base_prompt

def generate_enhanced_english_response(message: str, message_lower: str, scenario: str, level: str, conversation_context: dict, custom_scenario_name: str = None, custom_scenario_description: str = None) -> str:
    """
    生成增强的英文回复 - 更加自然、人性化，有情感表达
    
    Args:
        message: 用户消息
        message_lower: 用户消息小写
        scenario: 对话场景
        level: 用户语言水平
        conversation_context: 对话上下文
        custom_scenario_name: 自定义场景名称
        custom_scenario_description: 自定义场景描述
    
    Returns:
        自然的英文回复
    """
    
    # 处理自定义场景
    if scenario and scenario.startswith('custom_') and custom_scenario_name:
        return generate_custom_scenario_response_english(message, message_lower, custom_scenario_name, custom_scenario_description, level)
    
    # 根据场景生成回复
    if scenario == "restaurant":
        return generate_restaurant_response_english(message, message_lower, conversation_context, level)
    elif scenario == "shopping":
        return generate_shopping_response_english(message, message_lower, conversation_context, level)
    elif scenario == "direction":
        return generate_direction_response_english(message, message_lower, conversation_context, level)
    elif scenario == "introduction":
        return generate_introduction_response_english(message, message_lower, conversation_context, level)
    else:
        return generate_general_response_english(message, message_lower, conversation_context, level)

def generate_enhanced_chinese_response(message: str, message_lower: str, scenario: str, level: str, conversation_context: dict, custom_scenario_name: str = None, custom_scenario_description: str = None) -> str:
    """
    生成增强的中文回复 - 更加自然、人性化，有情感表达
    
    Args:
        message: 用户消息
        message_lower: 用户消息小写
        scenario: 对话场景
        level: 用户语言水平
        conversation_context: 对话上下文
        custom_scenario_name: 自定义场景名称
        custom_scenario_description: 自定义场景描述
    
    Returns:
        自然的中文回复
    """
    
    # 处理自定义场景
    if scenario and scenario.startswith('custom_') and custom_scenario_name:
        return generate_custom_scenario_response_chinese(message, message_lower, custom_scenario_name, custom_scenario_description, level)
    
    # 根据场景生成回复
    if scenario == "restaurant":
        return generate_restaurant_response_chinese(message, message_lower, conversation_context, level)
    elif scenario == "shopping":
        return generate_shopping_response_chinese(message, message_lower, conversation_context, level)
    elif scenario == "direction":
        return generate_direction_response_chinese(message, message_lower, conversation_context, level)
    elif scenario == "introduction":
        return generate_introduction_response_chinese(message, message_lower, conversation_context, level)
    else:
        return generate_general_response_chinese(message, message_lower, conversation_context, level)

def generate_restaurant_response_english(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成餐厅场景的英文回复"""
    
    # 检测用户明确提到的食物或需求
    food_items = {
        "pizza": "pizza",
        "burger": "burger", 
        "pasta": "pasta",
        "salad": "salad",
        "steak": "steak",
        "chicken": "chicken",
        "fish": "fish",
        "salmon": "salmon",
        "soup": "soup",
        "sandwich": "sandwich",
        "dessert": "dessert",
        "coffee": "coffee",
        "tea": "tea",
        "water": "water",
        "wine": "wine",
        "beer": "beer",
        "pasta": "pasta",
        "curry": "curry"
    }
    
    # 检查用户是否提到了具体食物
    mentioned_food = None
    for food_key, food_name in food_items.items():
        if food_key in message_lower:
            mentioned_food = food_name
            break
    
    # 如果用户明确提到了食物，直接提供相关信息
    if mentioned_food:
        if "want" in message_lower or "like" in message_lower or "order" in message_lower:
            responses = [
                f"Excellent choice! Our {mentioned_food} is really popular here. Would you like to hear about our special preparation?",
                f"Great selection! The {mentioned_food} is one of our best dishes. How would you like it prepared?",
                f"Perfect! I can definitely help you with the {mentioned_food}. Any specific preferences for preparation or sides?"
            ]
        elif "price" in message_lower or "cost" in message_lower or "how much" in message_lower:
            responses = [
                f"Our {mentioned_food} is $12.99. Would you like to add any sides or drinks to that?",
                f"The {mentioned_food} costs $12.99. It comes with your choice of sides. Sound good?",
                f"Great choice! The {mentioned_food} is $12.99. Would you like to see what sides are available?"
            ]
        else:
            responses = [
                f"I'd be happy to tell you about our {mentioned_food}! It's one of our signature dishes.",
                f"Excellent choice! Our {mentioned_food} is fantastic. Would you like to know more about it?",
                f"Perfect! The {mentioned_food} is very popular here. Any questions about it?"
            ]
        return random.choice(responses)
    
    # 原有的逻辑处理其他情况
    mood = context.get("mood", "neutral")
    
    if "menu" in message_lower or "food" in message_lower:
        responses = [
            "Great! Our menu features fresh local ingredients. What type of cuisine are you in the mood for today?",
            "I'd be happy to tell you about our specialties! Do you prefer something light or hearty?",
            "Our chef's special today is amazing! Are you interested in seafood, meat, or vegetarian options?"
        ]
    elif "recommend" in message_lower or "suggest" in message_lower:
        responses = [
            "I'd recommend our signature pasta - it's absolutely delicious! Would you like to try it?",
            "Our grilled salmon is very popular today. How does that sound to you?",
            "If you like spicy food, our curry is fantastic! What's your spice tolerance?"
        ]
    elif "price" in message_lower or "cost" in message_lower:
        responses = [
            "Our prices are very reasonable! Most entrees range from $15-25. Would you like to see the menu?",
            "We have great value meals! Our lunch specials are particularly good deals. Interested?",
            "I can show you our budget-friendly options too. What's your price range?"
        ]
    elif mood == "positive":
        responses = [
            "I'm so glad you're enjoying it! Is there anything else I can get for you?",
            "Wonderful! I love seeing happy customers. Would you like to try our dessert menu?",
            "Fantastic! You made a great choice. How's everything tasting?"
        ]
    else:
        responses = [
            "Welcome to our restaurant! How can I help you today?",
            "Good to see you! Are you ready to order, or would you like a few more minutes?",
            "Hello! I'm here to help with anything you need. What brings you in today?"
        ]
    
    return random.choice(responses)

def generate_shopping_response_english(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成购物场景的英文回复"""
    
    # 检测用户明确提到的商品或需求
    products = {
        "shirt": "shirt",
        "pants": "pants",
        "dress": "dress",
        "shoes": "shoes",
        "jacket": "jacket",
        "hat": "hat",
        "bag": "bag",
        "watch": "watch",
        "phone": "phone",
        "laptop": "laptop",
        "book": "book",
        "gift": "gift",
        "toy": "toy",
        "perfume": "perfume",
        "jewelry": "jewelry",
        "sunglasses": "sunglasses"
    }
    
    # 检查用户是否提到了具体商品
    mentioned_product = None
    for product_key, product_name in products.items():
        if product_key in message_lower:
            mentioned_product = product_name
            break
    
    # 如果用户明确提到了商品，直接提供相关信息
    if mentioned_product:
        if "looking for" in message_lower or "need" in message_lower or "want" in message_lower:
            responses = [
                f"Perfect! We have some great {mentioned_product}s in stock right now. What size are you looking for?",
                f"Excellent choice! I can help you find the perfect {mentioned_product}. Do you have a color preference?",
                f"Great! We have several {mentioned_product}s available. What's your budget range?"
            ]
        elif "price" in message_lower or "cost" in message_lower or "how much" in message_lower:
            responses = [
                f"Our {mentioned_product}s start at $29.99. We have different styles and price ranges. Would you like to see them?",
                f"The {mentioned_product} is currently $39.99, and it's on sale! Would you like to try it on?",
                f"Great choice! The {mentioned_product} is $49.99. We also have similar items at different price points."
            ]
        elif "size" in message_lower:
            responses = [
                f"We have the {mentioned_product} in sizes S, M, L, and XL. What's your usual size?",
                f"Perfect! For the {mentioned_product}, we carry sizes 6-16. Would you like to try one on?",
                f"Great! The {mentioned_product} comes in multiple sizes. Let me help you find the right fit."
            ]
        else:
            responses = [
                f"I'd be happy to show you our {mentioned_product} collection! We have some really nice options.",
                f"Excellent choice! Our {mentioned_product}s are very popular. Would you like to see what we have?",
                f"Perfect! I can help you with the {mentioned_product}. Any specific style or color in mind?"
            ]
        return random.choice(responses)
    
    # 原有的逻辑处理其他情况
    if "size" in message_lower:
        responses = [
            "Let me help you find the right size! What size are you looking for?",
            "I can check our inventory for different sizes. What's your usual size?",
            "We have a great range of sizes available. Would you like to try something on?"
        ]
    elif "price" in message_lower or "cost" in message_lower:
        responses = [
            "Great question! This item is on sale right now. Would you like to know the details?",
            "I can show you our current promotions! Are you interested in any specific items?",
            "We have some amazing deals today! What's your budget range?"
        ]
    elif "color" in message_lower:
        responses = [
            "We have this in several colors! What's your favorite?",
            "I love the blue one! Which color catches your eye?",
            "Great choice! We have it in black, navy, and gray. What do you think?"
        ]
    else:
        responses = [
            "Hi there! How can I help you find what you're looking for today?",
            "Welcome! Is there something specific you're shopping for?",
            "Hello! I'm here to help. What brings you in today?"
        ]
    
    return random.choice(responses)

def generate_direction_response_english(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成问路场景的英文回复"""
    
    # 检测用户明确提到的目的地
    destinations = {
        "hospital": "the hospital",
        "school": "the school", 
        "bank": "the bank",
        "store": "the store",
        "restaurant": "the restaurant",
        "hotel": "the hotel",
        "airport": "the airport",
        "station": "the train station",
        "park": "the park",
        "library": "the library",
        "museum": "the museum",
        "mall": "the mall",
        "pharmacy": "the pharmacy",
        "post office": "the post office"
    }
    
    # 检查用户是否提到了具体目的地
    mentioned_destination = None
    for dest_key, dest_name in destinations.items():
        if dest_key in message_lower:
            mentioned_destination = dest_name
            break
    
    # 如果用户明确提到了目的地，直接提供指引
    if mentioned_destination:
        if "going" in message_lower or "need to go" in message_lower or "want to go" in message_lower:
            responses = [
                f"Great! I can help you get to {mentioned_destination}. It's about a 10-minute walk from here. Go straight down this street for two blocks, then turn left.",
                f"Sure! {mentioned_destination.title()} is not far from here. You can walk there in about 8 minutes. Head north on Main Street, then turn right at the second intersection.",
                f"Perfect! I know exactly where {mentioned_destination} is. It's a 12-minute walk. Go down this road, take the first left, and you'll see it on your right."
            ]
        else:
            responses = [
                f"Of course! {mentioned_destination.title()} is about 10 minutes away. Would you like walking directions or driving directions?",
                f"Absolutely! I can give you directions to {mentioned_destination}. It's pretty close - maybe 8 minutes on foot.",
                f"Sure thing! {mentioned_destination.title()} is just down the street. Are you walking or driving there?"
            ]
        return random.choice(responses)
    
    # 原有的逻辑处理其他情况
    if "how" in message_lower and ("get" in message_lower or "find" in message_lower):
        responses = [
            "I'd be happy to help you get there! Are you walking or driving?",
            "Sure thing! It's actually not too far from here. Do you have a map app?",
            "No problem! I know that area well. Which direction are you coming from?"
        ]
    elif "far" in message_lower or "distance" in message_lower:
        responses = [
            "It's about a 10-minute walk from here! Very doable.",
            "Not far at all! Maybe 5 minutes by car, 15 minutes walking.",
            "Pretty close! You could walk there in about 12 minutes."
        ]
    elif "bus" in message_lower or "train" in message_lower:
        responses = [
            "Yes! You can take the bus from here. The stop is just around the corner.",
            "Absolutely! The subway is actually closer. Would you like directions to the station?",
            "Great option! Public transport is very convenient here. Which line do you prefer?"
        ]
    else:
        responses = [
            "I'd be happy to help you find your way! Where are you trying to go?",
            "No worries! I know this area pretty well. What's your destination?",
            "Sure! I can give you directions. Where do you need to get to?"
        ]
    
    return random.choice(responses)

def generate_introduction_response_english(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成自我介绍场景的英文回复"""
    
    # 检测用户明确提到的个人信息或话题
    personal_topics = {
        "name": "name",
        "age": "age",
        "work": "work",
        "job": "job",
        "hobby": "hobby",
        "hobbies": "hobbies",
        "interest": "interest",
        "interests": "interests",
        "family": "family",
        "home": "home",
        "country": "country",
        "city": "city",
        "school": "school",
        "study": "study",
        "travel": "travel",
        "sport": "sport",
        "music": "music",
        "movie": "movie",
        "book": "book"
    }
    
    # 检查用户是否提到了具体话题
    mentioned_topic = None
    for topic_key, topic_name in personal_topics.items():
        if topic_key in message_lower:
            mentioned_topic = topic_name
            break
    
    # 如果用户明确提到了话题，直接回应并询问相关信息
    if mentioned_topic:
        if mentioned_topic == "name":
            responses = [
                "Nice to meet you! I'm Alex. What a great name! Where are you from?",
                "Pleasure to meet you! I'm Sarah. That's a beautiful name. How long have you been here?",
                "Hello! I'm Michael. Great to meet someone with that name! What brings you here today?"
            ]
        elif mentioned_topic in ["work", "job"]:
            responses = [
                "That sounds really interesting! I work in marketing myself. How long have you been in that field?",
                "Wow, that must be exciting! I'm a teacher. Do you enjoy what you do?",
                "That's cool! I'm actually between jobs right now. How did you get into that line of work?"
            ]
        elif mentioned_topic in ["hobby", "hobbies", "interest", "interests"]:
            responses = [
                "I love hiking and reading too! What specific activities do you enjoy most?",
                "That's awesome! I'm really into photography. Do you have a favorite hobby?",
                "Great! I enjoy cooking and trying new recipes. What kind of interests do you have?"
            ]
        elif mentioned_topic == "family":
            responses = [
                "Family is so important! I have two siblings myself. Tell me about yours.",
                "That's wonderful! I'm close with my family too. How many people are in your family?",
                "Family time is the best! I love spending time with mine. What's your family like?"
            ]
        elif mentioned_topic in ["travel", "country", "city"]:
            responses = [
                "Traveling is amazing! I love exploring new places. Where have you been recently?",
                "That sounds fantastic! I'm planning a trip myself. What's your favorite place you've visited?",
                "I'm so jealous! Traveling is one of my passions. Where would you like to go next?"
            ]
        else:
            responses = [
                f"That's really interesting! I'd love to hear more about your {mentioned_topic}.",
                f"Tell me more about your {mentioned_topic}! That sounds fascinating.",
                f"I'm curious about your {mentioned_topic}. How did you get interested in that?"
            ]
        return random.choice(responses)
    
    # 原有的逻辑处理其他情况
    if "name" in message_lower:
        responses = [
            "Nice to meet you! I'm Alex. What brings you here today?",
            "Pleasure to meet you! I'm Sarah. How's your day going so far?",
            "Hello! I'm Michael. It's great to meet new people here!"
        ]
    elif "work" in message_lower or "job" in message_lower:
        responses = [
            "That sounds interesting! I work in marketing. How long have you been in your field?",
            "Wow, that must be exciting! I'm a teacher myself. Do you enjoy what you do?",
            "That's cool! I'm actually between jobs right now. How did you get into that line of work?"
        ]
    elif "hobby" in message_lower or "interest" in message_lower:
        responses = [
            "I love hiking and reading! What about you? Any hobbies you're passionate about?",
            "That's awesome! I'm really into photography. Do you have a favorite spot to take pictures?",
            "Great! I enjoy cooking and trying new recipes. What kind of music do you like?"
        ]
    else:
        responses = [
            "Hi there! I don't think we've met before. I'm new here too!",
            "Hello! It's nice to meet you. Are you from around here?",
            "Hey! I'm glad we ran into each other. How's everything going?"
        ]
    
    return random.choice(responses)

def generate_general_response_english(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成通用场景的英文回复"""
    
    # 检测用户明确提到的具体话题或需求
    general_topics = {
        "help": "help",
        "problem": "problem",
        "question": "question",
        "weather": "weather",
        "news": "news",
        "today": "today",
        "tomorrow": "tomorrow",
        "weekend": "weekend",
        "vacation": "vacation",
        "holiday": "holiday",
        "birthday": "birthday",
        "party": "party",
        "meeting": "meeting",
        "appointment": "appointment",
        "plan": "plan",
        "idea": "idea",
        "suggestion": "suggestion",
        "advice": "advice",
        "opinion": "opinion",
        "thought": "thought"
    }
    
    # 检查用户是否提到了具体话题
    mentioned_topic = None
    for topic_key, topic_name in general_topics.items():
        if topic_key in message_lower:
            mentioned_topic = topic_name
            break
    
    # 如果用户明确提到了话题，直接回应并询问相关信息
    if mentioned_topic:
        if mentioned_topic == "help":
            responses = [
                "I'd be happy to help! What specifically do you need assistance with?",
                "Of course! I'm here to help. What can I do for you?",
                "Absolutely! Tell me what you need help with and I'll do my best to assist."
            ]
        elif mentioned_topic == "problem":
            responses = [
                "I'm sorry you're having a problem. Can you tell me more about what's going on?",
                "That sounds challenging. What kind of problem are you dealing with?",
                "I understand problems can be frustrating. What happened? Maybe I can help."
            ]
        elif mentioned_topic == "question":
            responses = [
                "I'm here to answer questions! What would you like to know?",
                "Great! I love answering questions. What's on your mind?",
                "Ask away! I'm happy to help with any questions you have."
            ]
        elif mentioned_topic == "weather":
            responses = [
                "The weather has been interesting lately! Do you prefer sunny or rainy days?",
                "I know, right? The weather can be so unpredictable. Are you planning anything outdoor?",
                "Weather talk! Are you from a place with different weather than here?"
            ]
        elif mentioned_topic in ["today", "tomorrow", "weekend"]:
            responses = [
                f"How is your {mentioned_topic} going so far? Any exciting plans?",
                f"I hope your {mentioned_topic} is going well! What are you up to?",
                f"Tell me about your {mentioned_topic}! Anything special happening?"
            ]
        elif mentioned_topic in ["vacation", "holiday"]:
            responses = [
                "Vacations are the best! Where are you planning to go?",
                "I love hearing about travel plans! What's your dream destination?",
                "That sounds exciting! Are you planning something special for your vacation?"
            ]
        else:
            responses = [
                f"That's really interesting! Tell me more about your {mentioned_topic}.",
                f"I'd love to hear more about that {mentioned_topic}. What's on your mind?",
                f"Tell me about your {mentioned_topic}! That sounds like it could be quite interesting."
            ]
        return random.choice(responses)
    
    # 原有的逻辑处理其他情况
    mood = context.get("mood", "neutral")
    topic = context.get("topic", "general")
    
    if mood == "positive":
        responses = [
            "That's wonderful! I'm so happy for you. Tell me more about it!",
            "Fantastic! You sound really excited. What happened?",
            "That's great news! I love hearing positive stories. How did it go?"
        ]
    elif mood == "negative":
        responses = [
            "I'm sorry to hear that. Is there anything I can do to help?",
            "That sounds tough. Do you want to talk about it?",
            "I understand how you feel. Sometimes things can be challenging. How are you doing?"
        ]
    elif topic == "weather":
        responses = [
            "The weather has been interesting lately! Do you prefer sunny or rainy days?",
            "I know, right? The weather can be so unpredictable. Are you planning anything outdoor?",
            "Weather talk! Are you from a place with different weather than here?"
        ]
    else:
        responses = [
            "That's interesting! Tell me more about that.",
            "I see what you mean. How do you feel about that?",
            "That sounds like quite a situation. What do you think about it?"
        ]
    
    return random.choice(responses)

# 中文回复生成函数（类似结构，但使用中文内容）
def generate_restaurant_response_chinese(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成餐厅场景的中文回复"""
    mood = context.get("mood", "neutral")
    
    if "菜单" in message_lower or "食物" in message_lower:
        responses = [
            "太好了！我们的菜单特色是新鲜的本地食材。您今天想吃什么类型的菜呢？",
            "我很乐意为您介绍我们的特色菜！您喜欢清淡的还是丰盛的？",
            "我们主厨今天的特色菜很棒！您对海鲜、肉类还是素食感兴趣？"
        ]
    elif "推荐" in message_lower or "建议" in message_lower:
        responses = [
            "我推荐我们的招牌意面，绝对美味！您想试试吗？",
            "我们的烤三文鱼今天很受欢迎。您觉得怎么样？",
            "如果您喜欢辣食，我们的咖喱很棒！您能接受什么辣度？"
        ]
    elif "价格" in message_lower or "费用" in message_lower:
        responses = [
            "我们的价格很合理！大多数主菜在15-25美元之间。您想看看菜单吗？",
            "我们有很棒的套餐！午餐特价特别划算。感兴趣吗？",
            "我也可以为您介绍经济实惠的选择。您的预算范围是多少？"
        ]
    elif mood == "positive":
        responses = [
            "很高兴您喜欢！还有什么我能为您做的吗？",
            "太棒了！我喜欢看到开心的顾客。您想看看我们的甜品菜单吗？",
            "太好了！您做了很棒的选择。味道怎么样？"
        ]
    else:
        responses = [
            "欢迎来到我们餐厅！今天我能为您做什么？",
            "很高兴见到您！您准备点餐了吗，还是需要再考虑一会儿？",
            "您好！我在这里为您提供帮助。今天是什么风把您吹来了？"
        ]
    
    return random.choice(responses)

def generate_shopping_response_chinese(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成购物场景的中文回复"""
    if "尺寸" in message_lower or "大小" in message_lower:
        responses = [
            "让我帮您找到合适的尺寸！您在找什么尺码？",
            "我可以查看我们的库存，看看有哪些尺寸。您平时穿什么尺码？",
            "我们有很棒的尺码范围。您想试穿一下吗？"
        ]
    elif "价格" in message_lower or "费用" in message_lower:
        responses = [
            "好问题！这个商品现在正在打折。您想了解详情吗？",
            "我可以给您看看我们当前的促销活动！您对什么商品感兴趣？",
            "我们今天有一些很棒的特价！您的预算范围是多少？"
        ]
    elif "颜色" in message_lower:
        responses = [
            "这个我们有几种颜色！您最喜欢哪种？",
            "我很喜欢蓝色的！哪种颜色吸引了您的注意？",
            "很棒的选择！我们有黑色、海军蓝和灰色。您觉得怎么样？"
        ]
    else:
        responses = [
            "您好！今天我能帮您找到什么？",
            "欢迎！您在找什么特定的东西吗？",
            "您好！我在这里为您提供帮助。今天是什么把您带来了？"
        ]
    
    return random.choice(responses)

def generate_direction_response_chinese(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成问路场景的中文回复"""
    
    # 检测用户明确提到的目的地
    destinations = {
        "医院": "医院",
        "学校": "学校",
        "银行": "银行",
        "商店": "商店",
        "餐厅": "餐厅",
        "酒店": "酒店",
        "机场": "机场",
        "车站": "车站",
        "公园": "公园",
        "图书馆": "图书馆",
        "博物馆": "博物馆",
        "商场": "商场",
        "药店": "药店",
        "邮局": "邮局",
        "超市": "超市",
        "加油站": "加油站"
    }
    
    # 检查用户是否提到了具体目的地
    mentioned_destination = None
    for dest_key, dest_name in destinations.items():
        if dest_key in message_lower:
            mentioned_destination = dest_name
            break
    
    # 如果用户明确提到了目的地，直接提供指引
    if mentioned_destination:
        if "去" in message_lower or "到" in message_lower or "要去" in message_lower:
            responses = [
                f"好的！我可以帮您找到{mentioned_destination}。从这里步行大约10分钟。沿着这条街直走两个街区，然后左转。",
                f"当然可以！{mentioned_destination}离这里不远。您步行大约8分钟就能到。沿着主街向北走，在第二个路口右转。",
                f"没问题！我知道{mentioned_destination}在哪里。步行大约12分钟。沿着这条路走，第一个路口左转，您就能在右边看到它。"
            ]
        else:
            responses = [
                f"当然！{mentioned_destination}大约10分钟路程。您想要步行路线还是开车路线？",
                f"绝对可以！我可以为您指路到{mentioned_destination}。很近，步行大概8分钟。",
                f"没问题！{mentioned_destination}就在这条街上。您是要步行去还是开车去？"
            ]
        return random.choice(responses)
    
    # 原有的逻辑处理其他情况
    if "怎么" in message_lower and ("去" in message_lower or "到" in message_lower):
        responses = [
            "我很乐意帮您找到那里！您是步行还是开车？",
            "当然可以！其实离这里不远。您有地图应用吗？",
            "没问题！我对那个地区很熟悉。您是从哪个方向来的？"
        ]
    elif "远" in message_lower or "距离" in message_lower:
        responses = [
            "从这里步行大约10分钟！完全可以走得到。",
            "一点也不远！开车大概5分钟，步行15分钟。",
            "很近！您步行大约12分钟就能到。"
        ]
    elif "公交" in message_lower or "地铁" in message_lower:
        responses = [
            "是的！您可以坐公交车。站点就在拐角处。",
            "当然可以！地铁其实更近。您想了解去地铁站的方向吗？",
            "很好的选择！这里的公共交通很方便。您更喜欢哪条线路？"
        ]
    else:
        responses = [
            "我很乐意帮您找到路！您想去哪里？",
            "没问题！我对这个地区很熟悉。您的目的地是哪里？",
            "当然！我可以为您指路。您需要去哪里？"
        ]
    
    return random.choice(responses)

def generate_introduction_response_chinese(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成自我介绍场景的中文回复"""
    if "名字" in message_lower or "姓名" in message_lower:
        responses = [
            "很高兴认识您！我叫小明。今天是什么把您带到这里的？",
            "很高兴见到您！我是小红。您今天过得怎么样？",
            "您好！我是小李。在这里认识新朋友真棒！"
        ]
    elif "工作" in message_lower or "职业" in message_lower:
        responses = [
            "听起来很有趣！我在市场营销工作。您在这个领域工作多久了？",
            "哇，那一定很刺激！我自己是老师。您喜欢自己的工作吗？",
            "很酷！我现在实际上在找工作。您是怎么进入那个行业的？"
        ]
    elif "爱好" in message_lower or "兴趣" in message_lower:
        responses = [
            "我喜欢徒步和阅读！您呢？有什么您热衷的爱好吗？",
            "太棒了！我真的很喜欢摄影。您有最喜欢的拍照地点吗？",
            "很好！我喜欢烹饪和尝试新食谱。您喜欢什么类型的音乐？"
        ]
    else:
        responses = [
            "您好！我想我们之前没有见过面。我也是新来的！",
            "您好！很高兴认识您。您是本地人吗？",
            "嘿！很高兴我们遇到了。一切都还好吗？"
        ]
    
    return random.choice(responses)

def generate_general_response_chinese(message: str, message_lower: str, context: dict, level: str) -> str:
    """生成通用场景的中文回复"""
    mood = context.get("mood", "neutral")
    topic = context.get("topic", "general")
    
    if mood == "positive":
        responses = [
            "太棒了！我为您感到高兴。告诉我更多吧！",
            "太棒了！您听起来真的很兴奋。发生了什么？",
            "好消息！我喜欢听积极的故事。进展如何？"
        ]
    elif mood == "negative":
        responses = [
            "很抱歉听到这个消息。有什么我能帮助的吗？",
            "听起来很困难。您想谈谈吗？",
            "我理解您的感受。有时候事情确实很具挑战性。您还好吗？"
        ]
    elif topic == "weather":
        responses = [
            "最近的天气确实很有趣！您更喜欢晴天还是雨天？",
            "我知道，对吧？天气总是这么不可预测。您有什么户外计划吗？",
            "天气话题！您是来自和这里天气不同的地方吗？"
        ]
    else:
        responses = [
            "很有趣！告诉我更多关于这个的信息。",
            "我明白您的意思。您对此有什么感受？",
            "听起来情况很复杂。您对此有什么想法？"
        ]
    
    return random.choice(responses)

def build_conversation_context(history: List[dict], current_message: str) -> str:
    """构建对话上下文"""
    context_parts = []
    
    for item in history:
        if item.get("user_message"):
            context_parts.append(f"User: {item['user_message']}")
        if item.get("ai_response"):
            context_parts.append(f"AI: {item['ai_response']}")
    
    context_parts.append(f"User: {current_message}")
    
    return "\n".join(context_parts)

def generate_english_natural_response(message: str, message_lower: str, scenario: str, level: str, conversation_context: str, custom_scenario_name: str = None, custom_scenario_description: str = None) -> str:
    """生成自然的英文回复"""
    
    # 处理自定义场景
    if scenario and scenario.startswith('custom_') and custom_scenario_name:
        return generate_custom_scenario_response_english(message, message_lower, custom_scenario_name, custom_scenario_description, level)
    
    # 根据场景和对话历史生成回复
    if scenario == "restaurant":
        return generate_restaurant_response_english(message, message_lower, conversation_context)
    elif scenario == "shopping":
        return generate_shopping_response_english(message, message_lower, conversation_context)
    elif scenario == "direction":
        return generate_direction_response_english(message, message_lower, conversation_context)
    elif scenario == "introduction":
        return generate_introduction_response_english(message, message_lower, conversation_context)
    else:
        return generate_general_response_english(message, message_lower, conversation_context)

def generate_chinese_natural_response(message: str, message_lower: str, scenario: str, level: str, conversation_context: str, custom_scenario_name: str = None, custom_scenario_description: str = None) -> str:
    """生成自然的中文回复"""
    
    # 处理自定义场景
    if scenario and scenario.startswith('custom_') and custom_scenario_name:
        return generate_custom_scenario_response_chinese(message, message_lower, custom_scenario_name, custom_scenario_description, level)
    
    # 根据场景和对话历史生成回复
    if scenario == "restaurant":
        return generate_restaurant_response_chinese(message, message_lower, conversation_context)
    elif scenario == "shopping":
        return generate_shopping_response_chinese(message, message_lower, conversation_context)
    elif scenario == "direction":
        return generate_direction_response_chinese(message, message_lower, conversation_context)
    elif scenario == "introduction":
        return generate_introduction_response_chinese(message, message_lower, conversation_context)
    else:
        return generate_general_response_chinese(message, message_lower, conversation_context)

# 自定义场景回复函数
def generate_custom_scenario_response_english(message: str, message_lower: str, scenario_name: str, scenario_description: str, level: str) -> str:
    """生成自定义场景的英文回复"""
    
    # 根据学习等级调整回复复杂度
    if level == "beginner":
        responses = [
            f"Hi there! Welcome to our {scenario_name.lower()} practice session. How can I help you today?",
            f"Hello! I'm here to help you with {scenario_name.lower()}. What would you like to know?",
            f"Great to meet you! Let's practice {scenario_name.lower()} together. What brings you here?",
            f"Welcome! I'm excited to help you with {scenario_name.lower()}. What can I do for you?",
            f"Hello! Ready to practice {scenario_name.lower()}? What would you like to work on?"
        ]
    elif level == "advanced":
        responses = [
            f"Good day! I'm delighted to assist you with this {scenario_name.lower()} scenario. How may I facilitate your learning experience today?",
            f"Welcome! I'm here to guide you through this sophisticated {scenario_name.lower()} practice session. What specific aspect would you like to explore?",
            f"Excellent! I'm prepared to engage with you in this comprehensive {scenario_name.lower()} exercise. What challenges are you hoping to address?",
            f"Greetings! I'm enthusiastic about supporting your {scenario_name.lower()} development. What particular skills would you like to enhance?",
            f"Hello! I'm ready to collaborate with you on this advanced {scenario_name.lower()} scenario. What objectives are you pursuing?"
        ]
    else:  # intermediate
        responses = [
            f"Hello! Welcome to our {scenario_name.lower()} practice session. I'm here to help you improve your skills. What would you like to focus on?",
            f"Hi there! I'm excited to work with you on {scenario_name.lower()}. What specific area would you like to practice?",
            f"Welcome! Let's make the most of this {scenario_name.lower()} learning opportunity. What questions do you have?",
            f"Great to see you! I'm ready to help you with {scenario_name.lower()}. What would you like to discuss?",
            f"Hello! I'm here to support your {scenario_name.lower()} practice. What aspects would you like to explore?"
        ]
    
    # 根据用户输入选择更具体的回复
    if any(word in message_lower for word in ["hello", "hi", "good morning", "good afternoon", "good evening"]):
        return random.choice(responses)
    elif any(word in message_lower for word in ["help", "assist", "support"]):
        return f"I'm here to help you with {scenario_name.lower()}! Based on your description: '{scenario_description}'. What specific aspect would you like to practice?"
    elif any(word in message_lower for word in ["question", "ask", "wonder"]):
        return f"That's a great question about {scenario_name.lower()}! I'd be happy to help you work through it. Can you tell me more details?"
    elif any(word in message_lower for word in ["practice", "learn", "improve"]):
        return f"Excellent! Let's practice {scenario_name.lower()} together. What specific skills or situations would you like to focus on?"
    else:
        return f"Interesting! I'm here to help you with {scenario_name.lower()}. Let's explore this topic together. What would you like to know more about?"

def generate_custom_scenario_response_chinese(message: str, message_lower: str, scenario_name: str, scenario_description: str, level: str) -> str:
    """生成自定义场景的中文回复"""
    
    # 根据学习等级调整回复复杂度
    if level == "beginner":
        responses = [
            f"您好！欢迎来到{scenario_name}练习。今天我可以怎么帮助您？",
            f"您好！我来帮助您练习{scenario_name}。您想了解什么？",
            f"很高兴见到您！让我们一起来练习{scenario_name}。您来这里想做什么？",
            f"欢迎！我很兴奋能帮助您练习{scenario_name}。我可以为您做什么？",
            f"您好！准备好练习{scenario_name}了吗？您想练习什么？"
        ]
    elif level == "advanced":
        responses = [
            f"您好！我很高兴能协助您进行这个{scenario_name}场景练习。今天我如何能促进您的学习体验？",
            f"欢迎！我将指导您完成这个复杂的{scenario_name}练习。您希望探索哪个特定方面？",
            f"太好了！我准备与您一起参与这个全面的{scenario_name}练习。您希望解决什么挑战？",
            f"问候！我对支持您的{scenario_name}发展充满热情。您希望提升哪些特定技能？",
            f"您好！我准备好与您在这个高级{scenario_name}场景中合作。您追求什么目标？"
        ]
    else:  # intermediate
        responses = [
            f"您好！欢迎来到我们的{scenario_name}练习。我来帮助您提高技能。您想专注于什么？",
            f"您好！我很兴奋能与您一起练习{scenario_name}。您想练习哪个特定领域？",
            f"欢迎！让我们充分利用这个{scenario_name}学习机会。您有什么问题？",
            f"很高兴见到您！我准备好帮助您练习{scenario_name}。您想讨论什么？",
            f"您好！我来支持您的{scenario_name}练习。您想探索哪些方面？"
        ]
    
    # 根据用户输入选择更具体的回复
    if any(word in message_lower for word in ["你好", "您好", "早上好", "下午好", "晚上好"]):
        return random.choice(responses)
    elif any(word in message_lower for word in ["帮助", "协助", "支持"]):
        return f"我来帮助您练习{scenario_name}！根据您的描述：'{scenario_description}'。您想练习哪个特定方面？"
    elif any(word in message_lower for word in ["问题", "问", "想知道"]):
        return f"关于{scenario_name}这是个很好的问题！我很乐意帮助您解决。您能告诉我更多细节吗？"
    elif any(word in message_lower for word in ["练习", "学习", "提高"]):
        return f"太好了！让我们一起练习{scenario_name}。您想专注于哪些特定技能或情况？"
    else:
        return f"有趣！我来帮助您练习{scenario_name}。让我们一起探索这个话题。您还想了解什么？"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
