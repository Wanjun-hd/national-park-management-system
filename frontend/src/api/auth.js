import request from '@/utils/request'

/**
 * 用户登录
 */
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}

/**
 * 用户登出
 */
export function logout() {
  return request({
    url: '/auth/logout/',
    method: 'post'
  })
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser() {
  return request({
    url: '/auth/current-user/',
    method: 'get'
  })
}

/**
 * 创建测试用户
 */
export function createTestUser() {
  return request({
    url: '/auth/create-test-user/',
    method: 'post'
  })
}

/**
 * 测试API连接
 */
export function testApi() {
  return request({
    url: '/test/',
    method: 'get'
  })
}
