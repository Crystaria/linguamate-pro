// API 配置
// 开发环境使用 localhost，生产环境使用环境变量
// 如果没有配置 API 地址，使用 Demo 模式
const API_BASE_URL = process.env.REACT_APP_API_URL || 'demo';

// 检测是否处于 Demo 模式
export const IS_DEMO_MODE = API_BASE_URL === 'demo';

// 导出配置
export const config = {
  API_BASE_URL,
  IS_DEMO_MODE,
};

// 默认导出
export default API_BASE_URL;

// 调用真实 API 的辅助函数
export const callAI_API = async (endpoint, body, aiConfig) => {
  const url = aiConfig.endpoint || getDefaultEndpoint(aiConfig.provider);

  const messages = [
    { role: 'user', content: typeof body === 'string' ? body : JSON.stringify(body) }
  ];

  const requestBody = {
    model: aiConfig.model,
    messages,
    max_tokens: 2000,
    temperature: 0.7
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${aiConfig.apiKey}`
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || `API Error: ${response.status}`);
  }

  const data = await response.json();
  return data.choices?.[0]?.message?.content || data.choices?.[0]?.text || '';
};

// 获取默认端点
const getDefaultEndpoint = (provider) => {
  const endpoints = {
    deepseek: 'https://api.deepseek.com/v1/chat/completions',
    openai: 'https://api.openai.com/v1/chat/completions',
    claude: 'https://api.anthropic.com/v1/messages',
    custom: ''
  };
  return endpoints[provider] || '';
};

// 分析文本的 Prompt
export const TEXT_ANALYSIS_PROMPT = `You are a professional linguistics teacher. Analyze the following text from a linguistic perspective:

{text}

Provide analysis covering:
1. Vocabulary analysis (difficulty level, word roots, etc.)
2. Grammar structure (sentence types, tense usage, etc.)
3. Semantic analysis (theme, context, etc.)
4. Pragmatic analysis (usage context, audience, etc.)

Keep the analysis clear and educational. Output in the same language as the input text.`;

// 生成练习题的 Prompt
export const EXERCISE_GENERATION_PROMPT = `Based on the following text and analysis, create 5 multiple-choice questions for language learning practice:

Text: {text}
Analysis: {analysis}

Each question should:
- Test comprehension or linguistic knowledge
- Have 4 options (A, B, C, D)
- Include the correct answer

Return ONLY a JSON array in this format:
[
  {
    "id": 1,
    "question": "Question text",
    "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
    "correct": "A"
  }
]`;

// 对话回复的 Prompt
export const CHAT_REPLY_PROMPT = `You are a friendly language learning partner. Respond naturally to the user's message in the context of: {context}

User level: {level}
User message: {message}

Adjust your vocabulary and sentence complexity based on the user's level:
- Beginner: Simple sentences, basic vocabulary
- Intermediate: Moderate complexity, varied sentences
- Advanced: Natural, complex sentences with idioms

Keep responses conversational and encouraging. Output in the same language as the user's message.`;
