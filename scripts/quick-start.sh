#!/bin/bash

# LinguaMate Pro - 一键启动脚本
# 用于快速启动前后端服务，适合演示和开发

echo "🚀 LinguaMate Pro - 一键启动"
echo "=============================="

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未检测到 Node.js，请先安装 Node.js 16+"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python，请先安装 Python 3.8+"
    exit 1
fi

echo "✅ 环境检查通过"

# 启动后端
echo ""
echo "📦 启动后端服务..."
cd backend

if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

echo "启动后端服务器 (http://localhost:8000)"
python main_local.py &
BACKEND_PID=$!

cd ..

# 等待后端启动
sleep 3

# 启动前端
echo ""
echo "🎨 启动前端服务..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo "启动前端服务器 (http://localhost:3000)"
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "=============================="
echo "✅ 服务启动成功！"
echo ""
echo "📱 前端：http://localhost:3000"
echo "🔧 后端：http://localhost:8000"
echo "📖 API 文档：http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "=============================="

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo '👋 服务已停止'; exit" INT

wait
