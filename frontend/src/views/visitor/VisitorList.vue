<template>
  <div class="visitor-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>游客管理</span>
          <el-button v-if="can('visitor.list.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增游客
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="关键字">
          <el-input v-model="searchForm.keyword" placeholder="姓名/身份证/手机号" clearable />
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
          <el-tag>在园 {{ inParkCount }}</el-tag>
        </div>
        <div class="tools-right">
          <span class="tools-label">紧凑模式</span>
          <el-switch v-model="denseTable" />
        </div>
      </div>
      <el-table :data="tableData" v-loading="loading" border stripe :size="denseTable ? 'small' : 'default'">
        <el-table-column prop="visitor_id" label="游客ID" width="110" />
        <el-table-column prop="visitor_name" label="姓名" min-width="120" />
        <el-table-column prop="contact_phone" label="手机号" min-width="120" />
        <el-table-column prop="entry_method" label="入园方式" min-width="110" />
        <el-table-column prop="entry_time" label="入园时间" min-width="160" />
        <el-table-column prop="exit_time" label="出园时间" min-width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('visitor.list.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="info" size="small" @click="handleView(row)">详情</el-button>
            <el-button link type="success" size="small" @click="copyPhone(row)">复制手机号</el-button>
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
        <el-form-item label="游客ID" prop="visitor_id">
          <el-input v-model="form.visitor_id" placeholder="请输入游客ID" />
        </el-form-item>
        <el-form-item label="姓名" prop="visitor_name">
          <el-input v-model="form.visitor_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="手机号" prop="contact_phone">
          <el-input v-model="form.contact_phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card_number">
          <el-input v-model="form.id_card_number" placeholder="请输入身份证号" />
        </el-form-item>
        <el-form-item label="入园方式" prop="entry_method">
          <el-select v-model="form.entry_method" placeholder="请选择入园方式">
            <el-option label="线上预约" value="线上预约" />
            <el-option label="现场购票" value="现场购票" />
          </el-select>
        </el-form-item>
        <el-form-item label="入园时间">
          <el-date-picker
            v-model="form.entry_time"
            type="datetime"
            placeholder="选择入园时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="出园时间">
          <el-date-picker
            v-model="form.exit_time"
            type="datetime"
            placeholder="选择出园时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
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

    <!-- 游客详情对话框 -->
    <el-dialog
      v-model="viewVisible"
      title="游客详情"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="游客ID">{{ viewData.visitor_id || "-" }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ viewData.visitor_name || "-" }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ viewData.id_card_number || "-" }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ viewData.contact_phone || "-" }}</el-descriptions-item>
        <el-descriptions-item label="入园方式">{{ viewData.entry_method || "-" }}</el-descriptions-item>
        <el-descriptions-item label="入园时间">{{ viewData.entry_time || "-" }}</el-descriptions-item>
        <el-descriptions-item label="离园时间">{{ viewData.exit_time || "-" }}</el-descriptions-item>
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
  getVisitors,
  createVisitor,
  updateVisitor
} from '@/api/visitor'

// 搜索表单
const searchForm = reactive({
  keyword: ''
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
const dialogTitle = ref('新增游客')
const formRef = ref(null)
const form = reactive({
  visitor_id: '',
  visitor_name: '',
  contact_phone: '',
  id_card_number: '',
  entry_method: '',
  entry_time: '',
  exit_time: ''
})
const submitting = ref(false)
const denseTable = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const inParkCount = computed(() =>
  tableData.value.filter(item => item.entry_time && !item.exit_time).length
)

// 表单验证规则
const rules = {
  visitor_id: [{ required: true, message: '请输入游客ID', trigger: 'blur' }],
  visitor_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  contact_phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  id_card_number: [{ required: true, message: '请输入身份证号', trigger: 'blur' }],
  entry_method: [{ required: true, message: '请选择入园方式', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.keyword
    }
    const { data } = await getVisitors(params)
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
  searchForm.keyword = ''
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
  dialogTitle.value = '新增游客'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑游客'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 查看详情
const handleView = (row) => {
  viewData.value = { ...row }
  viewVisible.value = true
}

const copyPhone = async (row) => {
  const phone = row.contact_phone || ''
  if (!phone) {
    ElMessage.warning('暂无手机号')
    return
  }
  try {
    await navigator.clipboard.writeText(phone)
    ElMessage.success('手机号已复制')
  } catch (error) {
    console.error(error)
    ElMessage.error('复制失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    if (form.visitor_id) {
      await updateVisitor(form.visitor_id, form)
      ElMessage.success('更新成功')
    } else {
      await createVisitor(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.visitor_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.visitor_id = ''
  form.visitor_name = ''
  form.contact_phone = ''
  form.id_card_number = ''
  form.entry_method = ''
  form.entry_time = ''
  form.exit_time = ''
  formRef.value?.clearValidate()
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.visitor-list {
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
