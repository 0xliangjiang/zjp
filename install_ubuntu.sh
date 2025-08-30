#!/bin/bash

echo "🔧 Ubuntu 24 环境安装脚本"
echo "这将检查并安装运行紫金盘商城系统所需的所有依赖"
echo ""

# 检查并安装Python3
echo "🐍 检查Python3环境..."
if command -v python3 &> /dev/null; then
    echo "   ✅ Python3 已安装: $(python3 --version)"
else
    echo "   📦 安装Python3..."
    sudo apt update
    sudo apt install -y python3
fi

# 检查并安装pip
echo "🔧 检查pip..."
if command -v pip3 &> /dev/null; then
    echo "   ✅ pip3 已安装: $(pip3 --version)"
else
    echo "   📦 安装pip3..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# 检查并安装venv
echo "📦 检查python3-venv..."
if python3 -c "import venv" 2>/dev/null; then
    echo "   ✅ python3-venv 已安装"
else
    echo "   📦 安装python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# 安装python3-dev（可能需要编译某些包）
echo "🔧 检查python3-dev..."
if dpkg -l | grep -q python3-dev; then
    echo "   ✅ python3-dev 已安装"
else
    echo "   📦 安装python3-dev..."
    sudo apt install -y python3-dev
fi

# 检查并安装Node.js
echo "📦 检查Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | sed 's/v//')
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
    if [ "$NODE_MAJOR" -ge "16" ]; then
        echo "   ✅ Node.js 已安装: v$NODE_VERSION"
    else
        echo "   ⚠️  Node.js 版本过低: v$NODE_VERSION，需要升级到18+"
        echo "   📦 安装Node.js 18..."
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
else
    echo "   📦 安装Node.js 18..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# 检查并安装构建工具
echo "🔨 检查构建工具..."
if command -v gcc &> /dev/null; then
    echo "   ✅ 构建工具已安装"
else
    echo "   📦 安装构建工具..."
    sudo apt install -y build-essential
fi

# 最终检查
echo ""
echo "🎉 环境检查完成！版本信息："
echo "   Python: $(python3 --version 2>/dev/null || echo '❌ 未安装')"
echo "   pip: $(pip3 --version 2>/dev/null | head -n1 || echo '❌ 未安装')"
echo "   Node.js: $(node --version 2>/dev/null || echo '❌ 未安装')"
echo "   npm: $(npm --version 2>/dev/null || echo '❌ 未安装')"
echo "   venv: $(python3 -c 'import venv; print("✅ 可用")' 2>/dev/null || echo '❌ 不可用')"
echo ""
echo "🚀 现在可以运行 ./start.sh 启动系统了！"