import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, logout as apiLogout, getCurrentUser } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials) {
    try {
      const response = await apiLogin(credentials)
      const data = response.data

      // 保存token和用户信息
      token.value = data.access
      user.value = data.user

      localStorage.setItem('token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))

      return true
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  async function logout() {
    try {
      await apiLogout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = ''
      user.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  }

  async function fetchUserInfo() {
    try {
      const response = await getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      // 如果获取用户信息失败,清除token
      logout()
    }
  }

  async function checkAuth() {
    if (token.value && user.value) {
      // Token和用户信息都存在,认为已登录
      return true
    }
    return false
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    checkAuth,
    fetchUserInfo
  }
})
