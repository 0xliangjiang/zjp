#!/bin/bash

echo "🚀 正在启动紫金盘商城系统..."

# 检查Python3是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    echo "   sudo apt update && sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    echo "   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "   sudo apt-get install -y nodejs"
    exit 1
fi

# 初始化后端虚拟环境
echo "🐍 初始化Python虚拟环境..."
cd backend

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "   创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "   激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "   安装Python依赖..."
pip install -r requirements.txt

# 启动后端服务
echo "🔧 启动后端服务..."
python app.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 初始化前端
echo "📦 初始化前端环境..."
cd ../frontend

# 安装前端依赖（如果node_modules不存在）
if [ ! -d "node_modules" ]; then
    echo "   安装前端依赖..."
    npm install
fi

# 启动前端服务
echo "🌐 启动前端服务..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 系统启动成功！"
echo "📱 后端API: http://localhost:5001"
echo "🌐 前端页面: http://localhost:3001"
echo ""
echo "测试用户（已授权）:"
echo "  📞 13800138000"
echo "  📞 13800138001" 
echo "  📞 13800138002"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap 'echo "正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait