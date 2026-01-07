import request from '@/utils/request'

/**
 * 游客智能管理 API
 * 包括:游客管理、预约管理、流量控制、轨迹追踪
 */

// ==================== 游客管理 ====================

/**
 * 获取游客列表
 */
export function getVisitors(params) {
  return request({
    url: '/visitor/visitors/',
    method: 'get',
    params
  })
}

/**
 * 获取游客详情
 */
export function getVisitorDetail(id) {
  return request({
    url: `/visitor/visitors/${id}/`,
    method: 'get'
  })
}

/**
 * 创建游客
 */
export function createVisitor(data) {
  return request({
    url: '/visitor/visitors/',
    method: 'post',
    data
  })
}

/**
 * 更新游客信息
 */
export function updateVisitor(id, data) {
  return request({
    url: `/visitor/visitors/${id}/`,
    method: 'put',
    data
  })
}

// ==================== 预约管理 ====================

/**
 * 获取预约列表
 */
export function getReservations(params) {
  return request({
    url: '/visitor/reservations/',
    method: 'get',
    params
  })
}

/**
 * 获取预约详情
 */
export function getReservationDetail(id) {
  return request({
    url: `/visitor/reservations/${id}/`,
    method: 'get'
  })
}

/**
 * 创建预约
 */
export function createReservation(data) {
  return request({
    url: '/visitor/reservations/',
    method: 'post',
    data
  })
}

/**
 * 更新预约
 */
export function updateReservation(id, data) {
  return request({
    url: `/visitor/reservations/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 取消预约
 */
export function cancelReservation(id) {
  return request({
    url: `/visitor/reservations/${id}/cancel/`,
    method: 'post'
  })
}

// ==================== 流量控制 ====================

/**
 * 获取流量控制列表
 */
export function getTrafficControls(params) {
  return request({
    url: '/visitor/traffic-controls/',
    method: 'get',
    params
  })
}

/**
 * 获取流量控制详情
 */
export function getTrafficControlDetail(areaId) {
  return request({
    url: `/visitor/traffic-controls/${areaId}/`,
    method: 'get'
  })
}

/**
 * 更新流量控制
 */
export function updateTrafficControl(areaId, data) {
  return request({
    url: `/visitor/traffic-controls/${areaId}/`,
    method: 'put',
    data
  })
}

/**
 * 获取流量统计
 */
export function getTrafficStats() {
  return request({
    url: '/visitor/traffic-controls/stats/',
    method: 'get'
  })
}

// ==================== 游客轨迹 ====================

/**
 * 获取游客轨迹
 */
export function getVisitorTrajectories(params) {
  return request({
    url: '/visitor/trajectories/',
    method: 'get',
    params
  })
}

/**
 * 获取指定游客的轨迹
 */
export function getVisitorTrajectoryByVisitorId(visitorId, params) {
  return request({
    url: `/visitor/trajectories/by-visitor/${visitorId}/`,
    method: 'get',
    params
  })
}

/**
 * 创建轨迹记录
 */
export function createTrajectory(data) {
  return request({
    url: '/visitor/trajectories/',
    method: 'post',
    data
  })
}

/**
 * 获取游客统计数据
 */
export function getVisitorStats() {
  return request({
    url: '/visitor/stats/',
    method: 'get'
  })
}
