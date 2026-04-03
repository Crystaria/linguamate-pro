import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageCircle, User, Bot, RotateCcw } from 'lucide-react';
import axios from 'axios';
import { useLanguage } from '../contexts/LanguageContext';
import { useAIConfig } from '../contexts/AIConfigContext';
import API_BASE_URL, { IS_DEMO_MODE, callAI_API, CHAT_REPLY_PROMPT } from '../config';

// Demo 模式回复模板
const DEMO_REPLIES = {
  restaurant: [
    { en: "Great choice! Our pasta is freshly made today. Would you like any sauce with that?", zh: "很好的选择！我们的意大利面是今天新鲜做的。您需要配什么酱吗？" },
    { en: "Excellent! I'll bring that right out for you. Anything to drink?", zh: "好的！我马上为您端上来。需要喝点什么吗？" },
    { en: "Perfect! Enjoy your meal!", zh: "完美！请享用您的美食！" }
  ],
  direction: [
    { en: "Oh, the train station? It's about 5 minutes walk. Go straight and turn left at the second crossing.", zh: "哦，火车站啊？步行大约 5 分钟。直走，在第二个路口左转。" },
    { en: "Yes, you'll see a big supermarket on the corner. The station is right there.", zh: "对的，你会在拐角看到一个大超市。火车站就在那里。" }
  ],
  shopping: [
    { en: "That shirt is $29.99. We also have it in other colors if you'd like to try!", zh: "这件衬衫 29.99 美元。我们还有其他颜色，您想试试吗？" },
    { en: "The fitting room is right over there. Let me know if you need any help!", zh: "试衣间就在那边。需要帮助请告诉我！" }
  ],
  introduction: [
    { en: "Nice to meet you! Where are you from originally?", zh: "很高兴认识你！你原来是哪里人？" },
    { en: "That's wonderful! What brings you here?", zh: "太棒了！是什么让你来到这里的？" }
  ]
};

