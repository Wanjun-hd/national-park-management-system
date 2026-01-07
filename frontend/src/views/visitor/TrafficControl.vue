<template>
  <div class="traffic-control">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>流量控制</span>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="区域">
          <el-select v-model="searchForm.area" placeholder="请选择区域" clearable filterable>
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="控制状态">
          <el-select v-model="searchForm.current_status" placeholder="请选择控制状态" clearable>
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="限流" value="限流" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="area" label="区域ID" width="100" />
        <el-table-column label="区域名称" min-width="120">
          <template #default="{ row }">
            {{ row.area_info?.area_name || row.area }}
          </template>
        </el-table-column>
        <el-table-column prop="current_visitor_count" label="当前人数" min-width="100" />
        <el-table-column prop="daily_capacity" label="最大容量" min-width="100" />
        <el-table-column label="占用率" min-width="150">
          <template #default="{ row }">
            <el-progress
              :percentage="getOccupancyRate(row)"
              :color="getProgressColor(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="current_status" label="控制状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.current_status)">
              {{ row.current_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warning_threshold" label="预警阈值" min-width="100" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('visitor.traffic.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
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

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑流量控制"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="区域名称">
          <el-input :model-value="form.area_info?.area_name || form.area" disabled />
        </el-form-item>
        <el-form-item label="最大容量" prop="daily_capacity">
          <el-input-number v-model="form.daily_capacity" :min="1" />
        </el-form-item>
        <el-form-item label="预警阈值" prop="warning_threshold">
          <el-input-number v-model="form.warning_threshold" :min="0" />
          <span style="margin-left: 10px;">%</span>
        </el-form-item>
        <el-form-item label="控制状态" prop="current_status">
          <el-select v-model="form.current_status" placeholder="请选择控制状态">
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="限流" value="限流" />
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import { canRole } from '@/utils/permissions'
import { getAreas } from '@/api/system'
import {
  getTrafficControls,
  updateTrafficControl
} from '@/api/visitor'

// 搜索表单
const searchForm = reactive({
  area: '',
  current_status: ''
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
const formRef = ref(null)
const form = reactive({
  area: '',
  area_info: null,
  daily_capacity: 0,
  warning_threshold: 80,
  current_status: '正常'
})
const submitting = ref(false)
const areaOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)

// 表单验证规则
const rules = {
  daily_capacity: [{ required: true, message: '请输入最大容量', trigger: 'blur' }],
  warning_threshold: [{ required: true, message: '请输入预警阈值', trigger: 'blur' }],
  current_status: [{ required: true, message: '请选择控制状态', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      area: searchForm.area,
      current_status: searchForm.current_status
    }
    const { data } = await getTrafficControls(params)
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
  searchForm.current_status = ''
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

// 计算占用率
const getOccupancyRate = (row) => {
  if (!row.daily_capacity) return 0
  return Math.round((row.current_visitor_count / row.daily_capacity) * 100)
}

// 进度条颜色
const getProgressColor = (row) => {
  const rate = getOccupancyRate(row)
  if (rate >= 90) return '#F56C6C'
  if (rate >= row.warning_threshold) return '#E6A23C'
  return '#67C23A'
}

// 状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    '正常': 'success',
    '预警': 'warning',
    '限流': 'danger'
  }
  return typeMap[status] || 'info'
}

// 编辑
const handleEdit = (row) => {
  Object.assign(form, {
    area: row.area,
    area_info: row.area_info || null,
    daily_capacity: row.daily_capacity,
    warning_threshold: row.warning_threshold,
    current_status: row.current_status
  })
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await updateTrafficControl(form.area, {
      daily_capacity: form.daily_capacity,
      warning_threshold: form.warning_threshold,
      current_status: form.current_status
    })
    ElMessage.success('更新成功')
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('更新失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 初始化
onMounted(() => {
  fetchData()
  getAreas({ page_size: 200 })
    .then(({ data }) => {
      areaOptions.value = (data.results || []).map(item => ({
        label: `${item.area_id} - ${item.area_name}`,
        value: item.area_id
      }))
    })
    .catch(error => {
      console.error('??????:', error)
    })
})
</script>

<style scoped>
.traffic-control {
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
