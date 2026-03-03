#!/bin/bash

# LinguaMate Pro - 一键部署到云端
# 免费部署到 Vercel + Railway

echo "🚀 LinguaMate Pro - 一键部署到云端"
echo "======================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未检测到 Node.js，请先安装 Node.js 16+"
    exit 1
fi

# 检查 Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "正在安装 Vercel CLI..."
    npm install -g vercel
fi

# 检查 Railway CLI
if ! command -v railway &> /dev/null; then
    echo "正在安装 Railway CLI..."
    npm install -g @railway/cli
fi

echo ""
echo "======================================"
echo "📦 第一步：部署前端到 Vercel"
echo "======================================"
echo ""

cd frontend

# Vercel 登录
echo "请登录 Vercel（如果已登录可跳过）"
vercel login

# 部署
echo ""
echo "开始部署前端..."
vercel --prod

echo ""
echo "✅ 前端部署完成！"
echo "请记录前端域名（上面输出的 URL）"

cd ..

echo ""
echo "======================================"
echo "🔧 第二步：部署后端到 Railway"
echo "======================================"
echo ""

# Railway 登录
echo "请登录 Railway（如果已登录可跳过）"
railway login

# 部署
echo ""
echo "开始部署后端..."
cd backend
railway init
railway up

echo ""
echo "✅ 后端部署完成！"
echo "请记录后端域名（上面输出的 URL）"

cd ..

echo ""
echo "======================================"
echo "🎉 部署完成！"
echo "======================================"
echo ""
echo "接下来："
echo "1. 在 Railway 控制台获取后端域名"
echo "2. 在 Vercel 控制台添加环境变量 REACT_APP_API_URL"
echo "3. 重新部署前端"
echo ""
echo "详细步骤请查看：📖在线部署指南.md"
echo ""
