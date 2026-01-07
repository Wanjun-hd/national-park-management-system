<template>
  <div class="surveillance-point">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>监控点管理</span>
          <el-button v-if="can('enforcement.surveillance.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增监控点
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
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
        <el-form-item label="运行状态">
          <el-select v-model="searchForm.device_status" placeholder="请选择运行状态" clearable>
            <el-option label="正常" value="正常" />
            <el-option label="故障" value="故障" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="monitor_id" label="监控点编号" width="120" />
        <el-table-column label="部署区域" min-width="140">
          <template #default="{ row }">
            {{ row.area_info?.area_name || row.area }}
          </template>
        </el-table-column>
        <el-table-column prop="location_latitude" label="纬度" min-width="110" />
        <el-table-column prop="location_longitude" label="经度" min-width="110" />
        <el-table-column prop="device_status" label="运行状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.device_status)">
              {{ row.device_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="storage_period" label="存储周期(天)" min-width="120" />
        <el-table-column prop="monitoring_range" label="监控范围" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('enforcement.surveillance.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('enforcement.surveillance.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="监控点编号" prop="monitor_id">
          <el-input v-model="form.monitor_id" placeholder="请输入监控点编号" :disabled="isEditing" />
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
        <el-form-item label="纬度">
          <el-input-number v-model="form.location_latitude" :precision="6" />
        </el-form-item>
        <el-form-item label="经度">
          <el-input-number v-model="form.location_longitude" :precision="6" />
        </el-form-item>
        <el-form-item label="运行状态" prop="device_status">
          <el-select v-model="form.device_status" placeholder="请选择运行状态">
            <el-option label="正常" value="正常" />
            <el-option label="故障" value="故障" />
          </el-select>
        </el-form-item>
        <el-form-item label="存储周期(天)" prop="storage_period">
          <el-input-number v-model="form.storage_period" :min="1" />
        </el-form-item>
        <el-form-item label="监控范围">
          <el-input
            v-model="form.monitoring_range"
            type="textarea"
            :rows="3"
            placeholder="请输入监控范围"
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
  getSurveillancePoints,
  createSurveillancePoint,
  updateSurveillancePoint,
  deleteSurveillancePoint
} from '@/api/enforcement'

// 搜索表单
const searchForm = reactive({
  area: '',
  device_status: ''
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
const dialogTitle = ref('新增监控点')
const formRef = ref(null)
const form = reactive({
  monitor_id: '',
  area: '',
  location_longitude: null,
  location_latitude: null,
  monitoring_range: '',
  device_status: '正常',
  storage_period: 90
})
const submitting = ref(false)
const areaOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  monitor_id: [{ required: true, message: '请输入监控点编号', trigger: 'blur' }],
  area: [{ required: true, message: '请输入区域ID', trigger: 'blur' }],
  device_status: [{ required: true, message: '请选择运行状态', trigger: 'change' }],
  storage_period: [{ required: true, message: '请输入存储周期', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      area: searchForm.area,
      device_status: searchForm.device_status
    }
    const { data } = await getSurveillancePoints(params)
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
  searchForm.area = ''
  searchForm.device_status = ''
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
    '故障': 'danger'
  }
  return typeMap[status] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增监控点'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑监控点'
  Object.assign(form, {
    monitor_id: row.monitor_id,
    area: row.area,
    location_longitude: row.location_longitude,
    location_latitude: row.location_latitude,
    monitoring_range: row.monitoring_range,
    device_status: row.device_status,
    storage_period: row.storage_period
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该监控点吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteSurveillancePoint(row.monitor_id)
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
    if (form.monitor_id) {
      await updateSurveillancePoint(form.monitor_id, form)
      ElMessage.success('更新成功')
    } else {
      await createSurveillancePoint(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.monitor_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.monitor_id = ''
  form.area = ''
  form.location_longitude = null
  form.location_latitude = null
  form.monitoring_range = ''
  form.device_status = '正常'
  form.storage_period = 90
  formRef.value?.clearValidate()
}

const loadOptions = async () => {
  try {
    const { data } = await getAreas({ page_size: 200 })
    areaOptions.value = (data.results || []).map(item => ({
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
  loadOptions()
})
</script>

<style scoped>
.surveillance-point {
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
