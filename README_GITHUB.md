# 🌟 LinguaMate AI - Intelligent Language Learning Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)

> An AI-powered language learning platform featuring intelligent text analysis, image recognition, personalized exercises, and natural conversation practice.

## 🚀 **Live Demo**

Visit the live application: [LinguaMate AI Demo](https://your-demo-url.com)

## ✨ **Key Features**

### 🧠 **Intelligent Text Analysis**
- **Multi-level Analysis**: Beginner, Intermediate, and Advanced linguistic analysis
- **Content-based Exercises**: Generate relevant questions based on input text
- **Real-time Feedback**: Instant answer validation with explanations

### 🖼️ **Image Analysis & OCR**
- **Text Extraction**: Extract text from images using OCR technology
- **Linguistic Processing**: Analyze extracted text with AI-powered insights
- **Visual Learning**: Combine image and text analysis for comprehensive learning

### 💬 **AI Chat Practice**
- **Scenario-based Conversations**: Practice in realistic scenarios (restaurant, shopping, directions, introductions)
- **Custom Scenarios**: Create your own conversation scenarios
- **Natural AI Responses**: Context-aware, human-like AI conversations
- **Multi-level Support**: Adapts to your learning level (Beginner/Intermediate/Advanced)

### 🌍 **Multilingual Support**
- **Bilingual Interface**: Full Chinese/English language switching
- **Smart Language Detection**: AI automatically responds in the appropriate language
- **Cultural Context**: Understanding of cultural nuances in conversations

### 📊 **Learning Analytics**
- **Progress Tracking**: Monitor your learning journey
- **Performance Metrics**: Track improvement over time
- **Learning History**: Review past exercises and conversations

## 🛠️ **Technology Stack**

### **Frontend**
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API communication
- **React Context** - State management for internationalization

### **Backend**
- **FastAPI** - High-performance Python web framework
- **Pydantic** - Data validation and serialization
- **Pillow & PyTesseract** - Image processing and OCR
- **Uvicorn** - ASGI server for FastAPI

### **AI & NLP**
- **Local AI Models** - No external API dependencies
- **Custom Language Models** - Tailored for language learning
- **Context-aware Responses** - Maintains conversation context
- **Scenario-based Intelligence** - Adapts to different conversation contexts

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- npm or yarn

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Crystaria/linguamate-ai.git
   cd linguamate-ai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main_local.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📖 **Usage Guide**

### **Text Analysis**
1. Navigate to "Text Analysis" page
2. Enter English text for analysis
3. Select your learning level
4. Review linguistic analysis results
5. Generate and complete personalized exercises

### **Image Analysis**
1. Go to "Image Analysis" page
2. Upload an image containing text
3. View extracted text content
4. Analyze linguistic features
5. Practice with generated exercises

### **AI Chat Practice**
1. Visit "AI Chat Practice" page
2. Choose a conversation scenario or create custom ones
3. Start natural conversations with AI
4. Practice real-world language skills

## 🎯 **Learning Levels**

### **Beginner Level**
- Simple vocabulary and basic grammar
- Clear, straightforward explanations
- Basic conversation patterns
- Foundation building exercises

### **Intermediate Level**
- Complex sentence structures
- Advanced vocabulary introduction
- Contextual understanding
- Critical thinking development

### **Advanced Level**
- Sophisticated language analysis
- Academic and professional vocabulary
- Cultural context and nuances
- Advanced communication skills

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the backend directory:
```env
# Optional: OpenAI API Key (for enhanced features)
OPENAI_API_KEY=your_api_key_here

# Tesseract OCR Configuration
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### **OCR Setup (Optional)**
For image analysis features, install Tesseract OCR:
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **FastAPI** team for the excellent web framework
- **React** team for the powerful UI library
- **Tailwind CSS** for the utility-first CSS framework
- **OpenAI** for AI model inspiration (when using external APIs)

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/Crystaria/linguamate-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Crystaria/linguamate-ai/discussions)
- **Email**: support@linguamate-ai.com

## 🌟 **Star History**

If you find this project helpful, please give it a star! ⭐

---

**Made with ❤️ for language learners worldwide**

