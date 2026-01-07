import request from '@/utils/request'

/**
 * 执法监管 API
 * 包括:非法行为记录、执法调度、监控点管理、执法人员
 */

// ==================== 非法行为记录 ====================

/**
 * 获取非法行为列表
 */
export function getIllegalBehaviors(params) {
  return request({
    url: '/enforcement/illegal-behaviors/',
    method: 'get',
    params
  })
}

/**
 * 获取非法行为详情
 */
export function getIllegalBehaviorDetail(id) {
  return request({
    url: `/enforcement/illegal-behaviors/${id}/`,
    method: 'get'
  })
}

/**
 * 创建非法行为记录
 */
export function createIllegalBehavior(data) {
  return request({
    url: '/enforcement/illegal-behaviors/',
    method: 'post',
    data
  })
}

/**
 * 更新非法行为记录
 */
export function updateIllegalBehavior(id, data) {
  return request({
    url: `/enforcement/illegal-behaviors/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 处理非法行为
 */
export function handleIllegalBehavior(id, data) {
  return request({
    url: `/enforcement/illegal-behaviors/${id}/handle/`,
    method: 'post',
    data
  })
}

// ==================== 执法调度 ====================

/**
 * 获取执法调度列表
 */
export function getEnforcementDispatches(params) {
  return request({
    url: '/enforcement/dispatches/',
    method: 'get',
    params
  })
}

/**
 * 获取执法调度详情
 */
export function getEnforcementDispatchDetail(id) {
  return request({
    url: `/enforcement/dispatches/${id}/`,
    method: 'get'
  })
}

/**
 * 创建执法调度
 */
export function createEnforcementDispatch(data) {
  return request({
    url: '/enforcement/dispatches/',
    method: 'post',
    data
  })
}

/**
 * 更新执法调度
 */
export function updateEnforcementDispatch(id, data) {
  return request({
    url: `/enforcement/dispatches/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 响应调度
 */
export function respondDispatch(id) {
  return request({
    url: `/enforcement/dispatches/${id}/respond/`,
    method: 'post'
  })
}

/**
 * 完成调度
 */
export function completeDispatch(id, data) {
  return request({
    url: `/enforcement/dispatches/${id}/complete/`,
    method: 'post',
    data
  })
}

// ==================== 执法人员 ====================

/**
 * 获取执法人员列表
 */
export function getLawEnforcers(params) {
  return request({
    url: '/enforcement/enforcers/',
    method: 'get',
    params
  })
}

/**
 * 获取执法人员详情
 */
export function getLawEnforcerDetail(id) {
  return request({
    url: `/enforcement/enforcers/${id}/`,
    method: 'get'
  })
}

/**
 * 创建执法人员
 */
export function createLawEnforcer(data) {
  return request({
    url: '/enforcement/enforcers/',
    method: 'post',
    data
  })
}

/**
 * 更新执法人员
 */
export function updateLawEnforcer(id, data) {
  return request({
    url: `/enforcement/enforcers/${id}/`,
    method: 'put',
    data
  })
}

// ==================== 监控点管理 ====================

/**
 * 获取监控点列表
 */
export function getSurveillancePoints(params) {
  return request({
    url: '/enforcement/surveillance-points/',
    method: 'get',
    params
  })
}

/**
 * 获取监控点详情
 */
export function getSurveillancePointDetail(id) {
  return request({
    url: `/enforcement/surveillance-points/${id}/`,
    method: 'get'
  })
}

/**
 * 创建监控点
 */
export function createSurveillancePoint(data) {
  return request({
    url: '/enforcement/surveillance-points/',
    method: 'post',
    data
  })
}

/**
 * 更新监控点
 */
export function updateSurveillancePoint(id, data) {
  return request({
    url: `/enforcement/surveillance-points/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除监控点
 */
export function deleteSurveillancePoint(id) {
  return request({
    url: `/enforcement/surveillance-points/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取执法统计数据
 */
export function getEnforcementStats() {
  return request({
    url: '/enforcement/stats/',
    method: 'get'
  })
}
