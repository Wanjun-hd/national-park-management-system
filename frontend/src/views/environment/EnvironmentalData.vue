<template>
  <div class="environmental-data">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>环境数据</span>
          <el-button v-if="can('environment.data.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增数据
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="指标ID">
          <el-select v-model="searchForm.indicator" placeholder="请选择指标" clearable filterable>
            <el-option
              v-for="item in indicatorOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="区域ID">
          <el-select v-model="searchForm.area" placeholder="请选择区域" clearable filterable>
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数据质量">
          <el-select v-model="searchForm.data_quality" placeholder="请选择质量" clearable>
            <el-option label="优" value="优" />
            <el-option label="良" value="良" />
            <el-option label="中" value="中" />
            <el-option label="差" value="差" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <div class="tools-bar">
        <div class="tools-left">
          <el-tag type="info">总数 {{ pagination.total }}</el-tag>
          <el-tag type="success">本页 {{ tableData.length }}</el-tag>
          <el-tag>优 {{ qualityStats.good }}</el-tag>
          <el-tag>良 {{ qualityStats.fair }}</el-tag>
          <el-tag>中 {{ qualityStats.medium }}</el-tag>
          <el-tag>差 {{ qualityStats.poor }}</el-tag>
        </div>
        <div class="tools-right">
          <span class="tools-label">紧凑模式</span>
          <el-switch v-model="denseTable" />
        </div>
      </div>
      <el-table :data="tableData" v-loading="loading" border stripe :size="denseTable ? 'small' : 'default'">
        <el-table-column prop="data_id" label="编号" width="120" />
        <el-table-column label="指标名称" min-width="120">
          <template #default="{ row }">
            {{ row.indicator_info?.indicator_name || row.indicator }}
          </template>
        </el-table-column>
        <el-table-column prop="monitoring_value" label="数值" min-width="100" />
        <el-table-column label="阈值异常" min-width="100">
          <template #default="{ row }">
            <el-tag :type="isAbnormal(row) ? 'danger' : 'success'">
              {{ isAbnormal(row) ? '异常' : '正常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="单位" min-width="80">
          <template #default="{ row }">
            {{ row.indicator_info?.unit || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="监测设备" min-width="120">
          <template #default="{ row }">
            {{ row.device_info?.device_id || row.device }}
          </template>
        </el-table-column>
        <el-table-column label="监测位置" min-width="150">
          <template #default="{ row }">
            {{ row.area_info?.area_name || row.area }}
          </template>
        </el-table-column>
        <el-table-column prop="collection_time" label="采集时间" min-width="160" />
        <el-table-column prop="data_quality" label="数据质量" min-width="100" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleView(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="数据编号" prop="data_id">
          <el-input v-model="form.data_id" placeholder="请输入数据编号" />
        </el-form-item>
        <el-form-item label="指标ID" prop="indicator">
          <el-select v-model="form.indicator" placeholder="请选择指标" filterable>
            <el-option
              v-for="item in indicatorOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="设备ID" prop="device">
          <el-select v-model="form.device" placeholder="请选择设备" filterable>
            <el-option
              v-for="item in deviceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="区域ID" prop="area">
          <el-select v-model="form.area" placeholder="请选择区域" filterable>
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数值" prop="monitoring_value">
          <el-input-number v-model="form.monitoring_value" :precision="2" />
        </el-form-item>
        <el-form-item label="采集时间" prop="collection_time">
          <el-date-picker
            v-model="form.collection_time"
            type="datetime"
            placeholder="请选择采集时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="数据质量" prop="data_quality">
          <el-select v-model="form.data_quality" placeholder="请选择质量">
            <el-option label="优" value="优" />
            <el-option label="良" value="良" />
            <el-option label="中" value="中" />
            <el-option label="差" value="差" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 环境数据详情对话框 -->
    <el-dialog
      v-model="viewVisible"
      title="环境数据详情"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="数据编号">{{ viewData.data_id || "-" }}</el-descriptions-item>
        <el-descriptions-item label="指标">{{ viewData.indicator_info?.indicator_name || viewData.indicator || "-" }}</el-descriptions-item>
        <el-descriptions-item label="单位">{{ viewData.indicator_info?.unit || "-" }}</el-descriptions-item>
        <el-descriptions-item label="监测值">{{ viewData.monitoring_value ?? "-" }}</el-descriptions-item>
        <el-descriptions-item label="阈值下限">{{ viewData.indicator_info?.threshold_lower ?? "-" }}</el-descriptions-item>
        <el-descriptions-item label="阈值上限">{{ viewData.indicator_info?.threshold_upper ?? "-" }}</el-descriptions-item>
        <el-descriptions-item label="设备">{{ viewData.device_info?.device_id || viewData.device || "-" }}</el-descriptions-item>
        <el-descriptions-item label="区域">{{ viewData.area_info?.area_name || viewData.area || "-" }}</el-descriptions-item>
        <el-descriptions-item label="采集时间">{{ viewData.collection_time || "-" }}</el-descriptions-item>
        <el-descriptions-item label="数据质量">{{ viewData.data_quality || "-" }}</el-descriptions-item>
        <el-descriptions-item label="是否异常">{{ isAbnormal(viewData) ? "异常" : "正常" }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="viewVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { canRole } from '@/utils/permissions'
import {
  getEnvironmentalData,
  createEnvironmentalData,
  getIndicators,
  getDevices
} from '@/api/environment'
import { getAreas } from '@/api/system'

// 搜索表单
const searchForm = reactive({
  indicator: '',
  area: '',
  data_quality: ''
})

// 表格数据
const tableData = ref([])
const loading = ref(false)

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 对话框
const dialogVisible = ref(false)
const viewVisible = ref(false)
const viewData = ref({})
const dialogTitle = ref('新增数据')
const formRef = ref(null)
const form = reactive({
  data_id: '',
  indicator: '',
  device: '',
  area: '',
  monitoring_value: 0,
  collection_time: '',
  data_quality: '优'
})
const submitting = ref(false)
const indicatorOptions = ref([])
const deviceOptions = ref([])
const areaOptions = ref([])
const denseTable = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const qualityStats = computed(() => {
  const stats = { good: 0, fair: 0, medium: 0, poor: 0 }
  tableData.value.forEach(item => {
    if (item.data_quality === '优') stats.good += 1
    if (item.data_quality === '良') stats.fair += 1
    if (item.data_quality === '中') stats.medium += 1
    if (item.data_quality === '差') stats.poor += 1
  })
  return stats
})

// 表单验证规则
const rules = {
  data_id: [{ required: true, message: '请输入数据编号', trigger: 'blur' }],
  indicator: [{ required: true, message: '请输入指标ID', trigger: 'blur' }],
  device: [{ required: true, message: '请输入设备ID', trigger: 'blur' }],
  area: [{ required: true, message: '请输入区域ID', trigger: 'blur' }],
  monitoring_value: [{ required: true, message: '请输入数值', trigger: 'blur' }],
  collection_time: [{ required: true, message: '请选择采集时间', trigger: 'change' }],
  data_quality: [{ required: true, message: '请选择数据质量', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      indicator: searchForm.indicator,
      area: searchForm.area,
      data_quality: searchForm.data_quality
    }
    const { data } = await getEnvironmentalData(params)
    tableData.value = data.results || []
    pagination.total = data.count || 0
  } catch (error) {
    ElMessage.error('获取数据失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置
const handleReset = () => {
  searchForm.indicator = ''
  searchForm.area = ''
  searchForm.data_quality = ''
  pagination.page = 1
  fetchData()
}

// 分页
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchData()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  fetchData()
}

// 查看
const handleView = (row) => {
  viewData.value = { ...row }
  viewVisible.value = true
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增数据'
  resetForm()
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await createEnvironmentalData(form)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.data_id = ''
  form.indicator = ''
  form.device = ''
  form.area = ''
  form.monitoring_value = 0
  form.collection_time = ''
  form.data_quality = '优'
  formRef.value?.clearValidate()
}

const isAbnormal = (row) => {
  const upper = row.indicator_info?.threshold_upper
  const lower = row.indicator_info?.threshold_lower
  if (upper === null && lower === null) return false
  if (upper !== null && Number(row.monitoring_value) > Number(upper)) return true
  if (lower !== null && Number(row.monitoring_value) < Number(lower)) return true
  return false
}

const loadOptions = async () => {
  try {
    const [indicatorRes, deviceRes, areaRes] = await Promise.all([
      getIndicators({ page_size: 200 }),
      getDevices({ page_size: 200 }),
      getAreas({ page_size: 200 })
    ])
    indicatorOptions.value = (indicatorRes.data.results || []).map(item => ({
      label: `${item.indicator_id} - ${item.indicator_name}`,
      value: item.indicator_id
    }))
    deviceOptions.value = (deviceRes.data.results || []).map(item => ({
      label: `${item.device_id} - ${item.device_type}`,
      value: item.device_id
    }))
    areaOptions.value = (areaRes.data.results || []).map(item => ({
      label: `${item.area_id} - ${item.area_name}`,
      value: item.area_id
    }))
  } catch (error) {
    console.error('加载选项失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchData()
  loadOptions()
})
</script>

<style scoped>
.environmental-data {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.tools-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 8px 0 16px;
  flex-wrap: wrap;
}

.tools-left {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tools-right {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7280;
  font-size: 12px;
}

.tools-label {
  font-size: 12px;
  color: #6b7280;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
