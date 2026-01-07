import request from '@/utils/request'

/**
 * 系统管理 API
 * 包括:用户管理、区域管理
 */

// ==================== 用户管理 ====================

/**
 * 获取用户列表
 */
export function getUsers(params) {
  return request({
    url: '/system/users/',
    method: 'get',
    params
  })
}

/**
 * 创建用户
 */
export function createUser(data) {
  return request({
    url: '/system/users/',
    method: 'post',
    data
  })
}

/**
 * 更新用户
 */
export function updateUser(id, data) {
  return request({
    url: `/system/users/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除用户
 */
export function deleteUser(id) {
  return request({
    url: `/system/users/${id}/`,
    method: 'delete'
  })
}

// ==================== 区域管理 ====================

/**
 * 获取区域列表
 */
export function getAreas(params) {
  return request({
    url: '/system/areas/',
    method: 'get',
    params
  })
}

/**
 * 创建区域
 */
export function createArea(data) {
  return request({
    url: '/system/areas/',
    method: 'post',
    data
  })
}

/**
 * 更新区域
 */
export function updateArea(id, data) {
  return request({
    url: `/system/areas/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除区域
 */
export function deleteArea(id) {
  return request({
    url: `/system/areas/${id}/`,
    method: 'delete'
  })
}
