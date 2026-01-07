import request from '@/utils/request'

/**
 * 科研数据支撑 API
 * 包括:科研项目、数据采集、科研成果
 */

// ==================== 科研项目 ====================

/**
 * 获取科研项目列表
 */
export function getResearchProjects(params) {
  return request({
    url: '/research/projects/',
    method: 'get',
    params
  })
}

/**
 * 获取科研项目详情
 */
export function getResearchProjectDetail(id) {
  return request({
    url: `/research/projects/${id}/`,
    method: 'get'
  })
}

/**
 * 创建科研项目
 */
export function createResearchProject(data) {
  return request({
    url: '/research/projects/',
    method: 'post',
    data
  })
}

/**
 * 更新科研项目
 */
export function updateResearchProject(id, data) {
  return request({
    url: `/research/projects/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除科研项目
 */
export function deleteResearchProject(id) {
  return request({
    url: `/research/projects/${id}/`,
    method: 'delete'
  })
}

/**
 * 结题科研项目
 */
export function completeResearchProject(id, data) {
  return request({
    url: `/research/projects/${id}/complete/`,
    method: 'post',
    data
  })
}

// ==================== 数据采集 ====================

/**
 * 获取数据采集记录列表
 */
export function getDataCollections(params) {
  return request({
    url: '/research/data-collections/',
    method: 'get',
    params
  })
}

/**
 * 获取数据采集记录详情
 */
export function getDataCollectionDetail(id) {
  return request({
    url: `/research/data-collections/${id}/`,
    method: 'get'
  })
}

/**
 * 创建数据采集记录
 */
export function createDataCollection(data) {
  return request({
    url: '/research/data-collections/',
    method: 'post',
    data
  })
}

/**
 * 更新数据采集记录
 */
export function updateDataCollection(id, data) {
  return request({
    url: `/research/data-collections/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除数据采集记录
 */
export function deleteDataCollection(id) {
  return request({
    url: `/research/data-collections/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取项目的数据采集记录
 */
export function getProjectDataCollections(projectId, params) {
  return request({
    url: `/research/projects/${projectId}/data-collections/`,
    method: 'get',
    params
  })
}

// ==================== 科研成果 ====================

/**
 * 获取科研成果列表
 */
export function getResearchAchievements(params) {
  return request({
    url: '/research/achievements/',
    method: 'get',
    params
  })
}

/**
 * 获取科研成果详情
 */
export function getResearchAchievementDetail(id) {
  return request({
    url: `/research/achievements/${id}/`,
    method: 'get'
  })
}

/**
 * 创建科研成果
 */
export function createResearchAchievement(data) {
  return request({
    url: '/research/achievements/',
    method: 'post',
    data
  })
}

/**
 * 更新科研成果
 */
export function updateResearchAchievement(id, data) {
  return request({
    url: `/research/achievements/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除科研成果
 */
export function deleteResearchAchievement(id) {
  return request({
    url: `/research/achievements/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取项目的科研成果
 */
export function getProjectAchievements(projectId, params) {
  return request({
    url: `/research/projects/${projectId}/achievements/`,
    method: 'get',
    params
  })
}

/**
 * 获取科研统计数据
 */
export function getResearchStats() {
  return request({
    url: '/research/stats/',
    method: 'get'
  })
}
