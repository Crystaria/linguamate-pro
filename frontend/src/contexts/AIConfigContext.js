import React, { createContext, useContext, useState, useEffect } from 'react';

const AIConfigContext = createContext();

const API_PROVIDERS = {
  deepseek: {
    name: 'DeepSeek',
    defaultEndpoint: 'https://api.deepseek.com/v1/chat/completions',
    models: ['deepseek-chat', 'deepseek-coder']
  },
  openai: {
    name: 'OpenAI',
    defaultEndpoint: 'https://api.openai.com/v1/chat/completions',
    models: ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo']
  },
  claude: {
    name: 'Claude (Anthropic)',
    defaultEndpoint: 'https://api.anthropic.com/v1/messages',
    models: ['claude-3-haiku-20240307', 'claude-3-sonnet-20240229', 'claude-3-opus-20240229']
  },
  custom: {
    name: '自定义',
    defaultEndpoint: '',
    models: []
  }
};

export const AIConfigProvider = ({ children }) => {
  const [config, setConfig] = useState(() => {
    const saved = localStorage.getItem('linguamate-ai-config');
    return saved ? JSON.parse(saved) : {
      enabled: false,
      provider: 'deepseek',
      apiKey: '',
      model: 'deepseek-chat',
      endpoint: ''
    };
  });

  useEffect(() => {
    localStorage.setItem('linguamate-ai-config', JSON.stringify(config));
  }, [config]);

  const updateConfig = (updates) => {
    setConfig(prev => ({ ...prev, ...updates }));
  };

  const setProvider = (provider) => {
    const providerConfig = API_PROVIDERS[provider];
    updateConfig({
      provider,
      endpoint: providerConfig.defaultEndpoint,
      model: providerConfig.models[0] || ''
    });
  };

  const clearConfig = () => {
    updateConfig({
      enabled: false,
      apiKey: '',
      endpoint: '',
      model: ''
    });
  };

  const testConnection = async () => {
    try {
      const response = await fetch(config.endpoint || API_PROVIDERS[config.provider].defaultEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${config.apiKey}`
        },
        body: JSON.stringify({
          model: config.model,
          messages: [{ role: 'user', content: 'Hello' }],
          max_tokens: 10
        })
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  };

  return (
    <AIConfigContext.Provider value={{
      config,
      updateConfig,
      setProvider,
      clearConfig,
      testConnection,
      API_PROVIDERS
    }}>
      {children}
    </AIConfigContext.Provider>
  );
};

export const useAIConfig = () => {
  const context = useContext(AIConfigContext);
  if (!context) {
    throw new Error('useAIConfig must be used within AIConfigProvider');
  }
  return context;
};
