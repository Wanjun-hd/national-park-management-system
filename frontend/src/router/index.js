import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'MainLayout',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: {
          title: '仪表盘',
          role: [
            '生态监测员',
            '数据分析师',
            '游客',
            '执法人员',
            '科研人员',
            '技术人员',
            '公园管理人员',
            '系统管理员'
          ]
        }
      },
      // 生物多样性监测
      {
        path: '/biodiversity/species',
        name: 'SpeciesManagement',
        component: () => import('@/views/biodiversity/SpeciesManagement.vue'),
        meta: { title: '物种管理', role: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/biodiversity/habitat',
        name: 'HabitatManagement',
        component: () => import('@/views/biodiversity/HabitatManagement.vue'),
        meta: { title: '栖息地管理', role: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/biodiversity/monitoring',
        name: 'MonitoringRecord',
        component: () => import('@/views/biodiversity/MonitoringRecord.vue'),
        meta: { title: '监测记录', role: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] }
      },
      // 环境监测
      {
        path: '/environment/devices',
        name: 'DeviceManagement',
        component: () => import('@/views/environment/DeviceManagement.vue'),
        meta: { title: '设备管理', role: ['技术人员', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/environment/data',
        name: 'EnvironmentalData',
        component: () => import('@/views/environment/EnvironmentalData.vue'),
        meta: { title: '环境数据', role: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/environment/indicators',
        name: 'IndicatorManagement',
        component: () => import('@/views/environment/IndicatorManagement.vue'),
        meta: { title: '指标管理', role: ['数据分析师', '系统管理员'] }
      },
      // 游客管理
      {
        path: '/visitor/list',
        name: 'VisitorList',
        component: () => import('@/views/visitor/VisitorList.vue'),
        meta: { title: '游客列表', role: ['公园管理人员', '系统管理员'] }
      },
      {
        path: '/visitor/reservation',
        name: 'ReservationManagement',
        component: () => import('@/views/visitor/ReservationManagement.vue'),
        meta: { title: '预约管理', role: ['游客', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/visitor/traffic',
        name: 'TrafficControl',
        component: () => import('@/views/visitor/TrafficControl.vue'),
        meta: { title: '流量控制', role: ['公园管理人员', '系统管理员'] }
      },
      {
        path: '/visitor/trajectory',
        name: 'VisitorTrajectory',
        component: () => import('@/views/visitor/VisitorTrajectory.vue'),
        meta: { title: '游客轨迹', role: ['执法人员', '公园管理人员', '系统管理员'] }
      },
      // 执法监管
      {
        path: '/enforcement/illegal',
        name: 'IllegalBehavior',
        component: () => import('@/views/enforcement/IllegalBehavior.vue'),
        meta: { title: '违法行为', role: ['执法人员', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/enforcement/dispatch',
        name: 'EnforcementDispatch',
        component: () => import('@/views/enforcement/EnforcementDispatch.vue'),
        meta: { title: '执法调度', role: ['执法人员', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/enforcement/surveillance',
        name: 'SurveillancePoint',
        component: () => import('@/views/enforcement/SurveillancePoint.vue'),
        meta: { title: '监控点管理', role: ['技术人员', '执法人员', '公园管理人员', '系统管理员'] }
      },
      // 科研支撑
      {
        path: '/research/projects',
        name: 'ResearchProject',
        component: () => import('@/views/research/ResearchProject.vue'),
        meta: { title: '科研项目', role: ['科研人员', '公园管理人员', '系统管理员'] }
      },
      {
        path: '/research/data-collection',
        name: 'DataCollection',
        component: () => import('@/views/research/DataCollection.vue'),
        meta: { title: '数据采集', role: ['科研人员', '系统管理员'] }
      },
      {
        path: '/research/achievements',
        name: 'ResearchAchievement',
        component: () => import('@/views/research/ResearchAchievement.vue'),
        meta: { title: '科研成果', role: ['科研人员', '公园管理人员', '系统管理员'] }
      },
      // 系统管理
      {
        path: '/system/users',
        name: 'UserManagement',
        component: () => import('@/views/system/UserManagement.vue'),
        meta: { title: '用户管理', role: ['系统管理员'] }
      },
      {
        path: '/system/areas',
        name: 'AreaManagement',
        component: () => import('@/views/system/AreaManagement.vue'),
        meta: { title: '区域管理', role: ['系统管理员'] }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    if (to.meta.role && to.meta.role.length > 0) {
      if (!to.meta.role.includes(authStore.user?.role_type)) {
        next('/dashboard')
      } else {
        next()
      }
    } else {
      next()
    }
  }
})

export default router
