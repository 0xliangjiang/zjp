# 抢购系统后台管理

一个基于 Flask + Vue.js 的抢购系统后台管理网站。

## 项目结构

```
zijinpan/
├── backend/                # Flask 后端
│   ├── app.py             # 主应用文件
│   ├── requirements.txt   # Python 依赖
│   └── shopping_system.db # SQLite 数据库（运行后自动生成）
├── frontend/              # Vue.js 前端
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── views/        # 页面
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 入口文件
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 功能特性

### 认证功能
- 手机号密码登录
- 管理员授权机制
- JWT Token 认证

### 五大功能模块
1. **市场列表** - 查看市场商品和抢购
2. **商品列表** - 浏览可购买商品
3. **持仓管理** - 查看持仓和收益情况
4. **托管管理** - 设置定时抢购任务，自动执行
5. **用户信息** - 查看账户信息和盈利情况

## 快速开始

### 一键启动（推荐）

```bash
./start.sh
```

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