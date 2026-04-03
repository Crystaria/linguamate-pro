import React, { useState } from 'react';
import { Key, Server, Cpu, CheckCircle, XCircle, Trash2, Save } from 'lucide-react';
import { useAIConfig } from '../contexts/AIConfigContext';
import { useLanguage } from '../contexts/LanguageContext';

const Settings = () => {
  const { t } = useLanguage();
  const { config, updateConfig, setProvider, clearConfig, testConnection, API_PROVIDERS } = useAIConfig();
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  const handleTestConnection = async () => {
    setTesting(true);
    setTestResult(null);
    const success = await testConnection();
    setTestResult(success);
    setTesting(false);
  };

  const handleSave = () => {
    updateConfig({ enabled: true });
    setTestResult(null);
  };

  const handleClear = () => {
    clearConfig();
    setTestResult(null);
  };

  const providerConfig = API_PROVIDERS[config.provider];

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-2">
          <Settings className="w-8 h-8 text-primary-500" />
          <h1 className="text-2xl font-bold text-gray-900">
            {t.language === 'en' ? 'AI Settings' : 'AI 设置'}
          </h1>
        </div>
        <p className="text-gray-600">
          {t.language === 'en'
            ? 'Configure your AI provider to use real API calls instead of demo mode'
            : '配置 AI 提供商以使用真实 API 调用，而非演示模式'}
        </p>
      </div>

      {/* Usage Mode */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          {t.language === 'en' ? 'Usage Mode' : '使用方式'}
        </h2>
        <div className="space-y-3">
          <label className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
            <input
              type="radio"
              name="usageMode"
              checked={!config.enabled}
              onChange={() => updateConfig({ enabled: false })}
              className="w-4 h-4 text-primary-500"
            />
            <div className="ml-3">
              <span className="font-medium text-gray-900">
                {t.language === 'en' ? 'Demo Mode (No configuration required)' : 'Demo 模式（无需配置）'}
              </span>
              <p className="text-sm text-gray-500">
                {t.language === 'en'
                  ? 'Use built-in demo responses for quick testing'
                  : '使用内置演示回复进行快速测试'}
              </p>
            </div>
          </label>
          <label className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50">
            <input
              type="radio"
              name="usageMode"
              checked={config.enabled}
              onChange={() => updateConfig({ enabled: true })}
              className="w-4 h-4 text-primary-500"
            />
            <div className="ml-3">
              <span className="font-medium text-gray-900">
                {t.language === 'en' ? 'Use your own API Key' : '使用自己的 API Key'}
              </span>
              <p className="text-sm text-gray-500">
                {t.language === 'en'
                  ? 'Configure your API provider for real AI responses'
                  : '配置 AI 提供商以获取真实的 AI 回复'}
              </p>
            </div>
          </label>
        </div>
      </div>

      {/* API Configuration */}
      {config.enabled && (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            {t.language === 'en' ? 'API Configuration' : 'API 配置'}
          </h2>

          {/* Provider Selection */}
          <div className="mb-4">
            <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
              <Server className="w-4 h-4 mr-2" />
              {t.language === 'en' ? 'API Provider' : 'API 提供商'}
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {Object.entries(API_PROVIDERS).map(([key, value]) => (
                <button
                  key={key}
                  onClick={() => setProvider(key)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    config.provider === key
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {value.name}
                </button>
              ))}
            </div>
          </div>

          {/* API Key */}
          <div className="mb-4">
            <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
              <Key className="w-4 h-4 mr-2" />
              API Key
            </label>
            <input
              type="password"
              value={config.apiKey}
              onChange={(e) => updateConfig({ apiKey: e.target.value })}
              placeholder={t.language === 'en' ? 'Enter your API Key' : '输入您的 API Key'}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Endpoint */}
          <div className="mb-4">
            <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
              <Server className="w-4 h-4 mr-2" />
              {t.language === 'en' ? 'API Endpoint' : 'API 端点'}
            </label>
            <input
              type="text"
              value={config.endpoint}
              onChange={(e) => updateConfig({ endpoint: e.target.value })}
              placeholder={providerConfig.defaultEndpoint || (t.language === 'en' ? 'Enter custom endpoint' : '输入自定义端点')}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            {config.provider !== 'custom' && (
              <p className="text-xs text-gray-500 mt-1">
                {t.language === 'en' ? 'Default:' : '默认：'} {providerConfig.defaultEndpoint}
              </p>
            )}
          </div>

          {/* Model Selection */}
          <div className="mb-4">
            <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
              <Cpu className="w-4 h-4 mr-2" />
              {t.language === 'en' ? 'Model' : '模型'}
            </label>
            {config.provider === 'custom' ? (
              <input
                type="text"
                value={config.model}
                onChange={(e) => updateConfig({ model: e.target.value })}
                placeholder={t.language === 'en' ? 'Enter model name' : '输入模型名称'}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            ) : (
              <select
                value={config.model}
                onChange={(e) => updateConfig({ model: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                {providerConfig.models.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Test Result */}
          {testResult !== null && (
            <div className={`mb-4 p-3 rounded-lg flex items-center ${
              testResult ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
            }`}>
              {testResult ? (
                <CheckCircle className="w-5 h-5 mr-2" />
              ) : (
                <XCircle className="w-5 h-5 mr-2" />
              )}
              <span>
                {testResult
                  ? (t.language === 'en' ? 'Connection successful!' : '连接成功！')
                  : (t.language === 'en' ? 'Connection failed. Please check your configuration.' : '连接失败，请检查配置。')}
              </span>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-3 pt-4 border-t">
            <button
              onClick={handleSave}
              className="flex items-center px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
            >
              <Save className="w-4 h-4 mr-2" />
              {t.language === 'en' ? 'Save Configuration' : '保存配置'}
            </button>
            <button
              onClick={handleTestConnection}
              disabled={testing || !config.apiKey}
              className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {testing ? (
                <span className="animate-spin mr-2">⏳</span>
              ) : (
                <CheckCircle className="w-4 h-4 mr-2" />
              )}
              {t.language === 'en' ? 'Test Connection' : '测试连接'}
            </button>
            <button
              onClick={handleClear}
              className="flex items-center px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors"
            >
              <Trash2 className="w-4 h-4 mr-2" />
              {t.language === 'en' ? 'Clear Configuration' : '清除配置'}
            </button>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
        <h3 className="font-semibold text-blue-900 mb-2">
          {t.language === 'en' ? 'Notes' : '注意事项'}
        </h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• {t.language === 'en'
            ? 'API Key is stored locally in your browser and never uploaded to our servers'
            : 'API Key 存储在您的浏览器本地，不会上传到我们的服务器'}</li>
          <li>• {t.language === 'en'
            ? 'API usage fees will be charged by your provider'
            : 'API 使用费用将由您的提供商收取'}</li>
          <li>• {t.language === 'en'
            ? 'You can switch back to Demo mode anytime'
            : '您可以随时切换回 Demo 模式'}</li>
        </ul>
      </div>
    </div>
  );
};

export default Settings;
