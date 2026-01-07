<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button v-if="can('system.user.create')" type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="用户名">
          <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="searchForm.role_type" placeholder="请选择角色" clearable>
            <el-option label="生态监测员" value="生态监测员" />
            <el-option label="数据分析师" value="数据分析师" />
            <el-option label="游客" value="游客" />
            <el-option label="执法人员" value="执法人员" />
            <el-option label="科研人员" value="科研人员" />
            <el-option label="技术人员" value="技术人员" />
            <el-option label="公园管理人员" value="公园管理人员" />
            <el-option label="系统管理员" value="系统管理员" />
          </el-select>
        </el-form-item>
        <el-form-item label="账号状态">
          <el-select v-model="searchForm.account_status" placeholder="请选择状态" clearable>
            <el-option label="正常" value="正常" />
            <el-option label="锁定" value="锁定" />
            <el-option label="停用" value="停用" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" border stripe>
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="real_name" label="真实姓名" min-width="100" />
        <el-table-column prop="role_type" label="角色" min-width="120">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role_type)">
              {{ row.role_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="contact_phone" label="手机号" min-width="120" />
        <el-table-column prop="account_status" label="状态" min-width="90" />
        <el-table-column prop="create_time" label="创建时间" min-width="160" />
        <el-table-column prop="last_login_time" label="最后登录" min-width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="can('system.user.edit')" link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="can('system.user.delete')" link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
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
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model="form.user_id" placeholder="请输入用户ID" :disabled="isEditing" />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码哈希" prop="password_hash" v-if="!form.user_id">
          <el-input v-model="form.password_hash" placeholder="请输入SHA-256密码哈希" />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role_type">
          <el-select v-model="form.role_type" placeholder="请选择角色">
            <el-option label="生态监测员" value="生态监测员" />
            <el-option label="数据分析师" value="数据分析师" />
            <el-option label="游客" value="游客" />
            <el-option label="执法人员" value="执法人员" />
            <el-option label="科研人员" value="科研人员" />
            <el-option label="技术人员" value="技术人员" />
            <el-option label="公园管理人员" value="公园管理人员" />
            <el-option label="系统管理员" value="系统管理员" />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.contact_phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="状态" prop="account_status">
          <el-select v-model="form.account_status" placeholder="请选择状态">
            <el-option label="正常" value="正常" />
            <el-option label="锁定" value="锁定" />
            <el-option label="停用" value="停用" />
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
import {
  getUsers,
  createUser,
  updateUser,
  deleteUser
} from '@/api/system'

// 搜索表单
const searchForm = reactive({
  username: '',
  role_type: '',
  account_status: ''
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
const dialogTitle = ref('新增用户')
const formRef = ref(null)
const form = reactive({
  user_id: '',
  username: '',
  password_hash: '',
  real_name: '',
  role_type: '',
  contact_phone: '',
  account_status: '正常'
})
const submitting = ref(false)
const authStore = useAuthStore()
const role = computed(() => authStore.user?.role_type || '')
const can = (key) => canRole(role.value, key)
const isEditing = computed(() => dialogTitle.value.startsWith('编辑'))

// 表单验证规则
const rules = {
  user_id: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  role_type: [{ required: true, message: '请选择角色', trigger: 'change' }],
  account_status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      search: searchForm.username,
      role_type: searchForm.role_type,
      account_status: searchForm.account_status
    }
    const { data } = await getUsers(params)
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
  searchForm.username = ''
  searchForm.role_type = ''
  searchForm.account_status = ''
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

// 角色标签类型
const getRoleType = (role) => {
  const typeMap = {
    '系统管理员': 'danger',
    '执法人员': 'warning',
    '科研人员': 'primary',
    '游客': 'info'
  }
  return typeMap[role] || 'info'
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增用户'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑用户'
  Object.assign(form, {
    user_id: row.user_id,
    username: row.username,
    password_hash: '',
    real_name: row.real_name,
    role_type: row.role_type,
    contact_phone: row.contact_phone,
    account_status: row.account_status
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该用户吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteUser(row.user_id)
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
      const payload = { ...form }
      if (!payload.password_hash) {
        delete payload.password_hash
      }
      await updateUser(form.user_id, payload)
      ElMessage.success('更新成功')
    } else {
      await createUser(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(form.user_id ? '更新失败' : '创建失败')
    console.error(error)
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.user_id = ''
  form.username = ''
  form.password_hash = ''
  form.real_name = ''
  form.role_type = ''
  form.contact_phone = ''
  form.account_status = '正常'
  formRef.value?.clearValidate()
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.user-management {
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
