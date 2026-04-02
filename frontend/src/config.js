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
