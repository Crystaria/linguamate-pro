import React, { useState, useRef, useEffect } from 'react';
import { Send, FileText, Brain, BookOpen, CheckCircle } from 'lucide-react';
import axios from 'axios';
import { useLanguage } from '../contexts/LanguageContext';
import { useToast } from '../components/Toast';
import API_BASE_URL from '../config';

const TextAnalysis = ({ userLevel }) => {
  const { t, language } = useLanguage();
  const toast = useToast();
  const [text, setText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [exercises, setExercises] = useState(null);
  const [exerciseId, setExerciseId] = useState(null);
  const [userAnswers, setUserAnswers] = useState({});
  const [submittedAnswers, setSubmittedAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);

  const handleTextAnalysis = async () => {
    if (!text.trim()) return;

    setLoading(true);
    try {
        const response = await axios.post(`${API_BASE_URL}/upload/text`, {
          text: text,
          level: userLevel,
          language: language
      });

      if (response.data.success) {
        setAnalysis(response.data.analysis);
        setCurrentStep(2);
        toast.success(t.language === 'en' ? 'Analysis completed!' : '分析完成！');
      }
    } catch (error) {
      console.error('分析失败:', error);
      const errorMsg = error.response?.data?.detail || (t.language === 'en' ? 'Analysis failed, please retry' : '分析失败，请重试');
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateExercises = async () => {
    if (!analysis) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/generate-exercises`, {
        text: text,
        analysis: analysis,
        level: userLevel
      });

      if (response.data.success) {
        setExercises(response.data.exercises);
        setExerciseId(response.data.exercise_id);
        setUserAnswers({});
        setSubmittedAnswers({});
        setCurrentStep(3);
        toast.success(t.language === 'en' ? 'Exercises generated!' : '练习题已生成！');
      }
    } catch (error) {
      console.error('生成练习失败:', error);
      const errorMsg = error.response?.data?.detail || (t.language === 'en' ? 'Failed to generate exercises, please retry' : '生成练习失败，请重试');
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSubmit = async (questionId) => {
    if (!exerciseId || !userAnswers[questionId] || !exercises) return;

    try {
      const response = await axios.post(`${API_BASE_URL}/submit-answer`, null, {
        params: {
          exercise_id: exerciseId,
          question_id: questionId,
          user_answer: userAnswers[questionId],
          questions_data: JSON.stringify(exercises)
        }
      });

      if (response.data.success) {
        setSubmittedAnswers(prev => ({
          ...prev,
          [questionId]: {
            isCorrect: response.data.is_correct,
            correctAnswer: response.data.correct_answer,
            explanation: response.data.explanation,
            userAnswer: response.data.user_answer
          }
        }));
        toast.success(response.data.is_correct ?
          (t.language === 'en' ? 'Correct!' : '回答正确！') :
          (t.language === 'en' ? 'Answer submitted' : '答案已提交'));
      }
    } catch (error) {
      console.error('提交答案失败:', error);
      toast.error(t.language === 'en' ? 'Failed to submit answer, please retry' : '提交答案失败，请重试');
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const sampleTexts = [
    "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet.",
    "Learning a new language is like opening a door to a new world. It allows you to communicate with people from different cultures and understand their perspectives.",
    "Artificial intelligence is transforming the way we learn languages. With AI-powered tools, students can get personalized feedback and practice in real-time."
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{t.textAnalysis.title}</h1>
        <p className="text-gray-600">{t.textAnalysis.subtitle}</p>
      </div>

      {/* 步骤指示器 */}
      <div className="flex items-center justify-center mb-8">
        <div className="flex items-center space-x-4">
          <div className={`flex items-center space-x-2 ${currentStep >= 1 ? 'text-primary-500' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 1 ? 'bg-primary-500 text-white' : 'bg-gray-200'}`}>
              <FileText className="w-4 h-4" />
            </div>
            <span className="text-sm font-medium">{t.textAnalysis.step1.split(': ')[1]}</span>
          </div>
          <div className={`w-8 h-0.5 ${currentStep >= 2 ? 'bg-primary-500' : 'bg-gray-200'}`}></div>
          <div className={`flex items-center space-x-2 ${currentStep >= 2 ? 'text-primary-500' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 2 ? 'bg-primary-500 text-white' : 'bg-gray-200'}`}>
              <Brain className="w-4 h-4" />
            </div>
            <span className="text-sm font-medium">{t.textAnalysis.step2.split(': ')[1]}</span>
          </div>
          <div className={`w-8 h-0.5 ${currentStep >= 3 ? 'bg-primary-500' : 'bg-gray-200'}`}></div>
          <div className={`flex items-center space-x-2 ${currentStep >= 3 ? 'text-primary-500' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 3 ? 'bg-primary-500 text-white' : 'bg-gray-200'}`}>
              <BookOpen className="w-4 h-4" />
            </div>
            <span className="text-sm font-medium">{t.textAnalysis.step3.split(': ')[1]}</span>
          </div>
        </div>
      </div>

      {/* 步骤1: 文本输入 */}
      {currentStep === 1 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">{t.textAnalysis.step1}</h2>
          
          {/* 示例文本 */}
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">
              {t.language === 'zh' ? '或者选择示例文本：' : 'Or choose from sample texts:'}
            </p>
            <div className="space-y-2">
              {sampleTexts.map((sample, index) => (
                <button
                  key={index}
                  onClick={() => setText(sample)}
                  className="block w-full text-left p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-sm"
                >
                  {sample}
                </button>
              ))}
            </div>
          </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={t.textAnalysis.inputPlaceholder}
            className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
          />
          
          <div className="flex items-center justify-between mt-4">
            <span className="text-sm text-gray-500">
              {t.language === 'zh' ? '当前学习等级: ' : 'Current Learning Level: '}
              {t.chat.levels[userLevel]}
            </span>
            <button
              onClick={handleTextAnalysis}
              disabled={!text.trim() || loading}
              className="flex items-center space-x-2 px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <Send className="w-4 h-4" />
              )}
              <span>{t.textAnalysis.analyze}</span>
            </button>
          </div>
        </div>
      )}

      {/* 步骤2: 分析结果 */}
      {currentStep >= 2 && analysis && (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">{t.textAnalysis.step2}</h2>
            <div className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="w-5 h-5" />
              <span className="text-sm">{t.textAnalysis.analysisComplete}</span>
            </div>
          </div>
          
          <div className="prose max-w-none">
            <pre className="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-lg">
              {analysis}
            </pre>
          </div>

          {currentStep === 2 && (
            <div className="mt-6 text-center">
              <button
                onClick={handleGenerateExercises}
                disabled={loading}
                className="flex items-center space-x-2 px-6 py-2 bg-secondary-500 text-white rounded-lg hover:bg-secondary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors mx-auto"
              >
                {loading ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <BookOpen className="w-4 h-4" />
                )}
                <span>{t.textAnalysis.generateExercises}</span>
              </button>
            </div>
          )}
        </div>
      )}

      {/* 原始文本显示 */}
      {currentStep >= 2 && text && (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">{t.textAnalysis.originalText}</h2>
            <div className="flex items-center space-x-2 text-blue-600">
              <FileText className="w-5 h-5" />
              <span className="text-sm">{t.textAnalysis.originalTextTitle}</span>
            </div>
          </div>
          
          <p className="text-sm text-gray-600 mb-4">{t.textAnalysis.originalTextDescription}</p>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">
              {text}
            </pre>
          </div>
        </div>
      )}

      {/* 步骤3: 练习题 */}
      {currentStep >= 3 && exercises && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">{t.textAnalysis.step3}</h2>
            <div className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="w-5 h-5" />
              <span className="text-sm">{t.textAnalysis.exercisesComplete}</span>
            </div>
          </div>
          
          <div className="prose max-w-none">
            {typeof exercises === 'string' ? (
              <pre className="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-lg">
                {exercises}
              </pre>
            ) : (
              <div className="space-y-6">
                {Array.isArray(exercises) && exercises.map((question, index) => (
                  <div key={question.id || index} className="border-l-4 border-blue-500 pl-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="font-medium mb-3 text-lg">{question.question}</p>
                      <div className="space-y-2 mb-4">
                        {question.options && question.options.map((option, optIndex) => (
                          <label key={optIndex} className="flex items-center space-x-2 cursor-pointer">
                            <input 
                              type="radio" 
                              name={`q${question.id || index}`} 
                              value={option} 
                              className="text-blue-600"
                              onChange={(e) => handleAnswerChange(question.id || index, option)}
                              disabled={submittedAnswers[question.id || index]}
                            />
                            <span className={submittedAnswers[question.id || index] ? 'opacity-75' : ''}>{option}</span>
                          </label>
                        ))}
                      </div>
                      
                      {userAnswers[question.id || index] && !submittedAnswers[question.id || index] && (
                        <button
                          onClick={() => handleAnswerSubmit(question.id || index)}
                          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                        >
                          {t.textAnalysis.submitAnswer}
                        </button>
                      )}
                      
                      {submittedAnswers[question.id || index] && (
                        <div className={`mt-4 p-3 rounded-lg ${
                          submittedAnswers[question.id || index].isCorrect 
                            ? 'bg-green-100 border border-green-300' 
                            : 'bg-red-100 border border-red-300'
                        }`}>
                          <div className="flex items-center space-x-2 mb-2">
                            {submittedAnswers[question.id || index].isCorrect ? (
                              <CheckCircle className="w-5 h-5 text-green-600" />
                            ) : (
                              <span className="w-5 h-5 text-red-600">✗</span>
                            )}
                            <span className={`font-medium ${
                              submittedAnswers[question.id || index].isCorrect ? 'text-green-800' : 'text-red-800'
                            }`}>
                              {submittedAnswers[question.id || index].isCorrect ? t.textAnalysis.correct : t.textAnalysis.incorrect}
                            </span>
                          </div>
                          <p className="text-sm text-gray-700 mb-1">
                            <strong>{t.textAnalysis.yourAnswer}：</strong>{submittedAnswers[question.id || index].userAnswer}
                          </p>
                          <p className="text-sm text-gray-700 mb-2">
                            <strong>{t.textAnalysis.correctAnswer}：</strong>{submittedAnswers[question.id || index].correctAnswer}
                          </p>
                          {submittedAnswers[question.id || index].explanation && (
                            <p className="text-sm text-gray-700">
                              <strong>{t.textAnalysis.explanation}：</strong>{submittedAnswers[question.id || index].explanation}
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={() => {
                setCurrentStep(1);
                setText('');
                setAnalysis(null);
                setExercises(null);
                setExerciseId(null);
                setUserAnswers({});
                setSubmittedAnswers({});
              }}
              className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              {t.textAnalysis.restart}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TextAnalysis;
