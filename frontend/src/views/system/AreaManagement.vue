<template>
  <div class="area-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>区域管理</span>
          <el-button v-if="can('system.area.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增区域
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="区域名称">
          <el-input v-model="searchForm.name" placeholder="请输入区域名称" clearable />
        </el-form-item>
        <el-form-item label="区域类型">
          <el-select v-model="searchForm.area_type" placeholder="请选择区域类型" clearable>
            <el-option label="核心保护区" value="核心保护区" />
            <el-option label="缓冲区" value="缓冲区" />
            <el-option label="实验区" value="实验区" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="area_id" label="区域ID" width="100" />
        <el-table-column prop="area_name" label="区域名称" min-width="150" />
        <el-table-column prop="area_type" label="区域类型" min-width="120">
          <template #default="{ row }">
            <el-tag :type="getAreaTypeTag(row.area_type)">
              {{ row.area_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="area_size" label="面积(公顷)" min-width="120" />
        <el-table-column prop="boundary_description" label="边界描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('system.area.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('system.area.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="区域ID" prop="area_id">
          <el-input v-model="form.area_id" placeholder="请输入区域ID" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="区域名称" prop="area_name">
          <el-input v-model="form.area_name" placeholder="请输入区域名称" />
        </el-form-item>
        <el-form-item label="区域类型" prop="area_type">
          <el-select v-model="form.area_type" placeholder="请选择区域类型">
            <el-option label="核心保护区" value="核心保护区" />
            <el-option label="缓冲区" value="缓冲区" />
            <el-option label="实验区" value="实验区" />
          </el-select>
        </el-form-item>
        <el-form-item label="面积(公顷)" prop="area_size">
          <el-input-number v-model="form.area_size" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="边界描述">
          <el-input
            v-model="form.boundary_description"
            type="textarea"
            :rows="4"
            placeholder="请输入边界描述"
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
import {
  getAreas,
  createArea,
  updateArea,
  deleteArea
} from '@/api/system'

// 搜索表单
const searchForm = reactive({
  name: '',
  area_type: ''
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
const dialogTitle = ref('新增区域')
const formRef = ref(null)
const form = reactive({
  area_id: '',
  area_name: '',
  area_type: '',
  area_size: 0,
  boundary_description: ''
})
const submitting = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  area_id: [{ required: true, message: '请输入区域ID', trigger: 'blur' }],
  area_name: [{ required: true, message: '请输入区域名称', trigger: 'blur' }],
  area_type: [{ required: true, message: '请选择区域类型', trigger: 'change' }],
  area_size: [{ required: true, message: '请输入面积', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.name,
      area_type: searchForm.area_type
    }
    const { data } = await getAreas(params)
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
  searchForm.area_type = ''
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

// 区域类型标签
const getAreaTypeTag = (type) => {
  const typeMap = {
    '核心保护区': 'danger',
    '缓冲区': 'warning',
    '实验区': 'primary'
  }
  return typeMap[type] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增区域'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑区域'
  Object.assign(form, {
    area_id: row.area_id,
    area_name: row.area_name,
    area_type: row.area_type,
    area_size: row.area_size,
    boundary_description: row.boundary_description
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该区域吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteArea(row.area_id)
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
      await updateArea(form.area_id, form)
      ElMessage.success('更新成功')
    } else {
      await createArea(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.area_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.area_id = ''
  form.area_name = ''
  form.area_type = ''
  form.area_size = 0
  form.boundary_description = ''
  formRef.value?.clearValidate()
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.area-management {
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
