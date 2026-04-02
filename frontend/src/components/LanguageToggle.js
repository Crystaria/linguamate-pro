import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Globe } from 'lucide-react';

const LanguageToggle = () => {
  const { language, toggleLanguage, t } = useLanguage();

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center space-x-2 px-3 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
      title={t.language === 'zh' ? '切换到英文' : 'Switch to Chinese'}
    >
      <Globe className="w-4 h-4" />
      <span className="text-sm font-medium">
        {t.language === 'zh' ? 'English' : '中文'}
      </span>
    </button>
  );
};

export default LanguageToggle;



