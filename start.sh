#!/bin/bash

echo "正在启动抢购系统后台管理..."

# 启动后端
echo "启动后端服务..."
cd backend
python3 app.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 授权测试用户
echo "授权测试用户..."
python3 test_authorize.py

# 启动前端
echo "启动前端服务..."
cd ../frontend
npx vite &
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