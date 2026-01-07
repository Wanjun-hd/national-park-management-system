import request from '@/utils/request'

/**
 * 生物多样性监测 API
 * 包括:物种管理、栖息地管理、监测记录
 */

// ==================== 物种管理 ====================

/**
 * 获取物种列表
 */
export function getSpeciesList(params) {
  return request({
    url: '/biodiversity/species/',
    method: 'get',
    params
  })
}

/**
 * 获取物种详情
 */
export function getSpeciesDetail(id) {
  return request({
    url: `/biodiversity/species/${id}/`,
    method: 'get'
  })
}

/**
 * 创建物种
 */
export function createSpecies(data) {
  return request({
    url: '/biodiversity/species/',
    method: 'post',
    data
  })
}

/**
 * 更新物种
 */
export function updateSpecies(id, data) {
  return request({
    url: `/biodiversity/species/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除物种
 */
export function deleteSpecies(id) {
  return request({
    url: `/biodiversity/species/${id}/`,
    method: 'delete'
  })
}

// ==================== 栖息地管理 ====================

/**
 * 获取栖息地列表
 */
export function getHabitatList(params) {
  return request({
    url: '/biodiversity/habitats/',
    method: 'get',
    params
  })
}

/**
 * 获取栖息地详情
 */
export function getHabitatDetail(id) {
  return request({
    url: `/biodiversity/habitats/${id}/`,
    method: 'get'
  })
}

/**
 * 创建栖息地
 */
export function createHabitat(data) {
  return request({
    url: '/biodiversity/habitats/',
    method: 'post',
    data
  })
}

/**
 * 更新栖息地
 */
export function updateHabitat(id, data) {
  return request({
    url: `/biodiversity/habitats/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除栖息地
 */
export function deleteHabitat(id) {
  return request({
    url: `/biodiversity/habitats/${id}/`,
    method: 'delete'
  })
}

// ==================== 监测记录 ====================

/**
 * 获取监测记录列表
 */
export function getMonitoringRecords(params) {
  return request({
    url: '/biodiversity/monitoring-records/',
    method: 'get',
    params
  })
}

/**
 * 获取监测记录详情
 */
export function getMonitoringRecordDetail(id) {
  return request({
    url: `/biodiversity/monitoring-records/${id}/`,
    method: 'get'
  })
}

/**
 * 创建监测记录
 */
export function createMonitoringRecord(data) {
  return request({
    url: '/biodiversity/monitoring-records/',
    method: 'post',
    data
  })
}

/**
 * 更新监测记录
 */
export function updateMonitoringRecord(id, data) {
  return request({
    url: `/biodiversity/monitoring-records/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 更新监测记录状态(部分更新)
 */
export function patchMonitoringRecord(id, data) {
  return request({
    url: `/biodiversity/monitoring-records/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除监测记录
 */
export function deleteMonitoringRecord(id) {
  return request({
    url: `/biodiversity/monitoring-records/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取监测设备列表
 */
export function getMonitoringDevices(params) {
  return request({
    url: '/biodiversity/devices/',
    method: 'get',
    params
  })
}

/**
 * 获取生物多样性统计数据
 */
export function getBiodiversityStats() {
  return request({
    url: '/biodiversity/stats/',
    method: 'get'
  })
}
