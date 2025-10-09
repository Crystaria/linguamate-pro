#!/bin/bash

# LinguaMate AI 项目设置脚本
# 用于快速设置开发环境

echo "🚀 开始设置 LinguaMate AI 开发环境"
echo "=================================="

# 检查必要的工具
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 未安装，请先安装 $1"
        exit 1
    else
        echo "✅ $1 已安装"
    fi
}

echo "🔍 检查必要工具..."
check_command "python3"
check_command "node"
check_command "npm"

# 设置后端环境
echo ""
echo "🔧 设置后端环境..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "创建环境变量文件..."
    cp env_example.txt .env
    echo "⚠️  请编辑 backend/.env 文件，填入必要的API密钥"
fi

cd ..

# 设置前端环境
echo ""
echo "🔧 设置前端环境..."
cd frontend

# 安装依赖
echo "安装Node.js依赖..."
npm install

cd ..

echo ""
echo "🎉 环境设置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 编辑 backend/.env 文件，填入API密钥"
echo "2. 设置 Supabase 数据库（参考 database/README.md）"
echo "3. 启动后端服务：cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "4. 启动前端服务：cd frontend && npm start"
echo ""
echo "🌐 访问地址："
echo "- 前端应用：http://localhost:3000"
echo "- API文档：http://localhost:8000/docs"
echo ""
echo "📚 更多信息请查看 README.md"
