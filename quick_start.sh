#!/bin/bash

echo "⚡ 快速启动紫金盘商城系统（跳过环境检查）"
echo ""

# 直接进入后端目录
cd backend

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "🐍 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装或更新依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 启动后端服务
echo "🚀 启动后端服务..."
python app.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo "🌐 启动前端服务..."
cd ../frontend

# 安装前端依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

# 启动前端服务
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 系统启动成功！"
echo "📱 后端API: http://localhost:5001"
echo "🌐 前端页面: http://localhost:3001"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap 'echo "正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait