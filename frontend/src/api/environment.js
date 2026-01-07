import request from '@/utils/request'

/**
 * 生态环境监测 API
 * 包括:环境数据、监测指标、监测设备
 */

// ==================== 环境数据 ====================

/**
 * 获取环境监测数据列表
 */
export function getEnvironmentalData(params) {
  return request({
    url: '/environment/data/',
    method: 'get',
    params
  })
}

/**
 * 获取环境数据详情
 */
export function getEnvironmentalDataDetail(id) {
  return request({
    url: `/environment/data/${id}/`,
    method: 'get'
  })
}

/**
 * 创建环境数据
 */
export function createEnvironmentalData(data) {
  return request({
    url: '/environment/data/',
    method: 'post',
    data
  })
}

/**
 * 获取环境数据统计
 */
export function getEnvironmentalDataStats(params) {
  return request({
    url: '/environment/data/stats/',
    method: 'get',
    params
  })
}

// ==================== 监测指标 ====================

/**
 * 获取监测指标列表
 */
export function getIndicators(params) {
  return request({
    url: '/environment/indicators/',
    method: 'get',
    params
  })
}

/**
 * 获取指标详情
 */
export function getIndicatorDetail(id) {
  return request({
    url: `/environment/indicators/${id}/`,
    method: 'get'
  })
}

/**
 * 创建监测指标
 */
export function createIndicator(data) {
  return request({
    url: '/environment/indicators/',
    method: 'post',
    data
  })
}

/**
 * 更新监测指标
 */
export function updateIndicator(id, data) {
  return request({
    url: `/environment/indicators/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除监测指标
 */
export function deleteIndicator(id) {
  return request({
    url: `/environment/indicators/${id}/`,
    method: 'delete'
  })
}

// ==================== 监测设备 ====================

/**
 * 获取监测设备列表
 */
export function getDevices(params) {
  return request({
    url: '/environment/devices/',
    method: 'get',
    params
  })
}

/**
 * 获取设备详情
 */
export function getDeviceDetail(id) {
  return request({
    url: `/environment/devices/${id}/`,
    method: 'get'
  })
}

/**
 * 创建监测设备
 */
export function createDevice(data) {
  return request({
    url: '/environment/devices/',
    method: 'post',
    data
  })
}

/**
 * 更新监测设备
 */
export function updateDevice(id, data) {
  return request({
    url: `/environment/devices/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除监测设备
 */
export function deleteDevice(id) {
  return request({
    url: `/environment/devices/${id}/`,
    method: 'delete'
  })
}

/**
 * 设备状态更新
 */
export function updateDeviceStatus(id, status) {
  return request({
    url: `/environment/devices/${id}/update_status/`,
    method: 'post',
    data: { operation_status: status }
  })
}
