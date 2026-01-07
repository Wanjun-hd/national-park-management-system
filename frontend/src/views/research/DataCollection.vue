<template>
  <div class="data-collection">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据采集管理</span>
          <el-button v-if="can('research.data.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增采集记录
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="项目ID">
          <el-select v-model="searchForm.project" placeholder="请选择项目" clearable filterable>
            <el-option
              v-for="item in projectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="数据来源">
          <el-select v-model="searchForm.data_source" placeholder="请选择数据来源" clearable>
            <el-option label="实地采集" value="实地采集" />
            <el-option label="系统调用" value="系统调用" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="collection_id" label="编号" width="120" />
        <el-table-column label="所属项目" min-width="160">
          <template #default="{ row }">
            {{ row.project_info?.project_name || row.project }}
          </template>
        </el-table-column>
        <el-table-column label="采集人" min-width="120">
          <template #default="{ row }">
            {{ row.collector_info?.real_name || row.collector }}
          </template>
        </el-table-column>
        <el-table-column label="采集区域" min-width="140">
          <template #default="{ row }">
            {{ row.area_info?.area_name || row.area }}
          </template>
        </el-table-column>
        <el-table-column prop="collection_time" label="采集时间" min-width="160" />
        <el-table-column prop="data_source" label="数据来源" min-width="100" />
        <el-table-column prop="sample_number" label="样本编号" min-width="120" />
        <el-table-column prop="monitoring_data_id" label="监测数据编号" min-width="140" />
        <el-table-column prop="collection_content" label="采集内容" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('research.data.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('research.data.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="采集编号" prop="collection_id">
          <el-input v-model="form.collection_id" placeholder="请输入采集编号" :disabled="isEditing" />
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
        <el-form-item label="采集人ID" prop="collector">
          <el-select v-model="form.collector" placeholder="请选择采集人" filterable>
            <el-option
              v-for="item in collectorOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="采集区域ID" prop="area">
          <el-select v-model="form.area" placeholder="请选择区域" filterable>
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="采集时间" prop="collection_time">
          <el-date-picker
            v-model="form.collection_time"
            type="datetime"
            placeholder="选择采集时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="数据来源" prop="data_source">
          <el-select v-model="form.data_source" placeholder="请选择数据来源">
            <el-option label="实地采集" value="实地采集" />
            <el-option label="系统调用" value="系统调用" />
          </el-select>
        </el-form-item>
        <el-form-item label="样本编号">
          <el-input v-model="form.sample_number" placeholder="请输入样本编号" />
        </el-form-item>
        <el-form-item label="监测数据编号">
          <el-input v-model="form.monitoring_data_id" placeholder="请输入监测数据编号" />
        </el-form-item>
        <el-form-item label="采集内容" prop="collection_content">
          <el-input
            v-model="form.collection_content"
            type="textarea"
            :rows="4"
            placeholder="请输入采集内容"
          />
        </el-form-item>
        <el-form-item label="调查记录">
          <el-input
            v-model="form.survey_record"
            type="textarea"
            :rows="3"
            placeholder="请输入调查记录"
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
import { getUsers, getAreas } from '@/api/system'
import {
  getDataCollections,
  createDataCollection,
  updateDataCollection,
  deleteDataCollection,
  getResearchProjects
} from '@/api/research'

// 搜索表单
const searchForm = reactive({
  project: '',
  data_source: ''
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
const dialogTitle = ref('新增采集记录')
const formRef = ref(null)
const form = reactive({
  collection_id: '',
  project: '',
  collector: '',
  collection_time: '',
  area: '',
  collection_content: '',
  sample_number: '',
  monitoring_data_id: '',
  survey_record: '',
  data_source: '实地采集'
})
const submitting = ref(false)
const projectOptions = ref([])
const collectorOptions = ref([])
const areaOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  collection_id: [{ required: true, message: '请输入采集编号', trigger: 'blur' }],
  project: [{ required: true, message: '请输入项目ID', trigger: 'blur' }],
  collector: [{ required: true, message: '请输入采集人ID', trigger: 'blur' }],
  area: [{ required: true, message: '请输入区域ID', trigger: 'blur' }],
  collection_time: [{ required: true, message: '请选择采集时间', trigger: 'change' }],
  data_source: [{ required: true, message: '请选择数据来源', trigger: 'change' }],
  collection_content: [{ required: true, message: '请输入采集内容', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      project: searchForm.project,
      data_source: searchForm.data_source
    }
    const { data } = await getDataCollections(params)
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
  searchForm.project = ''
  searchForm.data_source = ''
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
  dialogTitle.value = '新增采集记录'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑采集记录'
  Object.assign(form, {
    collection_id: row.collection_id,
    project: row.project,
    collector: row.collector,
    collection_time: row.collection_time,
    area: row.area,
    collection_content: row.collection_content,
    sample_number: row.sample_number,
    monitoring_data_id: row.monitoring_data_id,
    survey_record: row.survey_record,
    data_source: row.data_source
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该采集记录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteDataCollection(row.collection_id)
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
      await updateDataCollection(form.collection_id, form)
      ElMessage.success('更新成功')
    } else {
      await createDataCollection(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.collection_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.collection_id = ''
  form.project = ''
  form.collector = ''
  form.collection_time = ''
  form.area = ''
  form.collection_content = ''
  form.sample_number = ''
  form.monitoring_data_id = ''
  form.survey_record = ''
  form.data_source = '实地采集'
  formRef.value?.clearValidate()
}

const loadOptions = async () => {
  try {
    const [projectRes, userRes, areaRes] = await Promise.all([
      getResearchProjects({ page_size: 200 }),
      getUsers({ page_size: 200 }),
      getAreas({ page_size: 200 })
    ])
    projectOptions.value = (projectRes.data.results || []).map(item => ({
      label: `${item.project_id} - ${item.project_name}`,
      value: item.project_id
    }))
    collectorOptions.value = (userRes.data.results || []).map(item => ({
      label: `${item.user_id} - ${item.real_name || item.username}`,
      value: item.user_id
    }))
    areaOptions.value = (areaRes.data.results || []).map(item => ({
      label: `${item.area_id} - ${item.area_name}`,
      value: item.area_id
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
.data-collection {
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
