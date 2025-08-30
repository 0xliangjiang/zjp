# 紫金盘商城系统

一个基于 Flask + Vue.js 的商城管理系统。

## 系统要求

- Ubuntu 24.04 LTS（推荐）
- Python 3.8+ 
- Node.js 18+
- 2GB+ RAM

## 快速开始（Ubuntu 24）

### 方法一：完整安装（首次使用推荐）

```bash
# 1. 克隆项目
git clone https://github.com/0xliangjiang/zjp.git
cd zjp

# 2. 检查并安装环境依赖
./install_ubuntu.sh

# 3. 启动系统
./start.sh
```

### 方法二：快速启动（已有Python3和Node.js）

```bash
# 克隆项目
git clone https://github.com/0xliangjiang/zjp.git
cd zjp

# 快速启动（跳过环境检查）
./quick_start.sh
```

### 停止系统

```bash
# 停止所有服务
./stop.sh
```

## 项目结构

```
zjp/
├── backend/                    # Flask 后端
│   ├── app.py                 # 主应用文件
│   ├── requirements.txt       # Python 依赖
│   └── venv/                  # Python虚拟环境（自动创建）
├── frontend/                  # Vue.js 前端
│   ├── src/
│   │   ├── components/        # 组件
│   │   ├── views/            # 页面
│   │   ├── App.vue           # 根组件
│   │   └── main.js           # 入口文件
│   ├── node_modules/         # 前端依赖（自动安装）
│   ├── package.json
│   └── vite.config.js
├── install_ubuntu.sh         # Ubuntu环境检查安装脚本
├── start.sh                  # 完整启动脚本（含环境检查）
├── quick_start.sh            # 快速启动脚本（跳过环境检查）
├── stop.sh                   # 停止脚本
└── README.md
```

## 脚本说明

### install_ubuntu.sh
- 智能检查已安装的组件
- 只安装缺失的依赖项
- 检查Python3、pip、venv、Node.js版本
- 避免重复安装

### start.sh
- 检查环境依赖
- 自动创建Python虚拟环境（backend/venv/）
- 激活虚拟环境并安装Python依赖
- 自动安装前端依赖（如果不存在）
- 启动后端和前端服务

### quick_start.sh
- 跳过环境检查，直接启动
- 适合已确认环境正常的情况
- 更快的启动速度

### stop.sh  
- 优雅停止所有服务
- 清理进程

### 手动启动

**后端启动：**
1. 进入后端目录：
```bash
cd backend
```

2. 安装依赖：
```bash
pip3 install -r requirements.txt
```

3. 启动后端服务：
```bash
python3 app.py
```

后端服务将在 `http://localhost:5001` 启动。

**前端启动：**
1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动前端服务：
```bash
npm run dev
```

前端服务将在 `http://localhost:3001` 启动。

## 使用说明

### 管理员授权用户

使用以下 API 为用户授权：

```bash
curl -X POST http://localhost:5001/api/authorize_user \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000"}'
```

或者使用提供的测试脚本：
```bash
cd backend
python3 test_authorize.py
```

### 登录流程

1. 在登录页面输入手机号和密码
2. 点击"登录"按钮
3. 成功登录后进入后台管理页面
4. 默认密码为：123456

### 功能使用

- **市场列表**：查看市场商品，支持多线程抢购和超级抢购功能
- **商品列表**：浏览可购买商品，查看商品详情
- **持仓管理**：查看持仓情况，计算日收益
- **托管管理**：设置定时抢购任务，保存token和抢购设置，到点自动执行
- **用户信息**：查看账户余额、盈利情况和基本信息

## 开发说明

### 后端 API 接口

- `POST /api/login_password` - 用户登录
- `POST /api/GetUserInfo` - 获取用户信息
- `POST /api/proxy/<endpoint>` - 通用代理接口，转发到抢购平台
- `GET /api/proxy/tasks` - 获取托管任务列表
- `POST /api/proxy/tasks` - 创建托管任务
- `POST /api/proxy/tasks/<id>/start` - 立即执行任务
- `POST /api/proxy/tasks/<id>/cancel` - 取消任务
- `GET /api/proxy/tasks/<id>/logs` - 获取任务日志
- `POST /api/proxy/multi_purchase` - 多线程并发抢购
- `GET /api/test_connection` - 测试网络连接

### 系统架构

- 中间件代理模式，转发请求到抢购平台
- 用户授权验证机制
- 实时抢购日志记录
- 多线程并发抢购，提高成功率
- 自动抢购重试机制
- 托管任务管理，定时自动执行

### 技术栈

**后端：**
- Flask - Web 框架
- Requests - HTTP 客户端
- 代理转发模式
- 用户授权验证

**前端：**
- Vue.js 3 - 前端框架
- Element Plus - UI 组件库
- Axios - HTTP 客户端
- Vite - 构建工具

## 使用提示

- 后端运行在 `http://localhost:5001`
- 前端运行在 `http://localhost:3001`
- 使用 `./start.sh` 一键启动所有服务
- 授权用户：15192025411
- 支持自动抢购和实时日志记录

## 注意事项

1. 系统采用中间件代理模式，转发请求到抢购平台
2. 支持自定义抢购签名和密码
3. 自动抢购支持设置重试次数和间隔时间
4. 需要先授权用户才能登录系统