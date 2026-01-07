<template>
  <div class="visitor-trajectory">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>游客轨迹追踪</span>
          <el-button v-if="can('visitor.trajectory.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增轨迹
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="游客ID">
          <el-select v-model="searchForm.visitor" placeholder="请选择游客" clearable filterable>
            <el-option
              v-for="item in visitorOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
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
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="trajectory_id" label="编号" width="120" />
        <el-table-column label="游客ID" min-width="100">
          <template #default="{ row }">
            {{ row.visitor_info?.visitor_id || row.visitor }}
          </template>
        </el-table-column>
        <el-table-column label="游客姓名" min-width="100">
          <template #default="{ row }">
            {{ row.visitor_info?.visitor_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="所在区域" min-width="120">
          <template #default="{ row }">
            {{ row.area_info?.area_name || row.area }}
          </template>
        </el-table-column>
        <el-table-column prop="location_latitude" label="纬度" min-width="120" />
        <el-table-column prop="location_longitude" label="经度" min-width="120" />
        <el-table-column prop="tracking_time" label="记录时间" min-width="160" />
        <el-table-column prop="out_of_route" label="是否偏离" min-width="100">
          <template #default="{ row }">
            <el-tag :type="row.out_of_route === 'Y' ? 'danger' : 'success'">
              {{ row.out_of_route === 'Y' ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button link type="info" size="small" @click="handleView(row)">详情</el-button>
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

    <!-- 新增对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="新增轨迹记录"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="轨迹编号" prop="trajectory_id">
          <el-input v-model="form.trajectory_id" placeholder="请输入轨迹编号" />
        </el-form-item>
        <el-form-item label="游客ID" prop="visitor">
          <el-select v-model="form.visitor" placeholder="请选择游客" filterable>
            <el-option
              v-for="item in visitorOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="区域ID" prop="area">
          <el-select v-model="form.area" placeholder="请选择区域" filterable>
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="记录时间" prop="tracking_time">
          <el-date-picker
            v-model="form.tracking_time"
            type="datetime"
            placeholder="请选择记录时间"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="纬度" prop="location_latitude">
          <el-input-number v-model="form.location_latitude" :precision="6" />
        </el-form-item>
        <el-form-item label="经度" prop="location_longitude">
          <el-input-number v-model="form.location_longitude" :precision="6" />
        </el-form-item>
        <el-form-item label="是否偏离" prop="out_of_route">
          <el-select v-model="form.out_of_route" placeholder="请选择">
            <el-option label="是" value="Y" />
            <el-option label="否" value="N" />
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

    <!-- 轨迹详情对话框 -->
    <el-dialog
      v-model="viewVisible"
      title="轨迹详情"
      width="560px"
      :close-on-click-modal="false"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="轨迹编号">{{ viewData.trajectory_id || "-" }}</el-descriptions-item>
        <el-descriptions-item label="游客">{{ viewData.visitor_info?.visitor_name || viewData.visitor || "-" }}</el-descriptions-item>
        <el-descriptions-item label="区域">{{ viewData.area_info?.area_name || viewData.area || "-" }}</el-descriptions-item>
        <el-descriptions-item label="记录时间">{{ viewData.tracking_time || "-" }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ viewData.location_latitude ?? "-" }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ viewData.location_longitude ?? "-" }}</el-descriptions-item>
        <el-descriptions-item label="是否偏离">{{ viewData.out_of_route === "Y" ? "是" : "否" }}</el-descriptions-item>
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
import { getVisitors } from '@/api/visitor'
import { getAreas } from '@/api/system'
import {
  getVisitorTrajectories,
  createTrajectory
} from '@/api/visitor'

// 搜索表单
const searchForm = reactive({
  visitor: '',
  area: ''
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
const formRef = ref(null)
const form = reactive({
  trajectory_id: '',
  visitor: '',
  area: '',
  tracking_time: '',
  location_latitude: null,
  location_longitude: null,
  out_of_route: 'N'
})
const submitting = ref(false)
const visitorOptions = ref([])
const areaOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)

// 表单验证规则
const rules = {
  trajectory_id: [{ required: true, message: '请输入轨迹编号', trigger: 'blur' }],
  visitor: [{ required: true, message: '请输入游客ID', trigger: 'blur' }],
  area: [{ required: true, message: '请输入区域ID', trigger: 'blur' }],
  tracking_time: [{ required: true, message: '请选择记录时间', trigger: 'change' }],
  location_latitude: [{ required: true, message: '请输入纬度', trigger: 'blur' }],
  location_longitude: [{ required: true, message: '请输入经度', trigger: 'blur' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      visitor: searchForm.visitor,
      area: searchForm.area
    }
    const { data } = await getVisitorTrajectories(params)
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
  searchForm.visitor = ''
  searchForm.area = ''
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
  resetForm()
  dialogVisible.value = true
}

// 查看详情
const handleView = (row) => {
  viewData.value = { ...row }
  viewVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await createTrajectory(form)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.trajectory_id = ''
  form.visitor = ''
  form.area = ''
  form.tracking_time = ''
  form.location_latitude = null
  form.location_longitude = null
  form.out_of_route = 'N'
  formRef.value?.clearValidate()
}

const loadOptions = async () => {
  try {
    const [visitorRes, areaRes] = await Promise.all([
      getVisitors({ page_size: 200 }),
      getAreas({ page_size: 200 })
    ])
    visitorOptions.value = (visitorRes.data.results || []).map(item => ({
      label: `${item.visitor_id} - ${item.visitor_name}`,
      value: item.visitor_id
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
.visitor-trajectory {
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
