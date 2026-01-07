<template>
  <div class="species-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>物种管理</span>
          <el-button v-if="can('biodiversity.species.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增物种
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="物种名称">
          <el-input v-model="searchForm.name" placeholder="请输入物种名称" clearable />
        </el-form-item>
        <el-form-item label="保护级别">
          <el-select v-model="searchForm.protection_level" placeholder="请选择保护级别" clearable>
            <el-option label="国家一级" value="国家一级" />
            <el-option label="国家二级" value="国家二级" />
            <el-option label="无" value="无" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="species_id" label="编号" width="100" />
        <el-table-column prop="chinese_name" label="物种名称" min-width="120" />
        <el-table-column prop="latin_name" label="学名" min-width="160" />
        <el-table-column prop="kingdom" label="界" min-width="90" />
        <el-table-column prop="phylum" label="门" min-width="90" />
        <el-table-column prop="class_field" label="纲" min-width="90" />
        <el-table-column prop="order_name" label="目" min-width="90" />
        <el-table-column prop="family" label="科" min-width="90" />
        <el-table-column prop="genus" label="属" min-width="90" />
        <el-table-column prop="species_name" label="种" min-width="90" />
        <el-table-column prop="protection_level" label="保护级别" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getProtectionLevelType(row.protection_level)">
              {{ row.protection_level }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="habitat_description" label="生存习性" min-width="180" show-overflow-tooltip />
        <el-table-column prop="distribution_range" label="分布范围" min-width="180" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('biodiversity.species.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('biodiversity.species.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="物种编号" prop="species_id">
          <el-input v-model="form.species_id" placeholder="请输入物种编号" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="物种名称" prop="chinese_name">
          <el-input v-model="form.chinese_name" placeholder="请输入物种名称" />
        </el-form-item>
        <el-form-item label="学名" prop="latin_name">
          <el-input v-model="form.latin_name" placeholder="请输入学名" />
        </el-form-item>
        <el-form-item label="界" prop="kingdom">
          <el-input v-model="form.kingdom" placeholder="请输入界" />
        </el-form-item>
        <el-form-item label="门" prop="phylum">
          <el-input v-model="form.phylum" placeholder="请输入门" />
        </el-form-item>
        <el-form-item label="纲" prop="class_field">
          <el-input v-model="form.class_field" placeholder="请输入纲" />
        </el-form-item>
        <el-form-item label="目" prop="order_name">
          <el-input v-model="form.order_name" placeholder="请输入目" />
        </el-form-item>
        <el-form-item label="科" prop="family">
          <el-input v-model="form.family" placeholder="请输入科" />
        </el-form-item>
        <el-form-item label="属" prop="genus">
          <el-input v-model="form.genus" placeholder="请输入属" />
        </el-form-item>
        <el-form-item label="种" prop="species_name">
          <el-input v-model="form.species_name" placeholder="请输入种" />
        </el-form-item>
        <el-form-item label="保护级别" prop="protection_level">
          <el-select v-model="form.protection_level" placeholder="请选择保护级别">
            <el-option label="国家一级" value="国家一级" />
            <el-option label="国家二级" value="国家二级" />
            <el-option label="无" value="无" />
          </el-select>
        </el-form-item>
        <el-form-item label="生存习性">
          <el-input
            v-model="form.habitat_description"
            type="textarea"
            :rows="4"
            placeholder="请输入生存习性"
          />
        </el-form-item>
        <el-form-item label="分布范围">
          <el-input
            v-model="form.distribution_range"
            type="textarea"
            :rows="3"
            placeholder="请输入分布范围"
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
  getSpeciesList,
  createSpecies,
  updateSpecies,
  deleteSpecies
} from '@/api/biodiversity'

// 搜索表单
const searchForm = reactive({
  name: '',
  protection_level: ''
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
const dialogTitle = ref('新增物种')
const formRef = ref(null)
const form = reactive({
  species_id: '',
  chinese_name: '',
  latin_name: '',
  kingdom: '',
  phylum: '',
  class_field: '',
  order_name: '',
  family: '',
  genus: '',
  species_name: '',
  protection_level: '',
  habitat_description: '',
  distribution_range: ''
})
const submitting = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  species_id: [{ required: true, message: '请输入物种编号', trigger: 'blur' }],
  chinese_name: [{ required: true, message: '请输入物种名称', trigger: 'blur' }],
  latin_name: [{ required: true, message: '请输入学名', trigger: 'blur' }],
  kingdom: [{ required: true, message: '请输入界', trigger: 'blur' }],
  phylum: [{ required: true, message: '请输入门', trigger: 'blur' }],
  class_field: [{ required: true, message: '请输入纲', trigger: 'blur' }],
  order_name: [{ required: true, message: '请输入目', trigger: 'blur' }],
  family: [{ required: true, message: '请输入科', trigger: 'blur' }],
  genus: [{ required: true, message: '请输入属', trigger: 'blur' }],
  species_name: [{ required: true, message: '请输入种', trigger: 'blur' }],
  protection_level: [{ required: true, message: '请选择保护级别', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.name,
      protection_level: searchForm.protection_level
    }
    const { data } = await getSpeciesList(params)
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
  searchForm.protection_level = ''
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

// 保护级别标签类型
const getProtectionLevelType = (level) => {
  const typeMap = {
    '国家一级': 'danger',
    '国家二级': 'warning',
    '无': 'info'
  }
  return typeMap[level] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增物种'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑物种'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该物种吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteSpecies(row.species_id)
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
    if (form.species_id) {
      await updateSpecies(form.species_id, form)
      ElMessage.success('更新成功')
    } else {
      await createSpecies(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.species_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.species_id = ''
  form.chinese_name = ''
  form.latin_name = ''
  form.kingdom = ''
  form.phylum = ''
  form.class_field = ''
  form.order_name = ''
  form.family = ''
  form.genus = ''
  form.species_name = ''
  form.protection_level = ''
  form.habitat_description = ''
  form.distribution_range = ''
  formRef.value?.clearValidate()
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.species-management {
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
