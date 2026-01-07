<template>
  <div class="device-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备管理</span>
          <el-button v-if="can('environment.device.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增设备
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="设备类型">
          <el-input v-model="searchForm.device_type" placeholder="请输入设备类型" clearable />
        </el-form-item>
        <el-form-item label="运行状态">
          <el-select v-model="searchForm.operation_status" placeholder="请选择运行状态" clearable>
            <el-option label="正常" value="正常" />
            <el-option label="故障" value="故障" />
            <el-option label="离线" value="离线" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="device_id" label="设备编号" width="120" />
        <el-table-column prop="device_type" label="设备类型" min-width="120">
          <template #default="{ row }">
            <el-tag>{{ row.device_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="部署区域" min-width="140">
          <template #default="{ row }">
            {{ row.deployment_area_info?.area_name || row.deployment_area }}
          </template>
        </el-table-column>
        <el-table-column prop="operation_status" label="运行状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.operation_status)">
              {{ row.operation_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="installation_date" label="安装日期" min-width="120" />
        <el-table-column prop="calibration_cycle" label="校准周期(天)" min-width="120" />
        <el-table-column prop="communication_protocol" label="通信协议" min-width="120" />
        <el-table-column prop="last_calibration_date" label="最后校准日期" min-width="130" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('environment.device.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('environment.device.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
            <el-button
              v-if="can('environment.device.status')"
              link
              type="success"
              size="small"
              @click="handleStatus(row, '正常')"
            >
              设为正常
            </el-button>
            <el-button
              v-if="can('environment.device.status')"
              link
              type="warning"
              size="small"
              @click="handleStatus(row, '故障')"
            >
              设为故障
            </el-button>
            <el-button
              v-if="can('environment.device.status')"
              link
              type="info"
              size="small"
              @click="handleStatus(row, '离线')"
            >
              设为离线
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
      <el-form ref="formRef" :model="form" :rules="rules" label-width="110px">
        <el-form-item label="设备编号" prop="device_id">
          <el-input v-model="form.device_id" placeholder="请输入设备编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="设备类型" prop="device_type">
          <el-input v-model="form.device_type" placeholder="请输入设备类型" />
        </el-form-item>
        <el-form-item label="部署区域" prop="deployment_area">
          <el-select v-model="form.deployment_area" placeholder="请选择部署区域" filterable>
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="运行状态" prop="operation_status">
          <el-select v-model="form.operation_status" placeholder="请选择运行状态">
            <el-option label="正常" value="正常" />
            <el-option label="故障" value="故障" />
            <el-option label="离线" value="离线" />
          </el-select>
        </el-form-item>
        <el-form-item label="安装日期" prop="installation_date">
          <el-date-picker
            v-model="form.installation_date"
            type="date"
            placeholder="请选择安装日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="校准周期(天)" prop="calibration_cycle">
          <el-input-number v-model="form.calibration_cycle" :min="1" />
        </el-form-item>
        <el-form-item label="通信协议" prop="communication_protocol">
          <el-input v-model="form.communication_protocol" placeholder="请输入通信协议" />
        </el-form-item>
        <el-form-item label="最后校准日期">
          <el-date-picker
            v-model="form.last_calibration_date"
            type="date"
            placeholder="请选择最后校准日期"
            value-format="YYYY-MM-DD"
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
import { getAreas } from '@/api/system'
import {
  getDevices,
  createDevice,
  updateDevice,
  deleteDevice,
  updateDeviceStatus
} from '@/api/environment'

// 搜索表单
const searchForm = reactive({
  device_type: '',
  operation_status: ''
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
const dialogTitle = ref('新增设备')
const formRef = ref(null)
const form = reactive({
  device_id: '',
  device_type: '',
  deployment_area: '',
  installation_date: '',
  calibration_cycle: 30,
  operation_status: '',
  communication_protocol: '',
  last_calibration_date: ''
})
const submitting = ref(false)
const areaOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  device_id: [{ required: true, message: '请输入设备编号', trigger: 'blur' }],
  device_type: [{ required: true, message: '请选择设备类型', trigger: 'change' }],
  deployment_area: [{ required: true, message: '请输入部署区域ID', trigger: 'blur' }],
  operation_status: [{ required: true, message: '请选择运行状态', trigger: 'change' }],
  installation_date: [{ required: true, message: '请选择安装日期', trigger: 'change' }],
  calibration_cycle: [{ required: true, message: '请输入校准周期', trigger: 'blur' }],
  communication_protocol: [{ required: true, message: '请输入通信协议', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      device_type: searchForm.device_type,
      operation_status: searchForm.operation_status
    }
    const { data } = await getDevices(params)
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
  searchForm.device_type = ''
  searchForm.operation_status = ''
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

// 状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    '正常': 'success',
    '故障': 'danger',
    '离线': 'info'
  }
  return typeMap[status] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增设备'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑设备'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该设备吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteDevice(row.device_id)
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
    if (form.device_id) {
      await updateDevice(form.device_id, form)
      ElMessage.success('更新成功')
    } else {
      await createDevice(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.device_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.device_id = ''
  form.device_type = ''
  form.deployment_area = ''
  form.installation_date = ''
  form.calibration_cycle = 30
  form.operation_status = ''
  form.communication_protocol = ''
  form.last_calibration_date = ''
  formRef.value?.clearValidate()
}

const handleStatus = async (row, status) => {
  try {
    await updateDeviceStatus(row.device_id, status)
    ElMessage.success('状态已更新')
    fetchData()
  } catch (error) {
    ElMessage.error('状态更新失败')
    console.error(error)
  }
}

const loadAreas = async () => {
  try {
    const response = await getAreas({ page_size: 200 })
    areaOptions.value = (response.data.results || []).map(item => ({
      label: `${item.area_id} - ${item.area_name}`,
      value: item.area_id
    }))
  } catch (error) {
    console.error('加载区域失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchData()
  loadAreas()
})
</script>

<style scoped>
.device-management {
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
