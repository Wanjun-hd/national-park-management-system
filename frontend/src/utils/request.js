import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const API_BASE_URL = `http://${window.location.hostname}:8000/api`
const service = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // Token过期或无效
          ElMessage.error('登录已过期,请重新登录')
          localStorage.removeItem('token')
          localStorage.removeItem('refresh_token')
          router.push('/login')
          break
        case 403:
          ElMessage.error('没有权限访问该资源')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误,请稍后重试')
          break
        default:
          ElMessage.error(data.detail || data.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误,请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }

    return Promise.reject(error)
  }
)

export default service
