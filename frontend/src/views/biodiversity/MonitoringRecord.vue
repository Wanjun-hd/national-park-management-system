<template>
  <div class="monitoring-record">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>监测记录</span>
          <el-button v-if="can('biodiversity.monitoring.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增记录
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="物种编号">
          <el-select v-model="searchForm.species" placeholder="请选择物种" clearable filterable>
            <el-option
              v-for="item in speciesOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="监测方式">
          <el-select v-model="searchForm.monitoring_method" placeholder="请选择监测方式" clearable>
            <el-option label="红外相机" value="红外相机" />
            <el-option label="人工巡查" value="人工巡查" />
            <el-option label="无人机" value="无人机" />
          </el-select>
        </el-form-item>
        <el-form-item label="数据状态">
          <el-select v-model="searchForm.data_status" placeholder="请选择数据状态" clearable>
            <el-option label="有效" value="有效" />
            <el-option label="待核实" value="待核实" />
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
          <el-tag>有效 {{ statusStats.valid }}</el-tag>
          <el-tag type="warning">待核实 {{ statusStats.pending }}</el-tag>
        </div>
        <div class="tools-right">
          <el-button size="small" :type="searchForm.monitoring_method ? 'default' : 'primary'" @click="applyMethodFilter('')">全部</el-button>
          <el-button size="small" :type="searchForm.monitoring_method === '红外相机' ? 'primary' : 'default'" @click="applyMethodFilter('红外相机')">红外相机</el-button>
          <el-button size="small" :type="searchForm.monitoring_method === '人工巡查' ? 'primary' : 'default'" @click="applyMethodFilter('人工巡查')">人工巡查</el-button>
          <el-button size="small" :type="searchForm.monitoring_method === '无人机' ? 'primary' : 'default'" @click="applyMethodFilter('无人机')">无人机</el-button>
          <span class="tools-label">紧凑模式</span>
          <el-switch v-model="denseTable" />
        </div>
      </div>
      <el-table :data="tableData" v-loading="loading" border stripe :size="denseTable ? 'small' : 'default'">
        <el-table-column prop="record_id" label="编号" width="120" />
        <el-table-column label="物种名称" min-width="140">
          <template #default="{ row }">
            {{ row.species_info?.chinese_name || row.species }}
          </template>
        </el-table-column>
        <el-table-column label="监测设备" min-width="140">
          <template #default="{ row }">
            {{ row.device_info?.device_id || row.device }}
          </template>
        </el-table-column>
        <el-table-column prop="monitoring_method" label="监测方式" min-width="120">
          <template #default="{ row }">
            <el-tag>{{ row.monitoring_method }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="monitoring_time" label="监测时间" min-width="160" />
        <el-table-column prop="location_longitude" label="经度" min-width="120" />
        <el-table-column prop="location_latitude" label="纬度" min-width="120" />
        <el-table-column prop="quantity" label="数量" min-width="100" />
        <el-table-column label="记录人" min-width="120">
          <template #default="{ row }">
            {{ row.recorder_info?.real_name || row.recorder }}
          </template>
        </el-table-column>
        <el-table-column prop="data_status" label="数据状态" min-width="110" />
        <el-table-column prop="behavior_description" label="行为描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('biodiversity.monitoring.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('biodiversity.monitoring.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
            <el-button
              v-if="row.data_status === '待核实' && can('biodiversity.monitoring.review')"
              link
              type="success"
              size="small"
              @click="handleReview(row)"
            >
              核实通过
            </el-button>
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="记录编号" prop="record_id">
          <el-input v-model="form.record_id" placeholder="请输入记录编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="物种编号" prop="species">
          <el-select v-model="form.species" placeholder="请选择物种" filterable>
            <el-option
              v-for="item in speciesOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="设备编号" prop="device">
          <el-select v-model="form.device" placeholder="请选择设备" filterable>
            <el-option
              v-for="item in deviceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="记录人" prop="recorder">
          <el-select v-model="form.recorder" placeholder="请选择记录人" filterable>
            <el-option
              v-for="item in recorderOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="监测方式" prop="monitoring_method">
          <el-select v-model="form.monitoring_method" placeholder="请选择监测方式">
            <el-option label="红外相机" value="红外相机" />
            <el-option label="人工巡查" value="人工巡查" />
            <el-option label="无人机" value="无人机" />
          </el-select>
        </el-form-item>
        <el-form-item label="监测时间" prop="monitoring_time">
          <el-date-picker
            v-model="form.monitoring_time"
            type="datetime"
            placeholder="请选择监测时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="经度" prop="location_longitude">
          <el-input-number v-model="form.location_longitude" :precision="6" :step="0.000001" />
        </el-form-item>
        <el-form-item label="纬度" prop="location_latitude">
          <el-input-number v-model="form.location_latitude" :precision="6" :step="0.000001" />
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input-number v-model="form.quantity" :min="0" />
        </el-form-item>
        <el-form-item label="影像路径">
          <el-input v-model="form.image_path" placeholder="请输入影像路径" />
        </el-form-item>
        <el-form-item label="数据状态" prop="data_status">
          <el-select v-model="form.data_status" placeholder="请选择数据状态">
            <el-option label="有效" value="有效" />
            <el-option label="待核实" value="待核实" />
          </el-select>
        </el-form-item>
        <el-form-item label="行为描述">
          <el-input
            v-model="form.behavior_description"
            type="textarea"
            :rows="4"
            placeholder="请输入行为描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { canRole } from '@/utils/permissions'
import {
  getMonitoringRecords,
  createMonitoringRecord,
  updateMonitoringRecord,
  deleteMonitoringRecord,
  patchMonitoringRecord,
  getSpeciesList,
  getMonitoringDevices
} from '@/api/biodiversity'
import { getUsers } from '@/api/system'

// 搜索表单
const searchForm = reactive({
  species: '',
  monitoring_method: '',
  data_status: ''
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
const dialogTitle = ref('新增记录')
const formRef = ref(null)
const form = reactive({
  record_id: '',
  species: '',
  device: '',
  recorder: '',
  monitoring_time: '',
  location_longitude: null,
  location_latitude: null,
  monitoring_method: '',
  image_path: '',
  quantity: 0,
  behavior_description: '',
  data_status: '待核实'
})
const submitting = ref(false)
const speciesOptions = ref([])
const deviceOptions = ref([])
const recorderOptions = ref([])
const denseTable = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))
const statusStats = computed(() => {
  const stats = { valid: 0, pending: 0 }
  tableData.value.forEach(item => {
    if (item.data_status === '有效') stats.valid += 1
    if (item.data_status === '待核实') stats.pending += 1
  })
  return stats
})

// 表单验证规则
const rules = {
  record_id: [{ required: true, message: '请输入记录编号', trigger: 'blur' }],
  species: [{ required: true, message: '请输入物种编号', trigger: 'blur' }],
  device: [{ required: true, message: '请输入设备编号', trigger: 'blur' }],
  recorder: [{ required: true, message: '请输入记录人ID', trigger: 'blur' }],
  monitoring_method: [{ required: true, message: '请选择监测方式', trigger: 'change' }],
  monitoring_time: [{ required: true, message: '请选择监测时间', trigger: 'change' }],
  location_longitude: [{ required: true, message: '请输入经度', trigger: 'blur' }],
  location_latitude: [{ required: true, message: '请输入纬度', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      species: searchForm.species,
      monitoring_method: searchForm.monitoring_method,
      data_status: searchForm.data_status
    }
    const { data } = await getMonitoringRecords(params)
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
  searchForm.species = ''
  searchForm.monitoring_method = ''
  searchForm.data_status = ''
  pagination.page = 1
  fetchData()
}

const applyMethodFilter = (method) => {
  searchForm.monitoring_method = method
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

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增记录'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑记录'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该监测记录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteMonitoringRecord(row.record_id)
        ElMessage.success('删除成功')
        fetchData()
      } catch (error) {
        ElMessage.error('删除失败')
        console.error(error)
      }
    })
    .catch(() => {})
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (form.record_id) {
      await updateMonitoringRecord(form.record_id, form)
      ElMessage.success('更新成功')
    } else {
      await createMonitoringRecord(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.record_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.record_id = ''
  form.species = ''
  form.device = ''
  form.recorder = ''
  form.monitoring_time = ''
  form.location_longitude = null
  form.location_latitude = null
  form.monitoring_method = ''
  form.image_path = ''
  form.quantity = 0
  form.behavior_description = ''
  form.data_status = '待核实'
  formRef.value?.clearValidate()
}

// 审核通过
const handleReview = async (row) => {
  try {
    await patchMonitoringRecord(row.record_id, { data_status: '有效' })
    ElMessage.success('已标记为有效')
    fetchData()
  } catch (error) {
    ElMessage.error('审核失败')
    console.error(error)
  }
}

const loadOptions = async () => {
  try {
    const [speciesRes, deviceRes, userRes] = await Promise.all([
      getSpeciesList({ page_size: 200 }),
      getMonitoringDevices({ page_size: 200 }),
      getUsers({ page_size: 200 })
    ])
    speciesOptions.value = (speciesRes.data.results || []).map(item => ({
      label: `${item.species_id} - ${item.chinese_name}`,
      value: item.species_id
    }))
    deviceOptions.value = (deviceRes.data.results || []).map(item => ({
      label: `${item.device_id} - ${item.device_type}`,
      value: item.device_id
    }))
    recorderOptions.value = (userRes.data.results || []).map(item => ({
      label: `${item.user_id} - ${item.real_name}`,
      value: item.user_id
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
.monitoring-record {
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
  flex-wrap: wrap;
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

