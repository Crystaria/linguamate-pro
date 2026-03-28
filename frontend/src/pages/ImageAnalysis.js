import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon, Brain, BookOpen, CheckCircle, X } from 'lucide-react';
import axios from 'axios';
import { useLanguage } from '../contexts/LanguageContext';
import API_BASE_URL from '../config';

const ImageAnalysis = ({ userLevel }) => {
  const { t, language } = useLanguage();
  const toast = useToast();
  const [uploadedFile, setUploadedFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [exercises, setExercises] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [exerciseId, setExerciseId] = useState(null);
  const [userAnswers, setUserAnswers] = useState({});
  const [submittedAnswers, setSubmittedAnswers] = useState({});

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      setCurrentStep(1);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    maxFiles: 1
  });

  const handleImageAnalysis = async () => {
    if (!uploadedFile) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('level', userLevel);
      formData.append('language', language);

      const response = await axios.post(`${API_BASE_URL}/upload/image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setExtractedText(response.data.extracted_text);
        setAnalysis(response.data.analysis);
        setCurrentStep(2);
      }
    } catch (error) {
      console.error('图片分析失败:', error);
      console.error('错误详情:', error.response?.data);
      const errorMessage = error.response?.data?.detail || error.message || (t.language === 'en' ? 'Image analysis failed, please retry' : '图片分析失败，请重试');
      const alertMsg = t.language === 'en' ? `Image analysis failed: ${errorMessage}` : `图片分析失败: ${errorMessage}`;
      toast.error(alertMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateExercises = async () => {
    if (!analysis || !extractedText) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/generate-exercises`, {
        text: extractedText,
        analysis: analysis,
        level: userLevel
      });

      if (response.data.success) {
        setExercises(response.data.exercises);
        setExerciseId(response.data.exercise_id);
        setCurrentStep(3);
      }
    } catch (error) {
      console.error('生成练习失败:', error);
      console.error('错误详情:', error.response?.data);
      const errorMessage = error.response?.data?.detail || error.message || (t.language === 'en' ? 'Failed to generate exercises, please retry' : '生成练习失败，请重试');
      const alertMsg = t.language === 'en' ? `Failed to generate exercises: ${errorMessage}` : `生成练习失败: ${errorMessage}`;
      toast.error(alertMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
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
      }
    } catch (error) {
      console.error('提交答案失败:', error);
      alert(t.language === 'en' ? 'Failed to submit answer' : '提交答案失败');
    }
  };

  const resetAnalysis = () => {
    setUploadedFile(null);
    setExtractedText('');
    setAnalysis(null);
    setExercises(null);
    setCurrentStep(1);
    setExerciseId(null);
    setUserAnswers({});
    setSubmittedAnswers({});
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{t.imageAnalysis.title}</h1>
        <p className="text-gray-600">{t.imageAnalysis.subtitle}</p>
      </div>

      {/* 步骤指示器 */}
      <div className="flex items-center justify-center mb-8">
        <div className="flex items-center space-x-2">
          <div className={`flex items-center space-x-2 ${currentStep >= 1 ? 'text-primary-500' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 1 ? 'bg-primary-500 text-white' : 'bg-gray-200'}`}>
              <ImageIcon className="w-4 h-4" />
            </div>
            <span className="text-sm font-medium">{t.language === 'en' ? 'Upload' : '上传'}</span>
          </div>
          <div className={`w-6 h-0.5 ${currentStep >= 2 ? 'bg-primary-500' : 'bg-gray-200'}`}></div>
          <div className={`flex items-center space-x-2 ${currentStep >= 2 ? 'text-primary-500' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 2 ? 'bg-primary-500 text-white' : 'bg-gray-200'}`}>
              <Brain className="w-4 h-4" />
            </div>
            <span className="text-sm font-medium">{t.language === 'en' ? 'Analysis' : '分析'}</span>
          </div>
          <div className={`w-6 h-0.5 ${currentStep >= 3 ? 'bg-primary-500' : 'bg-gray-200'}`}></div>
          <div className={`flex items-center space-x-2 ${currentStep >= 3 ? 'text-primary-500' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 3 ? 'bg-primary-500 text-white' : 'bg-gray-200'}`}>
              <BookOpen className="w-4 h-4" />
            </div>
            <span className="text-sm font-medium">{t.language === 'en' ? 'Exercises' : '练习题'}</span>
          </div>
        </div>
      </div>

      {/* 步骤1: 图片上传 */}
      {currentStep === 1 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">{t.imageAnalysis.step1}</h2>
          
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            {isDragActive ? (
              <p className="text-primary-600">
                {t.language === 'zh' ? '释放文件以上传...' : 'Drop file to upload...'}
              </p>
            ) : (
              <div>
                <p className="text-gray-600 mb-2">
                  {t.language === 'en' ? (
                    <>Drag image here, or <span className="text-primary-500">click to select file</span></>
                  ) : (
                    <>拖拽图片到这里，或 <span className="text-primary-500">点击选择文件</span></>
                  )}
                </p>
                <p className="text-sm text-gray-500">
                  {t.imageAnalysis.supportedFormats}
                </p>
              </div>
            )}
          </div>

          {uploadedFile && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <ImageIcon className="w-8 h-8 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">{uploadedFile.name}</p>
                    <p className="text-sm text-gray-500">
                      {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setUploadedFile(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
          )}

          <div className="flex items-center justify-between mt-6">
            <span className="text-sm text-gray-500">
              {t.language === 'en' ? 'Current Learning Level: ' : '当前学习等级: '}{userLevel === 'beginner' ? (t.language === 'en' ? 'Beginner' : '初学者') : userLevel === 'intermediate' ? (t.language === 'en' ? 'Intermediate' : '中级') : (t.language === 'en' ? 'Advanced' : '高级')}
            </span>
            <button
              onClick={handleImageAnalysis}
              disabled={!uploadedFile || loading}
              className="flex items-center space-x-2 px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <Brain className="w-4 h-4" />
              )}
              <span>{t.imageAnalysis.startAnalysis}</span>
            </button>
          </div>
        </div>
      )}

      {/* 步骤2: OCR识别和分析结果 */}
      {currentStep >= 2 && (
        <div className="space-y-6">
          {/* 识别的文本 */}
          {extractedText && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">{t.imageAnalysis.extractedText}</h2>
                <div className="flex items-center space-x-2 text-green-600">
                  <CheckCircle className="w-5 h-5" />
                  <span className="text-sm">{t.imageAnalysis.ocrComplete}</span>
                </div>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg">
                <pre className="whitespace-pre-wrap text-sm text-gray-700">
                  {extractedText}
                </pre>
              </div>
            </div>
          )}

          {/* 分析结果 */}
          {analysis && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">{t.imageAnalysis.analysisResult}</h2>
                <div className="flex items-center space-x-2 text-green-600">
                  <CheckCircle className="w-5 h-5" />
                  <span className="text-sm">{t.imageAnalysis.analysisComplete}</span>
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
                    <span>{t.imageAnalysis.generateExercises}</span>
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* 步骤3: 练习题 */}
      {currentStep >= 3 && exercises && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">{t.imageAnalysis.personalizedExercises}</h2>
            <div className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="w-5 h-5" />
              <span className="text-sm">{t.imageAnalysis.exercisesComplete}</span>
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
                          {t.imageAnalysis.submitAnswer || (language === 'en' ? 'Submit Answer' : '提交答案')}
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
                              {submittedAnswers[question.id || index].isCorrect 
                                ? (language === 'en' ? 'Correct!' : '正确！')
                                : (language === 'en' ? 'Incorrect' : '不正确')
                              }
                            </span>
                          </div>
                          <div className="text-sm text-gray-700 mb-2">
                            <span className="font-medium">
                              {language === 'en' ? 'Your answer:' : '您的答案：'}
                            </span> {submittedAnswers[question.id || index].userAnswer}
                          </div>
                          {!submittedAnswers[question.id || index].isCorrect && (
                            <div className="text-sm text-gray-700 mb-2">
                              <span className="font-medium">
                                {language === 'en' ? 'Correct answer:' : '正确答案：'}
                              </span> {submittedAnswers[question.id || index].correctAnswer}
                            </div>
                          )}
                          <div className="text-sm text-gray-600">
                            <span className="font-medium">
                              {language === 'en' ? 'Explanation:' : '解释：'}
                            </span> {submittedAnswers[question.id || index].explanation}
                          </div>
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
              onClick={resetAnalysis}
              className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
{t.imageAnalysis.restart}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageAnalysis;
