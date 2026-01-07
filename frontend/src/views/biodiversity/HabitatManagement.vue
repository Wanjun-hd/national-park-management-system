<template>
  <div class="habitat-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>栖息地管理</span>
          <el-button v-if="can('biodiversity.habitat.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增栖息地
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="区域名称">
          <el-input v-model="searchForm.area_name" placeholder="请输入区域名称" clearable />
        </el-form-item>
        <el-form-item label="生态类型">
          <el-select v-model="searchForm.ecology_type" placeholder="请选择类型" clearable>
            <el-option label="森林" value="森林" />
            <el-option label="湿地" value="湿地" />
            <el-option label="草原" value="草原" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="habitat_id" label="编号" width="110" />
        <el-table-column prop="area_name" label="区域名称" min-width="150" />
        <el-table-column prop="ecology_type" label="生态类型" min-width="110">
          <template #default="{ row }">
            <el-tag>{{ row.ecology_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="area_size" label="面积(公顷)" min-width="120" />
        <el-table-column prop="core_protection_range" label="核心保护范围" min-width="200" show-overflow-tooltip />
        <el-table-column prop="suitability_score" label="适宜性评分" min-width="120" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('biodiversity.habitat.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('biodiversity.habitat.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="栖息地编号" prop="habitat_id">
          <el-input v-model="form.habitat_id" placeholder="请输入栖息地编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="区域名称" prop="area_name">
          <el-input v-model="form.area_name" placeholder="请输入区域名称" />
        </el-form-item>
        <el-form-item label="生态类型" prop="ecology_type">
          <el-select v-model="form.ecology_type" placeholder="请选择类型">
            <el-option label="森林" value="森林" />
            <el-option label="湿地" value="湿地" />
            <el-option label="草原" value="草原" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="面积(公顷)" prop="area_size">
          <el-input-number v-model="form.area_size" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="核心保护范围">
          <el-input
            v-model="form.core_protection_range"
            type="textarea"
            :rows="3"
            placeholder="请输入核心保护范围"
          />
        </el-form-item>
        <el-form-item label="适宜性评分">
          <el-input-number v-model="form.suitability_score" :min="0" :max="10" :precision="1" />
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
  getHabitatList,
  createHabitat,
  updateHabitat,
  deleteHabitat
} from '@/api/biodiversity'

// 搜索表单
const searchForm = reactive({
  area_name: '',
  ecology_type: ''
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
const dialogTitle = ref('新增栖息地')
const formRef = ref(null)
const form = reactive({
  habitat_id: '',
  area_name: '',
  ecology_type: '',
  area_size: 0,
  core_protection_range: '',
  suitability_score: null
})
const submitting = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  habitat_id: [{ required: true, message: '请输入栖息地编号', trigger: 'blur' }],
  area_name: [{ required: true, message: '请输入区域名称', trigger: 'blur' }],
  ecology_type: [{ required: true, message: '请选择生态类型', trigger: 'change' }],
  area_size: [{ required: true, message: '请输入面积', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.area_name,
      ecology_type: searchForm.ecology_type
    }
    const { data } = await getHabitatList(params)
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
  searchForm.area_name = ''
  searchForm.ecology_type = ''
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
  dialogTitle.value = '新增栖息地'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑栖息地'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该栖息地吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteHabitat(row.habitat_id)
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
    if (form.habitat_id) {
      await updateHabitat(form.habitat_id, form)
      ElMessage.success('更新成功')
    } else {
      await createHabitat(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.habitat_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.habitat_id = ''
  form.area_name = ''
  form.ecology_type = ''
  form.area_size = 0
  form.core_protection_range = ''
  form.suitability_score = null
  formRef.value?.clearValidate()
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.habitat-management {
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