const ChatPractice = ({ userLevel }) => {
  const { t, language } = useLanguage();
  const { config: aiConfig } = useAIConfig();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState('');
  const [conversationStarted, setConversationStarted] = useState(false);
  const [customScenarios, setCustomScenarios] = useState([]);
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [customScenarioName, setCustomScenarioName] = useState('');
  const [customScenarioDescription, setCustomScenarioDescription] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startConversation = async (scenario) => {
    setSelectedScenario(scenario);
    setConversationStarted(true);
    
    // 根据场景生成开场白
    let openingMessage = '';
    switch (scenario) {
      case 'restaurant':
        openingMessage = t.language === 'en' 
          ? "Good evening! Welcome to our restaurant. I'm your server today. Would you like to see our menu?"
          : "晚上好！欢迎来到我们餐厅。我是您今天的服务员。您想看看我们的菜单吗？";
        break;
      case 'shopping':
        openingMessage = t.language === 'en'
          ? "Hello! Welcome to our store! How can I help you find what you're looking for today?"
          : "您好！欢迎来到我们商店！今天我可以帮您找到什么呢？";
        break;
      case 'direction':
        openingMessage = t.language === 'en'
          ? "Excuse me, I noticed you might need some help. Are you looking for directions somewhere?"
          : "打扰一下，我注意到您可能需要帮助。您是在找某个地方的方向吗？";
        break;
      case 'introduction':
        openingMessage = t.language === 'en'
          ? "Hi there! I don't think we've met before. My name is Alex. What's your name?"
          : "你好！我想我们之前没有见过面。我叫小明。您叫什么名字？";
        break;
      default:
        openingMessage = t.language === 'en'
          ? "Hello! How can I help you today?"
          : "您好！今天我可以为您做些什么？";
    }
    
    const aiMessage = { type: 'ai', content: openingMessage };
    setMessages([aiMessage]);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading || !conversationStarted) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setLoading(true);

    // 添加用户消息
    const newMessages = [...messages, { type: 'user', content: userMessage }];
    setMessages(newMessages);

    try {
      // 优先使用 AI 配置调用真实 API
      if (aiConfig.enabled && aiConfig.apiKey) {
        const currentScenario = [...conversationStarters, ...customScenarios].find(s => s.id === selectedScenario);
        const context = currentScenario?.description || selectedScenario || 'casual chat';
        const prompt = CHAT_REPLY_PROMPT
          .replace('{context}', context)
          .replace('{level}', userLevel)
          .replace('{message}', userMessage);

        const result = await callAI_API(prompt, {}, aiConfig);
        setMessages([...newMessages, { type: 'ai', content: result }]);

        // 保存学习记录（每 3 条消息保存一次）
        if ((messages.filter(m => m.type === 'user').length + 1) % 3 === 0) {
          try {
            const conversationContent = messages.map(m => `${m.type === 'user' ? 'User' : 'AI'}: ${m.content}`).join('\n');
            axios.post(`${API_BASE_URL}/learning-records`, null, {
              params: {
                record_type: 'chat_practice',
                level: userLevel,
                content: conversationContent.substring(0, 500),
                context: selectedScenario,
                language: language
              }
            });
          } catch (e) {
            console.warn('保存学习记录失败:', e);
          }
        }
      } else if (IS_DEMO_MODE) {
        // Demo 模式：使用模拟回复
        const replies = DEMO_REPLIES[selectedScenario] || DEMO_REPLIES.introduction;
        const aiCount = messages.filter(m => m.type === 'ai').length;
        const replyIndex = aiCount % replies.length;
        const aiReply = replies[replyIndex][t.language === 'en' ? 'en' : 'zh'];
        setMessages([...newMessages, { type: 'ai', content: aiReply }]);

        // 保存学习记录（每 3 条消息保存一次）
        if ((aiCount + 1) % 3 === 0) {
          try {
            const conversationContent = messages.map(m => `${m.type === 'user' ? 'User' : 'AI'}: ${m.content}`).join('\n');
            axios.post(`${API_BASE_URL}/learning-records`, null, {
              params: {
                record_type: 'chat_practice',
                level: userLevel,
                content: conversationContent.substring(0, 500),
                context: selectedScenario,
                language: language
              }
            });
          } catch (e) {
            console.warn('保存学习记录失败:', e);
          }
        }
      } else {
        // 后端 API 模式
        const conversationHistory = messages
          .filter(msg => msg.type === 'user' || msg.type === 'ai')
          .map(msg => ({
            user_message: msg.type === 'user' ? msg.content : '',
            ai_response: msg.type === 'ai' ? msg.content : ''
          }))
          .filter(msg => msg.user_message || msg.ai_response);

        const currentScenario = [...conversationStarters, ...customScenarios].find(s => s.id === selectedScenario);
        const customScenarioName = selectedScenario?.startsWith('custom_') && currentScenario ? currentScenario.title : null;
        const customScenarioDescription = selectedScenario?.startsWith('custom_') && currentScenario ? currentScenario.description : null;

        const response = await axios.post(`${API_BASE_URL}/chat`, {
          message: userMessage,
          context: selectedScenario,
          level: userLevel,
          conversation_history: conversationHistory,
          custom_scenario_name: customScenarioName,
          custom_scenario_description: customScenarioDescription
        });

        if (response.data.success) {
          setMessages([...newMessages, { type: 'ai', content: response.data.response }]);

          // 保存学习记录（每 3 条消息保存一次）
          const aiCount = messages.filter(m => m.type === 'ai').length;
          if ((aiCount + 1) % 3 === 0) {
            try {
              const conversationContent = messages.map(m => `${m.type === 'user' ? 'User' : 'AI'}: ${m.content}`).join('\n');
              axios.post(`${API_BASE_URL}/learning-records`, null, {
                params: {
                  record_type: 'chat_practice',
                  level: userLevel,
                  content: conversationContent.substring(0, 500),
                  context: selectedScenario,
                  language: language
                }
              });
            } catch (e) {
              console.warn('保存学习记录失败:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('发送消息失败:', error);
      setMessages([...newMessages, {
        type: 'ai',
        content: t.language === 'en' ? 'Sorry, I encountered some issues. Please try again later.' : '抱歉，我遇到了一些问题。请稍后再试。'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const resetChat = () => {
    setMessages([]);
    setSelectedScenario('');
    setConversationStarted(false);
    setInputMessage('');
    setShowCustomInput(false);
    setCustomScenarioName('');
    setCustomScenarioDescription('');
  };

  const conversationStarters = t.language === 'en' ? [
    {
      id: "restaurant",
      title: "Restaurant Ordering",
      description: "Practice ordering food at a restaurant",
      starter: "Hello, I'd like to order some pasta."
    },
    {
      id: "direction",
      title: "Asking for Directions",
      description: "Practice asking for and giving directions",
      starter: "Excuse me, how do I get to the train station?"
    },
    {
      id: "shopping",
      title: "Shopping",
      description: "Practice shopping conversations",
      starter: "How much does this shirt cost?"
    },
    {
      id: "introduction",
      title: "Self Introduction",
      description: "Practice self-introduction and daily conversation",
      starter: "Hello, my name is John, nice to meet you."
    }
  ] : [
    {
      id: "restaurant",
      title: "餐厅点餐",
      description: "练习在餐厅点餐的对话",
      starter: "你好，我想点一份意大利面。"
    },
    {
      id: "direction",
      title: "问路",
      description: "练习问路和指路的对话",
      starter: "请问去火车站怎么走？"
    },
    {
      id: "shopping",
      title: "购物",
      description: "练习在商店购物的对话",
      starter: "这件衣服多少钱？"
    },
    {
      id: "introduction",
      title: "自我介绍",
      description: "练习自我介绍和日常交流",
      starter: "你好，我叫小明，很高兴认识你。"
    }
  ];

  const startScenario = (scenario) => {
    startConversation(scenario.id);
  };

  const addCustomScenario = () => {
    if (customScenarioName.trim() && customScenarioDescription.trim()) {
      const newScenario = {
        id: `custom_${Date.now()}`,
        title: customScenarioName.trim(),
        description: customScenarioDescription.trim(),
        starter: t.language === 'en' ? `Let's practice ${customScenarioName.trim().toLowerCase()}` : `让我们练习${customScenarioName.trim()}`
      };
      
      setCustomScenarios([...customScenarios, newScenario]);
      setCustomScenarioName('');
      setCustomScenarioDescription('');
      setShowCustomInput(false);
    }
  };

  const deleteCustomScenario = (scenarioId) => {
    setCustomScenarios(customScenarios.filter(s => s.id !== scenarioId));
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{t.chat.title}</h1>
        <p className="text-gray-600">{t.chat.subtitle}</p>
      </div>

      {/* 场景选择界面 */}
      {!conversationStarted && (
        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              {t.language === 'en' ? 'Choose a Conversation Scenario' : '选择对话场景'}
            </h2>
            <p className="text-gray-600">
              {t.language === 'en' 
                ? 'Select a scenario to start a natural conversation practice session'
                : '选择一个场景开始自然的对话练习'}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* 预定义场景 */}
            {conversationStarters.map((scenario, index) => (
              <button
                key={index}
                onClick={() => startScenario(scenario)}
                className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 rounded-lg border border-blue-200 hover:border-blue-300 transition-all duration-200 text-left group"
              >
                <div className="flex items-center justify-center w-12 h-12 bg-blue-500 text-white rounded-lg mb-4 group-hover:bg-blue-600 transition-colors">
                  <MessageCircle className="w-6 h-6" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{scenario.title}</h3>
                <p className="text-sm text-gray-600 mb-4">{scenario.description}</p>
                <div className="text-xs text-blue-600 font-medium">
                  {t.language === 'en' ? 'Start Conversation' : '开始对话'} →
                </div>
              </button>
            ))}

            {/* 自定义场景 */}
            {customScenarios.map((scenario, index) => (
              <div
                key={scenario.id}
                className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg border border-green-200 relative group"
              >
                <button
                  onClick={() => startScenario(scenario)}
                  className="w-full text-left"
                >
                  <div className="flex items-center justify-center w-12 h-12 bg-green-500 text-white rounded-lg mb-4 group-hover:bg-green-600 transition-colors">
                    <MessageCircle className="w-6 h-6" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">{scenario.title}</h3>
                  <p className="text-sm text-gray-600 mb-4">{scenario.description}</p>
                  <div className="text-xs text-green-600 font-medium">
                    {t.language === 'en' ? 'Start Conversation' : '开始对话'} →
                  </div>
                </button>
                <button
                  onClick={() => deleteCustomScenario(scenario.id)}
                  className="absolute top-2 right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs hover:bg-red-600 transition-colors"
                  title={t.language === 'en' ? 'Delete' : '删除'}
                >
                  ×
                </button>
              </div>
            ))}

            {/* 添加自定义场景按钮 */}
            <button
              onClick={() => setShowCustomInput(true)}
              className="p-6 bg-gradient-to-br from-gray-50 to-slate-50 hover:from-gray-100 hover:to-slate-100 rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 transition-all duration-200 text-center group"
            >
              <div className="flex items-center justify-center w-12 h-12 bg-gray-400 text-white rounded-lg mb-4 mx-auto group-hover:bg-gray-500 transition-colors">
                <span className="text-xl">+</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">
                {t.language === 'en' ? 'Create Custom' : '创建自定义场景'}
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                {t.language === 'en' ? 'Add your own conversation scenario' : '添加您自己的对话场景'}
              </p>
              <div className="text-xs text-gray-600 font-medium">
                {t.language === 'en' ? 'Click to Add' : '点击添加'} →
              </div>
            </button>
          </div>

          {/* 自定义场景输入表单 */}
          {showCustomInput && (
            <div className="mt-8 p-6 bg-white border border-gray-200 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                {t.language === 'en' ? 'Create Custom Scenario' : '创建自定义场景'}
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.language === 'en' ? 'Scenario Name' : '场景名称'}
                  </label>
                  <input
                    type="text"
                    value={customScenarioName}
                    onChange={(e) => setCustomScenarioName(e.target.value)}
                    placeholder={t.language === 'en' ? 'e.g., Job Interview, Travel Planning' : '例如：工作面试、旅行规划'}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.language === 'en' ? 'Scenario Description' : '场景描述'}
                  </label>
                  <textarea
                    value={customScenarioDescription}
                    onChange={(e) => setCustomScenarioDescription(e.target.value)}
                    placeholder={t.language === 'en' ? 'Describe what this scenario involves...' : '描述这个场景涉及的内容...'}
                    rows={3}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  />
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={addCustomScenario}
                    disabled={!customScenarioName.trim() || !customScenarioDescription.trim()}
                    className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {t.language === 'en' ? 'Create Scenario' : '创建场景'}
                  </button>
                  <button
                    onClick={() => {
                      setShowCustomInput(false);
                      setCustomScenarioName('');
                      setCustomScenarioDescription('');
                    }}
                    className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
                  >
                    {t.language === 'en' ? 'Cancel' : '取消'}
                  </button>
                </div>
              </div>
            </div>
          )}

          <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <div className="w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center">
                  <span className="text-yellow-800 text-sm font-bold">!</span>
                </div>
              </div>
              <div className="text-sm text-yellow-800">
                <p className="font-medium mb-1">
                  {t.language === 'en' ? '💡 Conversation Tips:' : '💡 对话技巧：'}
                </p>
                <ul className="list-disc list-inside space-y-1">
                  <li>
                    {t.language === 'en' 
                      ? 'AI will respond naturally based on your selected scenario'
                      : 'AI会根据您选择的场景自然地回应'}
                  </li>
                  <li>
                    {t.language === 'en'
                      ? 'Try to use appropriate vocabulary and expressions for each situation'
                      : '尝试使用适合每种情况的词汇和表达'}
                  </li>
                  <li>
                    {t.language === 'en'
                      ? 'Ask follow-up questions to keep the conversation flowing'
                      : '提出后续问题让对话持续进行'}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 对话界面 */}
      {conversationStarted && (
        <div className="grid lg:grid-cols-4 gap-6">
          {/* 侧边栏 */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-lg font-semibold mb-4">
                {t.language === 'zh' ? '对话设置' : 'Conversation Settings'}
              </h2>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t.language === 'en' ? 'Current Scenario:' : '当前场景：'}
                </label>
                <div className="text-sm text-gray-600 bg-blue-50 p-2 rounded border border-blue-200">
                  {[...conversationStarters, ...customScenarios].find(s => s.id === selectedScenario)?.title}
                </div>
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t.chat.level}
                </label>
                <div className="text-sm text-gray-600 bg-gray-50 p-2 rounded">
                  {t.chat.levels[userLevel]}
                </div>
              </div>

              <button
                onClick={resetChat}
                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                <RotateCcw className="w-4 h-4" />
                <span>{t.chat.clearChat}</span>
              </button>
            </div>
          </div>

        {/* 聊天区域 */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
            {/* 聊天头部 */}
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Linguamate Pro</h3>
                  <p className="text-sm text-gray-500">{t.language === 'en' ? 'Your language learning partner' : '你的语言学习伙伴'}</p>
                </div>
              </div>
            </div>

            {/* 消息列表 */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.length === 0 ? (
                <div className="text-center text-gray-500 mt-8">
                  <MessageCircle className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>{t.language === 'en' ? 'Conversation started! AI is waiting for your response.' : '对话已开始！AI正在等待您的回应。'}</p>
                  <p className="text-sm mt-2">{t.language === 'en' ? 'Type your message below to continue the conversation.' : '在下方输入您的消息来继续对话。'}</p>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`flex items-start space-x-2 max-w-xs lg:max-w-md ${
                        message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                      }`}
                    >
                      <div
                        className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          message.type === 'user'
                            ? 'bg-primary-500'
                            : 'bg-gradient-to-r from-primary-500 to-secondary-500'
                        }`}
                      >
                        {message.type === 'user' ? (
                          <User className="w-4 h-4 text-white" />
                        ) : (
                          <Bot className="w-4 h-4 text-white" />
                        )}
                      </div>
                      <div
                        className={`px-4 py-2 rounded-lg ${
                          message.type === 'user'
                            ? 'bg-primary-500 text-white'
                            : 'bg-gray-100 text-gray-900'
                        }`}
                      >
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                      </div>
                    </div>
                  </div>
                ))
              )}
              
              {loading && (
                <div className="flex justify-start">
                  <div className="flex items-start space-x-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-gray-100 px-4 py-2 rounded-lg">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* 输入区域 */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={t.chat.placeholder}
                  className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                  rows={2}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim() || loading}
                  className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                {t.language === 'zh' ? '按 Enter 发送，Shift + Enter 换行' : 'Press Enter to send, Shift + Enter for new line'}
              </p>
            </div>
          </div>
        </div>
        </div>
      )}
    </div>
  );
};

export default ChatPractice;
