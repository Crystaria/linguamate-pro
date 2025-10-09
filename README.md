# LinguaMate AI - Multimodal Language Learning Companion

## Project Overview

LinguaMate AI is a multimodal language learning companion that leverages artificial intelligence to help learners master languages in authentic contexts. It combines linguistic theories (morphology, syntax, semantics, pragmatics, second language acquisition) to generate personalized, comprehensible learning materials.

## Core Features

- **Multimodal Input**: Upload text/images, AI automatically parses vocabulary, syntactic structures, and cultural contexts
- **Linguistics-Driven Analysis**: Provides root/affix breakdown, grammatical structure visualization, contextualized examples
- **Personalized Learning Path**: AI generates summaries and exercises (multiple choice, sentence building, dialogue completion) based on learner level
- **Real-time Interaction**: Users can chat with AI and practice language in simulated scenarios

## Technology Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI
- **AI Capabilities**: LLM (parsing/generation), OCR (image-to-text)
- **Database**: Supabase (learning record storage)

## Project Structure

```
eduhacks-ai-fest-2025/
├── frontend/          # React frontend application
├── backend/           # FastAPI backend service
├── database/          # Database schema and setup
├── deployment/        # Deployment configuration
├── demo/             # Demo scripts and materials
├── LinguaMate AI PRD.txt  # Product requirements document
├── requirements.txt   # Competition requirements
└── README.md         # Project documentation
```

## Quick Start

### Environment Setup

1. **Install Dependencies**
   - Python 3.9+
   - Node.js 16+
   - Tesseract OCR

2. **Configure Environment Variables**
   ```bash
   # Copy environment variable template
   cp backend/env_example.txt backend/.env
   
   # Edit .env file with the following information:
   OPENAI_API_KEY=your_openai_api_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_ANON_KEY=your_supabase_anon_key_here
   ```

3. **Setup Database**
   - Create Supabase project
   - Run `database/schema.sql` to create table structure
   - Refer to `database/README.md` for detailed configuration

### Local Development

#### Backend Startup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend Startup
```bash
cd frontend
npm install
npm start
```

### Docker Deployment

```bash
cd deployment
docker-compose up -d
```

## Demo Scenarios

1. **Text Analysis**: Input English text → AI linguistic analysis → Generate personalized exercises
2. **Image Analysis**: Upload textbook screenshots → OCR text recognition → Linguistic parsing → Generate exercises
3. **Conversation Practice**: Choose scenario (restaurant ordering) → Real-time dialogue with AI → Practice language usage

## Feature Highlights

### Linguistics-Driven AI Analysis
- Based on morphology, syntax, semantics, pragmatics theories
- Provides root, affix, grammatical structure analysis
- Combines second language acquisition theory for personalized recommendations

### Multimodal Learning Experience
- Supports both text and image input methods
- OCR technology recognizes text content in images
- Language learning in authentic contexts

### Personalized Learning Path
- Adjusts content based on learner level (beginner/intermediate/advanced)
- Dynamically generates appropriate exercises
- Tracks learning progress and records

### Immersive Conversation Practice
- Simulates real-world scenario dialogue practice
- AI as conversation partner for interaction
- Provides immediate feedback and correction

## API Endpoints

### Text Analysis
```
POST /upload/text
{
  "text": "Learning text content",
  "level": "beginner|intermediate|advanced"
}
```

### Image Analysis
```
POST /upload/image
FormData: file + level
```

### Exercise Generation
```
POST /generate-exercises
{
  "record_id": "Learning record ID",
  "level": "Learning level"
}
```

### AI Chat
```
POST /chat
{
  "message": "User message",
  "context": "Conversation context",
  "level": "Learning level"
}
```

## Team Members

- **廖悠澜** - Full-stack Development / Product Design / Linguistics Research

## Competition Information

- **Competition**: EduHacks AI Fest 2025
- **Date**: September 27 - October 11, 2025
- **Theme**: Personalized Learning
- **Track**: AI-driven Personalized Learning Systems

## Technical Highlights

### AI Technology Applications
- **Large Language Models**: For linguistic analysis and content generation
- **OCR Technology**: Image text recognition and extraction
- **Natural Language Processing**: Dialogue generation and language understanding

### User Experience Design
- **Responsive Interface**: Adapts to various device sizes
- **Step Indicators**: Clear learning process guidance
- **Real-time Feedback**: Immediate AI responses and status prompts

### Data Management
- **Learning Record Storage**: Complete learning history tracking
- **Progress Statistics**: Learning data analysis and visualization
- **Personalized Recommendations**: Intelligent recommendations based on learning history

## Deployment Instructions

### Production Environment Deployment
1. Use Docker Compose for containerized deployment
2. Configure Nginx reverse proxy
3. Set environment variables and database connections
4. Configure SSL certificates (if needed)

### Demo Environment
- Local development environment: http://localhost:3000
- API documentation: http://localhost:8000/docs
- Database management: Supabase Dashboard

### OCR功能配置

为了使用图片文字识别功能，需要安装Tesseract OCR引擎：

#### 快速安装（推荐）
```bash
# 运行自动安装脚本
install_tesseract.bat
```

#### 手动安装
1. 下载Tesseract OCR：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装时选择中文和英文语言包
3. 配置环境变量
4. 详细说明请查看：`TESSERACT_INSTALLATION_GUIDE.md`

#### 验证安装
```bash
tesseract --version
tesseract --list-langs
```

## Development Roadmap

- [x] Project architecture design
- [x] Backend API development
- [x] Frontend interface development
- [x] AI functionality integration
- [x] Database design
- [x] Deployment configuration
- [ ] Feature testing and optimization
- [ ] Demo video production
- [ ] Documentation completion

## License

MIT License

## Contact Information

For questions or suggestions, please contact:
- Email: your-email@example.com
- GitHub: your-github-username
