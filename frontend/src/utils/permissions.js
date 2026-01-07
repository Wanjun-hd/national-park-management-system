const rolePermissions = {
  'biodiversity.species.create': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.species.edit': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.species.delete': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.habitat.create': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.habitat.edit': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.habitat.delete': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.monitoring.create': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.monitoring.edit': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.monitoring.delete': ['生态监测员', '公园管理人员', '系统管理员'],
  'biodiversity.monitoring.review': ['数据分析师', '系统管理员'],

  'environment.device.create': ['技术人员', '公园管理人员', '系统管理员'],
  'environment.device.edit': ['技术人员', '公园管理人员', '系统管理员'],
  'environment.device.delete': ['技术人员', '公园管理人员', '系统管理员'],
  'environment.device.status': ['技术人员', '公园管理人员', '系统管理员'],
  'environment.indicator.create': ['数据分析师', '系统管理员'],
  'environment.indicator.edit': ['数据分析师', '系统管理员'],
  'environment.indicator.delete': ['数据分析师', '系统管理员'],
  'environment.data.create': ['技术人员', '系统管理员'],

  'visitor.list.create': ['公园管理人员', '系统管理员'],
  'visitor.list.edit': ['公园管理人员', '系统管理员'],
  'visitor.reservation.create': ['游客', '公园管理人员', '系统管理员'],
  'visitor.reservation.edit': ['公园管理人员', '系统管理员'],
  'visitor.reservation.cancel': ['公园管理人员', '系统管理员'],
  'visitor.reservation.complete': ['公园管理人员', '系统管理员'],
  'visitor.traffic.edit': ['公园管理人员', '系统管理员'],
  'visitor.trajectory.create': ['公园管理人员', '系统管理员'],

  'enforcement.illegal.create': ['执法人员', '公园管理人员', '系统管理员'],
  'enforcement.illegal.edit': ['执法人员', '公园管理人员', '系统管理员'],
  'enforcement.illegal.handle': ['执法人员', '公园管理人员', '系统管理员'],
  'enforcement.dispatch.create': ['公园管理人员', '系统管理员'],
  'enforcement.dispatch.edit': ['公园管理人员', '系统管理员'],
  'enforcement.dispatch.complete': ['执法人员', '公园管理人员', '系统管理员'],
  'enforcement.surveillance.create': ['技术人员', '公园管理人员', '系统管理员'],
  'enforcement.surveillance.edit': ['技术人员', '公园管理人员', '系统管理员'],
  'enforcement.surveillance.delete': ['技术人员', '公园管理人员', '系统管理员'],

  'research.project.create': ['科研人员', '公园管理人员', '系统管理员'],
  'research.project.edit': ['科研人员', '公园管理人员', '系统管理员'],
  'research.project.delete': ['公园管理人员', '系统管理员'],
  'research.data.create': ['科研人员', '系统管理员'],
  'research.data.edit': ['科研人员', '系统管理员'],
  'research.data.delete': ['科研人员', '系统管理员'],
  'research.achievement.create': ['科研人员', '系统管理员'],
  'research.achievement.edit': ['科研人员', '系统管理员'],
  'research.achievement.delete': ['科研人员', '系统管理员'],

  'system.user.create': ['系统管理员'],
  'system.user.edit': ['系统管理员'],
  'system.user.delete': ['系统管理员'],
  'system.area.create': ['系统管理员'],
  'system.area.edit': ['系统管理员'],
  'system.area.delete': ['系统管理员']
}

export function canRole(role, key) {
  if (!role || !key) return false
  const allowed = rolePermissions[key]
  return Array.isArray(allowed) ? allowed.includes(role) : false
}

export { rolePermissions }
