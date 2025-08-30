// 系统常量配置
export const SYSTEM_CONFIG = {
  // 默认签名值
  DEFAULT_SIGN: 'mnNrgWz6PAl0Xq4N',
  
  // 默认抢购密码
  DEFAULT_PASSWORD: '200412',
  
  // 抢购配置
  PURCHASE_CONFIG: {
    // 默认重试次数
    DEFAULT_MAX_RETRIES: 1000,
    // 默认重试间隔(毫秒)
    DEFAULT_RETRY_INTERVAL: 200,
    // 默认超级抢购线程数
    DEFAULT_SUPER_THREAD_COUNT: 50,
    // 请求超时时间(毫秒)
    REQUEST_TIMEOUT: 3000,
    // 总超时时间(毫秒)
    TOTAL_TIMEOUT: 30000
  },
  
  // API配置
  API_CONFIG: {
    // 基础URL
    BASE_URL: 'http://localhost:5001',
    // 请求超时
    TIMEOUT: 10000
  }
}

// 导出默认值，方便直接使用
export const DEFAULT_SIGN = SYSTEM_CONFIG.DEFAULT_SIGN
export const DEFAULT_PASSWORD = SYSTEM_CONFIG.DEFAULT_PASSWORD
