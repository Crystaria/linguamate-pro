// API 配置
// 开发环境使用 localhost，生产环境使用环境变量
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// 导出配置
export const config = {
  API_BASE_URL,
};

// 便捷导出
export default API_BASE_URL;
