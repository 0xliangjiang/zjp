import axios from 'axios'
import { Message } from 'element-ui'

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:5001',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 从localStorage获取token（抢购平台的token）
    const token = localStorage.getItem('token')
    if (token) {
      // 所有接口都使用Token头（抢购平台的格式）
      config.headers.Token = token
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      const { status } = error.response
      
      // 处理401未授权错误
      if (status === 401) {
        // 只显示提示消息，不清除token和用户信息，不自动登出
        Message.warning({
          message: 'Token已失效，部分功能可能无法正常使用，请联系管理员或手动退出重新登录',
          duration: 5000,
          showClose: true
        })
        
        return Promise.reject(error)
      }
      
      // 处理其他错误
      const errorMessage = error.response.data?.error || '请求失败'
      Message.error(errorMessage)
    } else {
      Message.error('网络错误，请检查网络连接')
    }
    
    return Promise.reject(error)
  }
)

export default request
