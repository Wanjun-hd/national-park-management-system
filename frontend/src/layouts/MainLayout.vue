<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>国家公园管理系统</h1>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in visibleMenu"
          :key="item.to"
          :to="item.to"
          class="nav-item"
        >
          {{ item.label }}
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-name">{{ authStore.user?.username || '未登录' }}</div>
          <div class="user-role">{{ authStore.user?.role_type || '' }}</div>
        </div>
        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </div>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const menuItems = [
  { label: '数据总览', to: '/dashboard', roles: ['生态监测员', '数据分析师', '游客', '执法人员', '科研人员', '技术人员', '公园管理人员', '系统管理员'] },
  { label: '物种管理', to: '/biodiversity/species', roles: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] },
  { label: '栖息地管理', to: '/biodiversity/habitat', roles: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] },
  { label: '监测记录', to: '/biodiversity/monitoring', roles: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] },
  { label: '监测设备', to: '/environment/devices', roles: ['技术人员', '公园管理人员', '系统管理员'] },
  { label: '环境指标', to: '/environment/indicators', roles: ['数据分析师', '系统管理员'] },
  { label: '环境数据', to: '/environment/data', roles: ['生态监测员', '数据分析师', '公园管理人员', '系统管理员'] },
  { label: '游客管理', to: '/visitor/list', roles: ['公园管理人员', '系统管理员'] },
  { label: '预约管理', to: '/visitor/reservation', roles: ['游客', '公园管理人员', '系统管理员'] },
  { label: '流量控制', to: '/visitor/traffic', roles: ['公园管理人员', '系统管理员'] },
  { label: '游客轨迹', to: '/visitor/trajectory', roles: ['执法人员', '公园管理人员', '系统管理员'] },
  { label: '违法行为', to: '/enforcement/illegal', roles: ['执法人员', '公园管理人员', '系统管理员'] },
  { label: '执法调度', to: '/enforcement/dispatch', roles: ['执法人员', '公园管理人员', '系统管理员'] },
  { label: '监控点管理', to: '/enforcement/surveillance', roles: ['技术人员', '执法人员', '公园管理人员', '系统管理员'] },
  { label: '科研项目', to: '/research/projects', roles: ['科研人员', '公园管理人员', '系统管理员'] },
  { label: '数据采集', to: '/research/data-collection', roles: ['科研人员', '系统管理员'] },
  { label: '科研成果', to: '/research/achievements', roles: ['科研人员', '公园管理人员', '系统管理员'] },
  { label: '用户管理', to: '/system/users', roles: ['系统管理员'] },
  { label: '区域管理', to: '/system/areas', roles: ['系统管理员'] }
]

const visibleMenu = computed(() => {
  const role = authStore.user?.role_type
  if (!role) return menuItems
  return menuItems.filter(item => item.roles.includes(role))
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  padding: 24px;
  gap: 24px;
  background: transparent;
}

.sidebar {
  width: 248px;
  display: flex;
  flex-direction: column;
  background: var(--surface-1);
  border-radius: var(--radius-2);
  border: 1px solid var(--border-1);
  box-shadow: var(--shadow-2);
}

.sidebar-header {
  padding: 22px 20px 18px;
  border-bottom: 1px solid var(--border-1);
}

.sidebar-header h1 {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 600;
  color: var(--ink-1);
  letter-spacing: -0.01em;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 14px 12px 18px;
}

.nav-item {
  display: block;
  padding: 10px 14px;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
  color: var(--muted-1);
  text-decoration: none;
  border-radius: 10px;
  border: 1px solid transparent;
  transition: all 0.16s ease;
}

.nav-item:hover {
  background: var(--surface-2);
  color: var(--ink-1);
  border-color: rgba(15, 23, 42, 0.06);
}

.nav-item.router-link-active {
  background: #f0f1f2;
  color: var(--ink-1);
  border-color: rgba(15, 23, 42, 0.08);
  box-shadow: none;
}

.sidebar-footer {
  padding: 14px 16px 18px;
  border-top: 1px solid var(--border-1);
}

.user-info {
  margin-bottom: 10px;
  padding: 10px 12px;
  background: var(--surface-2);
  border-radius: 12px;
  border: 1px solid rgba(15, 23, 42, 0.04);
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--ink-1);
  margin-bottom: 2px;
}

.user-role {
  font-size: 12px;
  color: var(--muted-1);
}

.logout-btn {
  width: 100%;
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink-1);
  background: var(--surface-1);
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.16s ease;
}

.logout-btn:hover {
  border-color: rgba(15, 23, 42, 0.2);
  box-shadow: var(--shadow-2);
}

.main-content {
  flex: 1;
  overflow-y: auto;
  background: var(--surface-1);
  border-radius: var(--radius-2);
  border: 1px solid var(--border-1);
  box-shadow: var(--shadow-1);
  padding: 26px;
}

@media (max-width: 960px) {
  .layout {
    flex-direction: column;
    padding: 16px;
  }

  .sidebar {
    width: 100%;
  }

  .sidebar-nav {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 8px;
  }

  .nav-item {
    margin-bottom: 0;
  }

  .sidebar-footer {
    display: flex;
    gap: 12px;
    align-items: center;
    justify-content: space-between;
  }

  .user-info {
    margin-bottom: 0;
    flex: 1;
  }

  .logout-btn {
    width: auto;
    white-space: nowrap;
  }
}

@media (max-width: 640px) {
  .sidebar-header h1 {
    font-size: 16px;
  }

  .main-content {
    padding: 18px;
  }
}
</style>
