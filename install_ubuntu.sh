#!/bin/bash

echo "🔧 Ubuntu 24 环境安装脚本"
echo "这将安装运行紫金盘商城系统所需的所有依赖"
echo ""

# 更新系统
echo "📦 更新系统包..."
sudo apt update

# 安装Python3和相关工具
echo "🐍 安装Python3环境..."
sudo apt install -y python3 python3-pip python3-venv python3-dev

# 安装Node.js 18.x
echo "📦 安装Node.js..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# 安装构建工具
echo "🔨 安装构建工具..."
sudo apt install -y build-essential

# 检查安装结果
echo ""
echo "✅ 安装完成！版本信息："
echo "   Python: $(python3 --version)"
echo "   pip: $(pip3 --version)"
echo "   Node.js: $(node --version)"
echo "   npm: $(npm --version)"
echo ""
echo "🚀 现在可以运行 ./start.sh 启动系统了！"