<template>
  <div class="research-project">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>科研项目管理</span>
          <el-button v-if="can('research.project.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增项目
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="项目名称">
          <el-input v-model="searchForm.name" placeholder="请输入项目名称" clearable />
        </el-form-item>
        <el-form-item label="项目状态">
          <el-select v-model="searchForm.project_status" placeholder="请选择项目状态" clearable>
            <el-option label="在研" value="在研" />
            <el-option label="已结题" value="已结题" />
            <el-option label="暂停" value="暂停" />
          </el-select>
        </el-form-item>
        <el-form-item label="研究领域">
          <el-input v-model="searchForm.research_field" placeholder="请输入研究领域" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="project_id" label="编号" width="110" />
        <el-table-column prop="project_name" label="项目名称" min-width="180" />
        <el-table-column label="负责人" min-width="120">
          <template #default="{ row }">
            {{ row.principal_info?.real_name || row.principal }}
          </template>
        </el-table-column>
        <el-table-column prop="applicant_unit" label="申请单位" min-width="140" />
        <el-table-column prop="research_field" label="研究领域" min-width="120" />
        <el-table-column prop="start_date" label="开始日期" min-width="120" />
        <el-table-column prop="end_date" label="结束日期" min-width="120" />
        <el-table-column prop="project_status" label="状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.project_status)">
              {{ row.project_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('research.project.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('research.project.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="项目编号" prop="project_id">
          <el-input v-model="form.project_id" placeholder="请输入项目编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="项目名称" prop="project_name">
          <el-input v-model="form.project_name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="负责人ID" prop="principal">
          <el-select v-model="form.principal" placeholder="请选择负责人" filterable>
            <el-option
              v-for="item in principalOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="申请单位" prop="applicant_unit">
          <el-input v-model="form.applicant_unit" placeholder="请输入申请单位" />
        </el-form-item>
        <el-form-item label="研究领域" prop="research_field">
          <el-input v-model="form.research_field" placeholder="请输入研究领域" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker
            v-model="form.start_date"
            type="date"
            placeholder="选择开始日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker
            v-model="form.end_date"
            type="date"
            placeholder="选择结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="项目状态" prop="project_status">
          <el-select v-model="form.project_status" placeholder="请选择项目状态">
            <el-option label="在研" value="在研" />
            <el-option label="已结题" value="已结题" />
            <el-option label="暂停" value="暂停" />
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
import { getUsers } from '@/api/system'
import {
  getResearchProjects,
  createResearchProject,
  updateResearchProject,
  deleteResearchProject
} from '@/api/research'

// 搜索表单
const searchForm = reactive({
  name: '',
  project_status: '',
  research_field: ''
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
const dialogTitle = ref('新增项目')
const formRef = ref(null)
const form = reactive({
  project_id: '',
  project_name: '',
  principal: '',
  applicant_unit: '',
  research_field: '',
  start_date: '',
  end_date: '',
  project_status: '在研'
})
const submitting = ref(false)
const principalOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  project_id: [{ required: true, message: '请输入项目编号', trigger: 'blur' }],
  project_name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  principal: [{ required: true, message: '请输入负责人ID', trigger: 'blur' }],
  applicant_unit: [{ required: true, message: '请输入申请单位', trigger: 'blur' }],
  research_field: [{ required: true, message: '请输入研究领域', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  project_status: [{ required: true, message: '请选择项目状态', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.name,
      project_status: searchForm.project_status,
      research_field: searchForm.research_field
    }
    const { data } = await getResearchProjects(params)
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
  searchForm.project_status = ''
  searchForm.research_field = ''
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
    '在研': 'primary',
    '已结题': 'success',
    '暂停': 'warning'
  }
  return typeMap[status] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增项目'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑项目'
  Object.assign(form, {
    project_id: row.project_id,
    project_name: row.project_name,
    principal: row.principal,
    applicant_unit: row.applicant_unit,
    research_field: row.research_field,
    start_date: row.start_date,
    end_date: row.end_date,
    project_status: row.project_status
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该项目吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteResearchProject(row.project_id)
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
    if (isEditing.value) {
      await updateResearchProject(form.project_id, form)
      ElMessage.success('更新成功')
    } else {
      await createResearchProject(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.project_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.project_id = ''
  form.project_name = ''
  form.principal = ''
  form.applicant_unit = ''
  form.research_field = ''
  form.start_date = ''
  form.end_date = ''
  form.project_status = '在研'
  formRef.value?.clearValidate()
}

const loadOptions = async () => {
  try {
    const { data } = await getUsers({ page_size: 200 })
    principalOptions.value = (data.results || []).map(item => ({
      label: `${item.user_id} - ${item.real_name || item.username}`,
      value: item.user_id
    }))
  } catch (error) {
    console.error('加载负责人失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchData()
  loadOptions()
})
</script>

<style scoped>
.research-project {
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
