<template>
  <div class="enforcement-dispatch">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>执法调度</span>
          <el-button v-if="can('enforcement.dispatch.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增调度
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="调度状态">
          <el-select v-model="searchForm.dispatch_status" placeholder="请选择调度状态" clearable>
            <el-option label="待响应" value="待响应" />
            <el-option label="已派单" value="已派单" />
            <el-option label="已完成" value="已完成" />
          </el-select>
        </el-form-item>
        <el-form-item label="执法人员ID">
          <el-select v-model="searchForm.enforcer" placeholder="请选择执法人员" clearable filterable>
            <el-option
              v-for="item in enforcerOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="dispatch_id" label="调度编号" width="120" />
        <el-table-column label="关联记录" min-width="160">
          <template #default="{ row }">
            {{ row.record_info?.behavior_type || row.record }}
          </template>
        </el-table-column>
        <el-table-column prop="dispatch_time" label="调度时间" min-width="160" />
        <el-table-column label="执法人员" min-width="120">
          <template #default="{ row }">
            {{ row.enforcer_info?.enforcer_name || row.enforcer }}
          </template>
        </el-table-column>
        <el-table-column prop="response_time" label="响应时间" min-width="160" />
        <el-table-column prop="completion_time" label="完成时间" min-width="160" />
        <el-table-column prop="dispatch_status" label="状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.dispatch_status)">
              {{ row.dispatch_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('enforcement.dispatch.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('enforcement.dispatch.complete')" link type="success" size="small" @click="handleComplete(row)">完成</el-button>
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
        <el-form-item label="调度编号" prop="dispatch_id">
          <el-input v-model="form.dispatch_id" placeholder="请输入调度编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="关联记录ID" prop="record">
          <el-select v-model="form.record" placeholder="请选择非法行为记录" filterable>
            <el-option
              v-for="item in recordOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="执法人员ID" prop="enforcer">
          <el-select v-model="form.enforcer" placeholder="请选择执法人员" filterable>
            <el-option
              v-for="item in enforcerOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="调度时间" prop="dispatch_time">
          <el-date-picker
            v-model="form.dispatch_time"
            type="datetime"
            placeholder="选择调度时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="响应时间">
          <el-date-picker
            v-model="form.response_time"
            type="datetime"
            placeholder="选择响应时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="完成时间">
          <el-date-picker
            v-model="form.completion_time"
            type="datetime"
            placeholder="选择完成时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="状态" prop="dispatch_status">
          <el-select v-model="form.dispatch_status" placeholder="请选择状态">
            <el-option label="待响应" value="待响应" />
            <el-option label="已派单" value="已派单" />
            <el-option label="已完成" value="已完成" />
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
import { Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { canRole } from '@/utils/permissions'
import {
  getEnforcementDispatches,
  createEnforcementDispatch,
  updateEnforcementDispatch,
  getIllegalBehaviors,
  getLawEnforcers
} from '@/api/enforcement'

// 搜索表单
const searchForm = reactive({
  dispatch_status: '',
  enforcer: ''
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
const dialogTitle = ref('新增调度')
const formRef = ref(null)
const form = reactive({
  dispatch_id: '',
  record: '',
  enforcer: '',
  dispatch_time: '',
  response_time: '',
  completion_time: '',
  dispatch_status: '待响应'
})
const submitting = ref(false)
const recordOptions = ref([])
const enforcerOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  dispatch_id: [{ required: true, message: '请输入调度编号', trigger: 'blur' }],
  record: [{ required: true, message: '请输入非法行为记录ID', trigger: 'blur' }],
  enforcer: [{ required: true, message: '请输入执法人员ID', trigger: 'blur' }],
  dispatch_time: [{ required: true, message: '请选择调度时间', trigger: 'change' }],
  dispatch_status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      dispatch_status: searchForm.dispatch_status,
      enforcer: searchForm.enforcer
    }
    const { data } = await getEnforcementDispatches(params)
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
  searchForm.dispatch_status = ''
  searchForm.enforcer = ''
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
    '待响应': 'warning',
    '已派单': 'primary',
    '已完成': 'success'
  }
  return typeMap[status] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增调度'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑调度'
  Object.assign(form, {
    dispatch_id: row.dispatch_id,
    record: row.record,
    enforcer: row.enforcer,
    dispatch_time: row.dispatch_time,
    response_time: row.response_time,
    completion_time: row.completion_time,
    dispatch_status: row.dispatch_status
  })
  dialogVisible.value = true
}

// 完成
const handleComplete = async (row) => {
  try {
    await updateEnforcementDispatch(row.dispatch_id, { ...row, dispatch_status: '已完成' })
    ElMessage.success('操作成功')
    fetchData()
  } catch (error) {
    ElMessage.error('操作失败')
    console.error(error)
  }
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (form.dispatch_id) {
      await updateEnforcementDispatch(form.dispatch_id, form)
      ElMessage.success('更新成功')
    } else {
      await createEnforcementDispatch(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.dispatch_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.dispatch_id = ''
  form.record = ''
  form.enforcer = ''
  form.dispatch_time = ''
  form.response_time = ''
  form.completion_time = ''
  form.dispatch_status = '待响应'
  formRef.value?.clearValidate()
}

const loadOptions = async () => {
  try {
    const [recordRes, enforcerRes] = await Promise.all([
      getIllegalBehaviors({ page_size: 200 }),
      getLawEnforcers({ page_size: 200 })
    ])
    recordOptions.value = (recordRes.data.results || []).map(item => ({
      label: `${item.record_id} - ${item.behavior_type}`,
      value: item.record_id
    }))
    enforcerOptions.value = (enforcerRes.data.results || []).map(item => ({
      label: `${item.enforcer_id} - ${item.enforcer_name}`,
      value: item.enforcer_id
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
.enforcement-dispatch {
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
