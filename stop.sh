#!/bin/bash

echo "🛑 停止紫金盘商城系统..."

# 查找并停止Python Flask进程
echo "   停止后端服务..."
pkill -f "python.*app.py" 2>/dev/null || true

# 查找并停止Vite/Node进程
echo "   停止前端服务..."
pkill -f "vite" 2>/dev/null || true
pkill -f "npm.*run.*dev" 2>/dev/null || true

# 停止可能的Node.js进程
pkill -f "node.*vite" 2>/dev/null || true

sleep 2

echo "✅ 所有服务已停止"

# 显示剩余的相关进程
REMAINING=$(ps aux | grep -E "(app\.py|vite|node.*dev)" | grep -v grep | wc -l)
if [ $REMAINING -gt 0 ]; then
    echo "⚠️  检测到仍有进程运行："
    ps aux | grep -E "(app\.py|vite|node.*dev)" | grep -v grep
    echo ""
    echo "如需强制停止，请运行: sudo pkill -9 -f 'python.*app.py|vite|node.*dev'"
fi