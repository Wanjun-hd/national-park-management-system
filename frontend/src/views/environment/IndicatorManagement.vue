<template>
  <div class="indicator-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>监测指标管理</span>
          <el-button v-if="can('environment.indicator.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增指标
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="指标名称">
          <el-input v-model="searchForm.name" placeholder="请输入指标名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="indicator_id" label="编号" width="100" />
        <el-table-column prop="indicator_name" label="指标名称" min-width="140" />
        <el-table-column prop="unit" label="单位" min-width="80" />
        <el-table-column prop="threshold_lower" label="最小阈值" min-width="100" />
        <el-table-column prop="threshold_upper" label="最大阈值" min-width="100" />
        <el-table-column prop="monitoring_frequency" label="监测频率" min-width="120" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('environment.indicator.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('environment.indicator.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="指标编号" prop="indicator_id">
          <el-input v-model="form.indicator_id" placeholder="请输入指标编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="指标名称" prop="indicator_name">
          <el-input v-model="form.indicator_name" placeholder="请输入指标名称" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="最小阈值">
          <el-input-number v-model="form.threshold_lower" :precision="2" />
        </el-form-item>
        <el-form-item label="最大阈值">
          <el-input-number v-model="form.threshold_upper" :precision="2" />
        </el-form-item>
        <el-form-item label="监测频率" prop="monitoring_frequency">
          <el-select v-model="form.monitoring_frequency" placeholder="请选择监测频率">
            <el-option label="小时" value="小时" />
            <el-option label="日" value="日" />
            <el-option label="周" value="周" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { canRole } from '@/utils/permissions'
import {
  getIndicators,
  createIndicator,
  updateIndicator,
  deleteIndicator
} from '@/api/environment'

// 搜索表单
const searchForm = reactive({
  name: ''
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
const dialogTitle = ref('新增指标')
const formRef = ref(null)
const form = reactive({
  indicator_id: '',
  indicator_name: '',
  unit: '',
  threshold_lower: null,
  threshold_upper: null,
  monitoring_frequency: ''
})
const submitting = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  indicator_id: [{ required: true, message: '请输入指标编号', trigger: 'blur' }],
  indicator_name: [{ required: true, message: '请输入指标名称', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  monitoring_frequency: [{ required: true, message: '请选择监测频率', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.name
    }
    const { data } = await getIndicators(params)
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
  searchForm.name = ''
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
  dialogTitle.value = '新增指标'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑指标'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该监测指标吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteIndicator(row.indicator_id)
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
    if (form.indicator_id) {
      await updateIndicator(form.indicator_id, form)
      ElMessage.success('更新成功')
    } else {
      await createIndicator(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.indicator_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.indicator_id = ''
  form.indicator_name = ''
  form.unit = ''
  form.threshold_lower = null
  form.threshold_upper = null
  form.monitoring_frequency = ''
  formRef.value?.clearValidate()
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.indicator-management {
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
