<template>
  <div class="reservation-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>预约管理</span>
          <el-button v-if="can('visitor.reservation.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增预约
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="预约编号">
          <el-input v-model="searchForm.reservation_id" placeholder="请输入预约编号" clearable />
        </el-form-item>
        <el-form-item label="预约状态">
          <el-select v-model="searchForm.reservation_status" placeholder="请选择预约状态" clearable>
            <el-option label="已确认" value="已确认" />
            <el-option label="已取消" value="已取消" />
            <el-option label="已完成" value="已完成" />
          </el-select>
        </el-form-item>
        <el-form-item label="支付状态">
          <el-select v-model="searchForm.payment_status" placeholder="请选择支付状态" clearable>
            <el-option label="已支付" value="已支付" />
            <el-option label="未支付" value="未支付" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="reservation_id" label="预约编号" min-width="150" />
        <el-table-column label="游客姓名" min-width="100">
          <template #default="{ row }">
            {{ row.visitor_info?.visitor_name || row.visitor }}
          </template>
        </el-table-column>
        <el-table-column label="联系电话" min-width="120">
          <template #default="{ row }">
            {{ row.visitor_info?.contact_phone || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="reservation_date" label="预约日期" min-width="120" />
        <el-table-column prop="entry_time_slot" label="入园时段" min-width="110" />
        <el-table-column prop="party_size" label="人数" min-width="80" />
        <el-table-column prop="ticket_amount" label="购票金额" min-width="100" />
        <el-table-column prop="reservation_status" label="预约状态" min-width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.reservation_status)">
              {{ row.reservation_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="payment_status" label="支付状态" min-width="100" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('visitor.reservation.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button
              v-if="row.reservation_status === '已确认' && can('visitor.reservation.cancel')"
              link
              type="warning"
              size="small"
              @click="handleCancel(row)"
            >
              取消
            </el-button>
            <el-button
              v-if="row.reservation_status === '已确认' && can('visitor.reservation.complete')"
              link
              type="success"
              size="small"
              @click="handleComplete(row)"
            >
              完成
            </el-button>
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
        <el-form-item label="预约编号" prop="reservation_id">
          <el-input v-model="form.reservation_id" placeholder="请输入预约编号" :disabled="isEditing" />
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
        <el-form-item label="预约日期" prop="reservation_date">
          <el-date-picker
            v-model="form.reservation_date"
            type="date"
            placeholder="选择预约日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="入园时段" prop="entry_time_slot">
          <el-input v-model="form.entry_time_slot" placeholder="请输入入园时段" />
        </el-form-item>
        <el-form-item label="预约人数" prop="party_size">
          <el-input-number v-model="form.party_size" :min="1" />
        </el-form-item>
        <el-form-item label="购票金额" prop="ticket_amount">
          <el-input-number v-model="form.ticket_amount" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="预约状态" prop="reservation_status">
          <el-select v-model="form.reservation_status" placeholder="请选择预约状态">
            <el-option label="已确认" value="已确认" />
            <el-option label="已取消" value="已取消" />
            <el-option label="已完成" value="已完成" />
          </el-select>
        </el-form-item>
        <el-form-item label="支付状态" prop="payment_status">
          <el-select v-model="form.payment_status" placeholder="请选择支付状态">
            <el-option label="已支付" value="已支付" />
            <el-option label="未支付" value="未支付" />
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
import { getVisitors } from '@/api/visitor'
import {
  getReservations,
  createReservation,
  updateReservation
} from '@/api/visitor'

// 搜索表单
const searchForm = reactive({
  reservation_id: '',
  reservation_status: '',
  payment_status: ''
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
const dialogTitle = ref('新增预约')
const formRef = ref(null)
const form = reactive({
  reservation_id: '',
  visitor: '',
  reservation_date: '',
  entry_time_slot: '',
  party_size: 1,
  reservation_status: '已确认',
  ticket_amount: 0,
  payment_status: '已支付'
})
const submitting = ref(false)
const visitorOptions = ref([])
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  reservation_id: [{ required: true, message: '请输入预约编号', trigger: 'blur' }],
  visitor: [{ required: true, message: '请输入游客ID', trigger: 'blur' }],
  reservation_date: [{ required: true, message: '请选择预约日期', trigger: 'change' }],
  entry_time_slot: [{ required: true, message: '请输入入园时段', trigger: 'blur' }],
  party_size: [{ required: true, message: '请输入预约人数', trigger: 'blur' }],
  reservation_status: [{ required: true, message: '请选择预约状态', trigger: 'change' }],
  payment_status: [{ required: true, message: '请选择支付状态', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      reservation_id: searchForm.reservation_id,
      reservation_status: searchForm.reservation_status,
      payment_status: searchForm.payment_status
    }
    const { data } = await getReservations(params)
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
  searchForm.reservation_id = ''
  searchForm.reservation_status = ''
  searchForm.payment_status = ''
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
    '已确认': 'success',
    '已取消': 'info',
    '已完成': 'primary'
  }
  return typeMap[status] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增预约'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑预约'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 取消预约
const handleCancel = async (row) => {
  try {
    await updateReservation(row.reservation_id, { ...row, reservation_status: '已取消' })
    ElMessage.success('取消成功')
    fetchData()
  } catch (error) {
    ElMessage.error('取消失败')
    console.error(error)
  }
}

// 完成预约
const handleComplete = async (row) => {
  try {
    await updateReservation(row.reservation_id, { ...row, reservation_status: '已完成' })
    ElMessage.success('已标记完成')
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
    if (form.reservation_id) {
      await updateReservation(form.reservation_id, form)
      ElMessage.success('更新成功')
    } else {
      await createReservation(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.reservation_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.reservation_id = ''
  form.visitor = ''
  form.reservation_date = ''
  form.entry_time_slot = ''
  form.party_size = 1
  form.reservation_status = '已确认'
  form.ticket_amount = 0
  form.payment_status = '已支付'
  formRef.value?.clearValidate()
}

const loadVisitors = async () => {
  try {
    const response = await getVisitors({ page_size: 200 })
    visitorOptions.value = (response.data.results || []).map(item => ({
      label: `${item.visitor_id} - ${item.visitor_name}`,
      value: item.visitor_id
    }))
  } catch (error) {
    console.error('加载游客失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchData()
  loadVisitors()
})
</script>

<style scoped>
.reservation-management {
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
