<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>数据总览</h1>
      <el-button @click="fetchDashboardStats" :loading="loading">刷新</el-button>
    </div>

    <div class="stats-section">
      <div class="stat-item">
        <div class="stat-label">物种总数</div>
        <div class="stat-value">{{ stats.biodiversity?.total_species || 0 }}</div>
        <div class="stat-meta">受保护物种 {{ stats.biodiversity?.protected_species || 0 }}</div>
      </div>

      <div class="stat-item">
        <div class="stat-label">监测设备</div>
        <div class="stat-value">{{ stats.biodiversity?.active_devices || 0 }}</div>
        <div class="stat-meta">正常运行</div>
      </div>

      <div class="stat-item">
        <div class="stat-label">游客数量</div>
        <div class="stat-value">{{ stats.visitor?.total_visitors || 0 }}</div>
        <div class="stat-meta">当前在园 {{ stats.visitor?.current_in_park || 0 }}</div>
      </div>

      <div class="stat-item">
        <div class="stat-label">科研项目</div>
        <div class="stat-value">{{ stats.research?.total_projects || 0 }}</div>
        <div class="stat-meta">在研 {{ stats.research?.ongoing_projects || 0 }}</div>
      </div>
    </div>

    <div class="charts-section">
      <div class="chart-card wide">
        <div class="chart-header">
          <h3>核心指标对比</h3>
          <span class="chart-note">按当前最大值归一化</span>
        </div>
        <div class="bar-chart">
          <div class="bar-row" v-for="item in barMetrics" :key="item.key">
            <div class="bar-label">{{ item.label }}</div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: item.percent + '%', background: item.color }"></div>
            </div>
            <div class="bar-value">{{ item.value }}</div>
          </div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-header">
          <h3>执法处理占比</h3>
          <span class="chart-note">未处理占比</span>
        </div>
        <div class="donut-wrap">
          <div class="donut" :style="enforcementDonutStyle">
            <div class="donut-center">
              <div class="donut-value">{{ enforcementRatio }}%</div>
              <div class="donut-label">未处理</div>
            </div>
          </div>
          <div class="donut-legend">
            <div class="legend-row">
              <span class="legend-dot danger"></span>
              <span>未处理</span>
              <strong>{{ stats.enforcement?.unhandled || 0 }}</strong>
            </div>
            <div class="legend-row">
              <span class="legend-dot ok"></span>
              <span>已处理</span>
              <strong>{{ handledCount }}</strong>
            </div>
          </div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-header">
          <h3>科研项目进度</h3>
          <span class="chart-note">在研占比</span>
        </div>
        <div class="donut-wrap">
          <div class="donut" :style="researchDonutStyle">
            <div class="donut-center">
              <div class="donut-value">{{ researchRatio }}%</div>
              <div class="donut-label">在研</div>
            </div>
          </div>
          <div class="donut-legend">
            <div class="legend-row">
              <span class="legend-dot info"></span>
              <span>在研</span>
              <strong>{{ stats.research?.ongoing_projects || 0 }}</strong>
            </div>
            <div class="legend-row">
              <span class="legend-dot muted"></span>
              <span>已结题</span>
              <strong>{{ completedResearch }}</strong>
            </div>
          </div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-header">
          <h3>游客在园占比</h3>
          <span class="chart-note">当前在园</span>
        </div>
        <div class="donut-wrap">
          <div class="donut" :style="visitorDonutStyle">
            <div class="donut-center">
              <div class="donut-value">{{ visitorRatio }}%</div>
              <div class="donut-label">在园</div>
            </div>
          </div>
          <div class="donut-legend">
            <div class="legend-row">
              <span class="legend-dot ok"></span>
              <span>在园</span>
              <strong>{{ stats.visitor?.current_in_park || 0 }}</strong>
            </div>
            <div class="legend-row">
              <span class="legend-dot muted"></span>
              <span>总游客</span>
              <strong>{{ stats.visitor?.total_visitors || 0 }}</strong>
            </div>
          </div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-header">
          <h3>预约转化概览</h3>
          <span class="chart-note">今日预约占比</span>
        </div>
        <div class="donut-wrap">
          <div class="donut" :style="reservationDonutStyle">
            <div class="donut-center">
              <div class="donut-value">{{ reservationRatio }}%</div>
              <div class="donut-label">今日预约</div>
            </div>
          </div>
          <div class="donut-legend">
            <div class="legend-row">
              <span class="legend-dot info"></span>
              <span>今日预约</span>
              <strong>{{ stats.visitor?.reservations_today || 0 }}</strong>
            </div>
            <div class="legend-row">
              <span class="legend-dot muted"></span>
              <span>总游客</span>
              <strong>{{ stats.visitor?.total_visitors || 0 }}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>


    <div class="modules-section">
      <div class="module-item">
        <div class="module-header">
          <h3>生物多样性</h3>
          <span class="status-badge">运行中</span>
        </div>
        <div class="module-data">
          <div class="data-row">
            <span>物种总数</span>
            <span>{{ stats.biodiversity?.total_species || 0 }}</span>
          </div>
          <div class="data-row">
            <span>受保护物种</span>
            <span>{{ stats.biodiversity?.protected_species || 0 }}</span>
          </div>
          <div class="data-row">
            <span>监测记录</span>
            <span>{{ stats.biodiversity?.monitoring_records || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="module-item">
        <div class="module-header">
          <h3>环境监测</h3>
          <span class="status-badge">运行中</span>
        </div>
        <div class="module-data">
          <div class="data-row">
            <span>监测指标</span>
            <span>{{ stats.environment?.total_indicators || 0 }}</span>
          </div>
          <div class="data-row">
            <span>数据点数</span>
            <span>{{ stats.environment?.total_data_points || 0 }}</span>
          </div>
          <div class="data-row">
            <span>监测设备</span>
            <span>{{ stats.environment?.devices || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="module-item">
        <div class="module-header">
          <h3>游客管理</h3>
          <span class="status-badge">运行中</span>
        </div>
        <div class="module-data">
          <div class="data-row">
            <span>游客总数</span>
            <span>{{ stats.visitor?.total_visitors || 0 }}</span>
          </div>
          <div class="data-row">
            <span>当前在园</span>
            <span>{{ stats.visitor?.current_in_park || 0 }}</span>
          </div>
          <div class="data-row">
            <span>今日预约</span>
            <span>{{ stats.visitor?.reservations_today || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="module-item">
        <div class="module-header">
          <h3>执法监管</h3>
          <span class="status-badge" :class="{ warning: stats.enforcement?.unhandled > 0 }">
            {{ stats.enforcement?.unhandled > 0 ? '待处理' : '正常' }}
          </span>
        </div>
        <div class="module-data">
          <div class="data-row">
            <span>违法行为</span>
            <span>{{ stats.enforcement?.total_illegal_behaviors || 0 }}</span>
          </div>
          <div class="data-row">
            <span>未处理</span>
            <span>{{ stats.enforcement?.unhandled || 0 }}</span>
          </div>
          <div class="data-row">
            <span>处理中</span>
            <span>{{ stats.enforcement?.in_progress || 0 }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="system-section">
      <h3>系统状态</h3>
      <div class="system-grid">
        <div class="system-item">
          <div class="system-status"></div>
          <div class="system-info">
            <div class="system-name">前端服务</div>
            <div class="system-desc">Vue 3 + Element Plus</div>
          </div>
        </div>
        <div class="system-item">
          <div class="system-status"></div>
          <div class="system-info">
            <div class="system-name">后端服务</div>
            <div class="system-desc">Django + DRF</div>
          </div>
        </div>
        <div class="system-item">
          <div class="system-status"></div>
          <div class="system-info">
            <div class="system-name">数据库</div>
            <div class="system-desc">MySQL 8.0</div>
          </div>
        </div>
        <div class="system-item">
          <div class="system-status"></div>
          <div class="system-info">
            <div class="system-name">API文档</div>
            <div class="system-desc">Swagger UI</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const stats = ref({
  biodiversity: {},
  environment: {},
  visitor: {},
  enforcement: {},
  research: {}
})
const loading = ref(false)

const barMetrics = computed(() => {
  const items = [
    {
      key: 'species',
      label: '物种总数',
      value: stats.value.biodiversity?.total_species || 0,
      color: 'var(--chart-1)'
    },
    {
      key: 'records',
      label: '监测记录',
      value: stats.value.biodiversity?.monitoring_records || 0,
      color: 'var(--chart-2)'
    },
    {
      key: 'env',
      label: '环境数据',
      value: stats.value.environment?.total_data_points || 0,
      color: 'var(--chart-3)'
    },
    {
      key: 'visitors',
      label: '游客总数',
      value: stats.value.visitor?.total_visitors || 0,
      color: 'var(--chart-4)'
    }
  ]
  const maxValue = Math.max(1, ...items.map(item => item.value))
  return items.map(item => ({
    ...item,
    percent: Math.round((item.value / maxValue) * 100)
  }))
})

const enforcementRatio = computed(() => {
  const total = stats.value.enforcement?.total_illegal_behaviors || 0
  const unhandled = stats.value.enforcement?.unhandled || 0
  if (!total) return 0
  return Math.round((unhandled / total) * 100)
})

const handledCount = computed(() => {
  const total = stats.value.enforcement?.total_illegal_behaviors || 0
  const unhandled = stats.value.enforcement?.unhandled || 0
  return Math.max(0, total - unhandled)
})

const enforcementDonutStyle = computed(() => ({
  background: `conic-gradient(var(--chart-danger) ${enforcementRatio.value}%, var(--chart-muted) 0)`
}))

const researchRatio = computed(() => {
  const total = stats.value.research?.total_projects || 0
  const ongoing = stats.value.research?.ongoing_projects || 0
  if (!total) return 0
  return Math.round((ongoing / total) * 100)
})

const completedResearch = computed(() => {
  const total = stats.value.research?.total_projects || 0
  const ongoing = stats.value.research?.ongoing_projects || 0
  return Math.max(0, total - ongoing)
})

const researchDonutStyle = computed(() => ({
  background: `conic-gradient(var(--chart-info) ${researchRatio.value}%, var(--chart-muted) 0)`
}))

const visitorRatio = computed(() => {
  const total = stats.value.visitor?.total_visitors || 0
  const current = stats.value.visitor?.current_in_park || 0
  if (!total) return 0
  return Math.round((current / total) * 100)
})

const visitorDonutStyle = computed(() => ({
  background: `conic-gradient(#22c55e ${visitorRatio.value}%, var(--chart-muted) 0)`
}))

const reservationRatio = computed(() => {
  const total = stats.value.visitor?.total_visitors || 0
  const today = stats.value.visitor?.reservations_today || 0
  if (!total) return 0
  return Math.round((today / total) * 100)
})

const reservationDonutStyle = computed(() => ({
  background: `conic-gradient(var(--chart-info) ${reservationRatio.value}%, var(--chart-muted) 0)`
}))


const fetchDashboardStats = async () => {
  try {
    loading.value = true
    const response = await request({
      url: '/dashboard/stats/',
      method: 'get'
    })
    stats.value = response.data
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.warning('暂无统计数据')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDashboardStats()
})
</script>

<style scoped>
.dashboard {
  padding: 48px 32px;
  max-width: 1200px;
  margin: 0 auto;
  background: radial-gradient(circle at top, rgba(244, 247, 252, 0.9), #ffffff 55%);
  --chart-1: #0f766e;
  --chart-2: #2563eb;
  --chart-3: #9333ea;
  --chart-4: #f97316;
  --chart-danger: #ef4444;
  --chart-info: #06b6d4;
  --chart-muted: #e5e7eb;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 48px;
}

.dashboard-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  letter-spacing: -0.01em;
}

.dashboard-header :deep(.el-button) {
  height: 36px;
  padding: 0 20px;
  font-size: 14px;
  font-weight: 500;
  background: #1a1a1a;
  border: none;
  color: #fff;
  border-radius: 8px;
}

.dashboard-header :deep(.el-button:hover) {
  background: #2a2a2a;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 32px;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
  margin-bottom: 48px;
}

.chart-card {
  padding: 24px;
  border: 1px solid #e5e5e5;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 8px 30px rgba(15, 23, 42, 0.04);
}

.chart-card.wide {
  grid-column: span 2;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 18px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.chart-note {
  font-size: 12px;
  color: #9ca3af;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.bar-row {
  display: grid;
  grid-template-columns: 90px 1fr 70px;
  gap: 12px;
  align-items: center;
}

.bar-label {
  font-size: 13px;
  color: #4b5563;
  font-weight: 500;
}

.bar-track {
  height: 10px;
  border-radius: 999px;
  background: #f3f4f6;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: inherit;
  transition: width 0.3s ease;
}

.bar-value {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  text-align: right;
}

.donut-wrap {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 16px;
  align-items: center;
}

.donut {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: conic-gradient(var(--chart-muted) 0deg, var(--chart-muted) 360deg);
  position: relative;
}

.donut::after {
  content: '';
  width: 92px;
  height: 92px;
  background: #fff;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px #e5e7eb;
}

.donut-center {
  position: absolute;
  text-align: center;
}

.donut-value {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
}

.donut-label {
  font-size: 12px;
  color: #6b7280;
}

.donut-legend {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.legend-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 13px;
  color: #4b5563;
}

.legend-row strong {
  color: #111827;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  display: inline-block;
}

.legend-dot.danger {
  background: var(--chart-danger);
}

.legend-dot.ok {
  background: #22c55e;
}

.legend-dot.info {
  background: var(--chart-info);
}

.legend-dot.muted {
  background: #cbd5f5;
}

.stat-item {
  padding: 16px 18px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  background: #fafafa;
  transition: all 0.2s;
}

.stat-item:hover {
  border-color: #d4d4d4;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.stat-label {
  font-size: 13px;
  color: #6b6b6b;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 6px;
  letter-spacing: -0.02em;
}

.stat-meta {
  font-size: 12px;
  color: #8a8a8a;
}

.modules-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 48px;
}

.module-item {
  padding: 24px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  background: #fff;
  transition: all 0.2s;
}

.module-item:hover {
  border-color: #d4d4d4;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  padding-bottom: 18px;
  border-bottom: 1px solid #f0f0f0;
}

.module-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.status-badge {
  font-size: 12px;
  padding: 5px 10px;
  background: #f0f0f0;
  color: #5a5a5a;
  border-radius: 6px;
  font-weight: 500;
}

.status-badge.warning {
  background: #fef3c7;
  color: #92400e;
}

.module-data {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.data-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  padding: 2px 0;
}

.data-row span:first-child {
  color: #6b6b6b;
}

.data-row span:last-child {
  color: #1a1a1a;
  font-weight: 600;
}

.system-section {
  padding: 24px;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  background: #fafafa;
}

.system-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 18px;
}

.system-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.system-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
}

.system-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
  flex-shrink: 0;
}

.system-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.system-desc {
  font-size: 12px;
  color: #8a8a8a;
}

@media (max-width: 1024px) {
  .stats-section {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 24px 16px;
  }

  .stats-section,
  .modules-section,
  .charts-section {
    grid-template-columns: 1fr;
  }

  .chart-card.wide {
    grid-column: span 1;
  }

  .donut-wrap {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .bar-row {
    grid-template-columns: 1fr;
    text-align: left;
  }

  .bar-value {
    text-align: left;
  }
}
</style>
