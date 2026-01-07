<template>
  <div class="research-achievement">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>科研成果管理</span>
          <el-button v-if="can('research.achievement.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增成果
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="成果名称">
          <el-input v-model="searchForm.name" placeholder="请输入成果名称" clearable />
        </el-form-item>
        <el-form-item label="成果类型">
          <el-select v-model="searchForm.achievement_type" placeholder="请选择成果类型" clearable>
            <el-option label="论文" value="论文" />
            <el-option label="专利" value="专利" />
            <el-option label="报告" value="报告" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="共享权限">
          <el-select v-model="searchForm.share_permission" placeholder="请选择共享权限" clearable>
            <el-option label="公开" value="公开" />
            <el-option label="内部共享" value="内部共享" />
            <el-option label="保密" value="保密" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="achievement_id" label="编号" width="120" />
        <el-table-column prop="achievement_name" label="成果名称" min-width="200" />
        <el-table-column prop="achievement_type" label="成果类型" min-width="100" />
        <el-table-column prop="publish_date" label="发表日期" min-width="120" />
        <el-table-column prop="share_permission" label="共享权限" min-width="100" />
        <el-table-column label="所属项目" min-width="150">
          <template #default="{ row }">
            {{ row.project_info?.project_name || row.project }}
          </template>
        </el-table-column>
        <el-table-column prop="file_path" label="文件路径" min-width="180" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('research.achievement.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('research.achievement.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="成果编号" prop="achievement_id">
          <el-input v-model="form.achievement_id" placeholder="请输入成果编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="成果名称" prop="achievement_name">
          <el-input v-model="form.achievement_name" placeholder="请输入成果名称" />
        </el-form-item>
        <el-form-item label="成果类型" prop="achievement_type">
          <el-select v-model="form.achievement_type" placeholder="请选择成果类型">
            <el-option label="论文" value="论文" />
            <el-option label="专利" value="专利" />
            <el-option label="报告" value="报告" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="发表日期" prop="publish_date">
          <el-date-picker
            v-model="form.publish_date"
            type="date"
            placeholder="选择发表日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="共享权限" prop="share_permission">
          <el-select v-model="form.share_permission" placeholder="请选择共享权限">
            <el-option label="公开" value="公开" />
            <el-option label="内部共享" value="内部共享" />
            <el-option label="保密" value="保密" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属项目ID" prop="project">
          <el-select v-model="form.project" placeholder="请选择项目" filterable>
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="文件路径">
          <el-input v-model="form.file_path" placeholder="请输入文件路径" />
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
  getResearchAchievements,
  createResearchAchievement,
  updateResearchAchievement,
  deleteResearchAchievement,
  getResearchProjects
} from '@/api/research'

// 搜索表单
const searchForm = reactive({
  name: '',
  achievement_type: '',
  share_permission: ''
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
const dialogTitle = ref('新增成果')
const formRef = ref(null)
const form = reactive({
  achievement_id: '',
  achievement_name: '',
  achievement_type: '',
  publish_date: '',
  share_permission: '公开',
  project: '',
  file_path: ''
})
const submitting = ref(false)
const projectOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  achievement_id: [{ required: true, message: '请输入成果编号', trigger: 'blur' }],
  achievement_name: [{ required: true, message: '请输入成果名称', trigger: 'blur' }],
  achievement_type: [{ required: true, message: '请选择成果类型', trigger: 'change' }],
  publish_date: [{ required: true, message: '请选择发表日期', trigger: 'change' }],
  share_permission: [{ required: true, message: '请选择共享权限', trigger: 'change' }],
  project: [{ required: true, message: '请输入项目ID', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.name,
      achievement_type: searchForm.achievement_type,
      share_permission: searchForm.share_permission
    }
    const { data } = await getResearchAchievements(params)
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
  searchForm.achievement_type = ''
  searchForm.share_permission = ''
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
  dialogTitle.value = '新增成果'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑成果'
  Object.assign(form, {
    achievement_id: row.achievement_id,
    achievement_name: row.achievement_name,
    achievement_type: row.achievement_type,
    publish_date: row.publish_date,
    share_permission: row.share_permission,
    project: row.project,
    file_path: row.file_path
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该成果吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteResearchAchievement(row.achievement_id)
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
      await updateResearchAchievement(form.achievement_id, form)
      ElMessage.success('更新成功')
    } else {
      await createResearchAchievement(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.achievement_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.achievement_id = ''
  form.achievement_name = ''
  form.achievement_type = ''
  form.publish_date = ''
  form.share_permission = '公开'
  form.project = ''
  form.file_path = ''
  formRef.value?.clearValidate()
}

const loadOptions = async () => {
  try {
    const { data } = await getResearchProjects({ page_size: 200 })
    projectOptions.value = (data.results || []).map(item => ({
      label: `${item.project_id} - ${item.project_name}`,
      value: item.project_id
    }))
  } catch (error) {
    console.error('加载项目失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchData()
  loadOptions()
})
</script>

<style scoped>
.research-achievement {
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
