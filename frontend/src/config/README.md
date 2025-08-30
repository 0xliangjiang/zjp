# 系统配置管理

## 概述

本目录包含系统的统一配置管理，用于集中管理各种常量和配置参数，避免在多个文件中重复定义相同的值。

## 文件结构

```
config/
├── constants.js    # 系统常量配置
└── README.md       # 配置说明文档
```

## 配置项说明

### SYSTEM_CONFIG

#### DEFAULT_SIGN
- **类型**: String
- **默认值**: 'uCsxXhfsdXNrstuGsRYR'
- **说明**: 系统默认的签名值，用于抢购接口
- **使用位置**: MarketList.vue, Management.vue

#### DEFAULT_PASSWORD
- **类型**: String
- **默认值**: '200412'
- **说明**: 系统默认的抢购密码
- **使用位置**: MarketList.vue, Management.vue

#### PURCHASE_CONFIG
抢购相关的配置参数：

- **DEFAULT_MAX_RETRIES**: 默认最大重试次数 (1000)
- **DEFAULT_RETRY_INTERVAL**: 默认重试间隔 (200ms)
- **DEFAULT_SUPER_THREAD_COUNT**: 默认超级抢购线程数 (50)
- **REQUEST_TIMEOUT**: 请求超时时间 (3000ms)
- **TOTAL_TIMEOUT**: 总超时时间 (30000ms)

#### API_CONFIG
API相关的配置参数：

- **BASE_URL**: API基础URL ('http://localhost:5001')
- **TIMEOUT**: API请求超时时间 (10000ms)

## 使用方法

### 1. 导入配置

```javascript
import { DEFAULT_SIGN, DEFAULT_PASSWORD, SYSTEM_CONFIG } from '../config/constants'
```

### 2. 使用配置

```javascript
// 使用默认签名
const sign = DEFAULT_SIGN

// 使用默认密码
const password = DEFAULT_PASSWORD

// 使用抢购配置
const maxRetries = SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_MAX_RETRIES
const interval = SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_RETRY_INTERVAL
```

## 优势

1. **统一管理**: 所有配置集中在一个文件中管理
2. **易于维护**: 修改配置只需要在一个地方进行
3. **避免重复**: 避免在多个文件中重复定义相同的值
4. **类型安全**: 使用常量可以避免拼写错误
5. **便于扩展**: 新增配置项只需要在constants.js中添加

## 注意事项

1. 修改配置后需要重新启动开发服务器
2. 生产环境部署时需要确保配置正确
3. 敏感信息（如密码、签名）应该通过环境变量管理
4. 配置变更需要同步更新相关文档

## 扩展配置

如需添加新的配置项，请在`constants.js`中添加，并更新此文档。
