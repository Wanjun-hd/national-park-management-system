<template>
  <div class="illegal-behavior">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>非法行为记录</span>
          <el-button v-if="can('enforcement.illegal.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增记录
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
        <el-form-item label="处理状态">
          <el-select v-model="searchForm.handling_status" placeholder="请选择处理状态" clearable>
            <el-option label="未处理" value="未处理" />
            <el-option label="处理中" value="处理中" />
            <el-option label="已结案" value="已结案" />
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
          <el-tag type="warning">未处理 {{ statusStats.unhandled }}</el-tag>
          <el-tag>处理中 {{ statusStats.inProgress }}</el-tag>
          <el-tag type="success">已结案 {{ statusStats.closed }}</el-tag>
        </div>
        <div class="tools-right">
          <el-button size="small" :type="searchForm.handling_status ? 'default' : 'primary'" @click="applyStatusFilter('')">全部</el-button>
          <el-button size="small" :type="searchForm.handling_status === '未处理' ? 'primary' : 'default'" @click="applyStatusFilter('未处理')">未处理</el-button>
          <el-button size="small" :type="searchForm.handling_status === '处理中' ? 'primary' : 'default'" @click="applyStatusFilter('处理中')">处理中</el-button>
          <el-button size="small" :type="searchForm.handling_status === '已结案' ? 'primary' : 'default'" @click="applyStatusFilter('已结案')">已结案</el-button>
          <span class="tools-label">紧凑模式</span>
          <el-switch v-model="denseTable" />
        </div>
      </div>
      <el-table :data="tableData" v-loading="loading" border stripe :size="denseTable ? 'small' : 'default'">
        <el-table-column prop="record_id" label="编号" width="120" />
        <el-table-column prop="behavior_type" label="行为类型" min-width="100" />
        <el-table-column label="发生区域" min-width="140">
          <template #default="{ row }">
            {{ row.area_info?.area_name || row.area }}
          </template>
        </el-table-column>
        <el-table-column prop="occurrence_time" label="发生时间" min-width="160" />
        <el-table-column label="执法人员" min-width="120">
          <template #default="{ row }">
            {{ row.enforcer_info?.enforcer_name || row.enforcer || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="handling_status" label="状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.handling_status)">
              {{ row.handling_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="evidence_path" label="证据路径" min-width="200" show-overflow-tooltip />
        <el-table-column prop="penalty_basis" label="处罚依据" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('enforcement.illegal.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('enforcement.illegal.handle')" link type="success" size="small" @click="handleProcess(row)">处理</el-button>
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
        <el-form-item label="行为类型" prop="behavior_type">
          <el-input v-model="form.behavior_type" placeholder="请输入行为类型" />
        </el-form-item>
        <el-form-item label="发生区域" prop="area">
          <el-select v-model="form.area" placeholder="请选择区域" filterable>
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="发生时间" prop="occurrence_time">
          <el-date-picker
            v-model="form.occurrence_time"
            type="datetime"
            placeholder="选择发生时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="证据路径" prop="evidence_path">
          <el-input v-model="form.evidence_path" placeholder="请输入证据路径" />
        </el-form-item>
        <el-form-item label="处理状态" prop="handling_status">
          <el-select v-model="form.handling_status" placeholder="请选择处理状态">
            <el-option label="未处理" value="未处理" />
            <el-option label="处理中" value="处理中" />
            <el-option label="已结案" value="已结案" />
          </el-select>
        </el-form-item>
        <el-form-item label="执法人员">
          <el-select v-model="form.enforcer" placeholder="请选择执法人员" filterable>
            <el-option
              v-for="item in enforcerOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="处理结果">
          <el-input
            v-model="form.handling_result"
            type="textarea"
            :rows="3"
            placeholder="请输入处理结果"
          />
        </el-form-item>
        <el-form-item label="处罚依据">
          <el-input
            v-model="form.penalty_basis"
            type="textarea"
            :rows="3"
            placeholder="请输入处罚依据"
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

    <!-- 处理对话框 -->
    <el-dialog
      v-model="processVisible"
      title="处理非法行为"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-form :model="processForm" label-width="100px">
        <el-form-item label="执法人员">
          <el-select v-model="processForm.enforcer" placeholder="请选择执法人员" filterable>
            <el-option
              v-for="item in enforcerOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="处理结果">
          <el-input
            v-model="processForm.handling_result"
            type="textarea"
            :rows="3"
            placeholder="请输入处理结果"
          />
        </el-form-item>
        <el-form-item label="处罚依据">
          <el-input
            v-model="processForm.penalty_basis"
            type="textarea"
            :rows="3"
            placeholder="请输入处罚依据"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="processVisible = false">取消</el-button>
        <el-button type="primary" @click="submitProcess">提交</el-button>
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
import { getAreas } from '@/api/system'
import {
  getIllegalBehaviors,
  createIllegalBehavior,
  updateIllegalBehavior,
  handleIllegalBehavior,
  getLawEnforcers
} from '@/api/enforcement'

// 搜索表单
const searchForm = reactive({
  area: '',
  handling_status: ''
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
  behavior_type: '',
  occurrence_time: '',
  area: '',
  evidence_path: '',
  handling_status: '未处理',
  enforcer: '',
  handling_result: '',
  penalty_basis: ''
})
const submitting = ref(false)
const processVisible = ref(false)
const processForm = reactive({
  record_id: '',
  enforcer: '',
  handling_result: '',
  penalty_basis: ''
})
const areaOptions = ref([])
const enforcerOptions = ref([])
const denseTable = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))
const statusStats = computed(() => {
  const stats = { unhandled: 0, inProgress: 0, closed: 0 }
  tableData.value.forEach(item => {
    if (item.handling_status === '未处理') stats.unhandled += 1
    if (item.handling_status === '处理中') stats.inProgress += 1
    if (item.handling_status === '已结案') stats.closed += 1
  })
  return stats
})

// 表单验证规则
const rules = {
  record_id: [{ required: true, message: '请输入记录编号', trigger: 'blur' }],
  behavior_type: [{ required: true, message: '请输入行为类型', trigger: 'blur' }],
  area: [{ required: true, message: '请输入区域ID', trigger: 'blur' }],
  occurrence_time: [{ required: true, message: '请选择发生时间', trigger: 'change' }],
  evidence_path: [{ required: true, message: '请输入证据路径', trigger: 'blur' }],
  handling_status: [{ required: true, message: '请选择处理状态', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      area: searchForm.area,
      handling_status: searchForm.handling_status
    }
    const { data } = await getIllegalBehaviors(params)
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
  searchForm.handling_status = ''
  pagination.page = 1
  fetchData()
}

const applyStatusFilter = (status) => {
  searchForm.handling_status = status
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
    '未处理': 'warning',
    '处理中': 'primary',
    '已结案': 'success'
  }
  return typeMap[status] || 'info'
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

// 处理
const handleProcess = (row) => {
  processForm.record_id = row.record_id
  processForm.enforcer = row.enforcer || ''
  processForm.handling_result = ''
  processForm.penalty_basis = ''
  processVisible.value = true
}

const submitProcess = async () => {
  try {
    await handleIllegalBehavior(processForm.record_id, {
      enforcer_id: processForm.enforcer,
      handling_result: processForm.handling_result,
      penalty_basis: processForm.penalty_basis
    })
    ElMessage.success('处理成功')
    processVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('处理失败')
    console.error(error)
  }
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (form.record_id) {
      await updateIllegalBehavior(form.record_id, form)
      ElMessage.success('更新成功')
    } else {
      await createIllegalBehavior(form)
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
  form.behavior_type = ''
  form.occurrence_time = ''
  form.area = ''
  form.evidence_path = ''
  form.handling_status = '未处理'
  form.enforcer = ''
  form.handling_result = ''
  form.penalty_basis = ''
  formRef.value?.clearValidate()
}

const loadOptions = async () => {
  try {
    const [areaRes, enforcerRes] = await Promise.all([
      getAreas({ page_size: 200 }),
      getLawEnforcers({ page_size: 200 })
    ])
    areaOptions.value = (areaRes.data.results || []).map(item => ({
      label: `${item.area_id} - ${item.area_name}`,
      value: item.area_id
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
.illegal-behavior {
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
