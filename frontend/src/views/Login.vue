<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-panel">
        <div class="login-header">
          <h1>国家公园管理系统</h1>
          <p>National Park Management System</p>
        </div>

        <el-form :model="loginForm" class="login-form" @submit.prevent="handleLogin">
          <el-form-item>
            <el-input
              v-model="loginForm.username"
              placeholder="用户名"
              size="large"
              clearable
            />
          </el-form-item>

          <el-form-item>
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="密码"
              size="large"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中' : '登录' }}
          </el-button>
        </el-form>

        <div class="footer">
          <el-button link @click="createTestUsers">创建测试账号</el-button>
        </div>
      </div>

      <div class="demo-panel">
        <div class="demo-title">演示账号</div>
        <div class="demo-accounts">
          <div class="demo-item" @click="fillAccount('admin', 'admin123')">
            <span class="demo-label">系统管理员</span>
            <span class="demo-credentials">admin / admin123</span>
          </div>
          <div class="demo-item" @click="fillAccount('monitor', 'monitor123')">
            <span class="demo-label">生态监测员</span>
            <span class="demo-credentials">monitor / monitor123</span>
          </div>
          <div class="demo-item" @click="fillAccount('analyst', 'analyst123')">
            <span class="demo-label">数据分析师</span>
            <span class="demo-credentials">analyst / analyst123</span>
          </div>
          <div class="demo-item" @click="fillAccount('visitor', 'visitor123')">
            <span class="demo-label">游客</span>
            <span class="demo-credentials">visitor / visitor123</span>
          </div>
          <div class="demo-item" @click="fillAccount('enforcer', 'enforcer123')">
            <span class="demo-label">执法人员</span>
            <span class="demo-credentials">enforcer / enforcer123</span>
          </div>
          <div class="demo-item" @click="fillAccount('researcher', 'researcher123')">
            <span class="demo-label">科研人员</span>
            <span class="demo-credentials">researcher / researcher123</span>
          </div>
          <div class="demo-item" @click="fillAccount('manager', 'manager123')">
            <span class="demo-label">公园管理人员</span>
            <span class="demo-credentials">manager / manager123</span>
          </div>
          <div class="demo-item" @click="fillAccount('tech', 'tech123')">
            <span class="demo-label">技术人员</span>
            <span class="demo-credentials">tech / tech123</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { createTestUser } from '@/api/auth'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const loginForm = ref({ username: '', password: '' })

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await authStore.login(loginForm.value)
    ElMessage.success('登录成功！')
    router.push('/dashboard')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

const fillAccount = (username, password) => {
  loginForm.value = { username, password }
  ElMessage.info('已填充账号信息')
}

const createTestUsers = async () => {
  try {
    await createTestUser()
    ElMessage.success('测试账号创建成功！')
  } catch {
    ElMessage.warning('测试账号可能已存在')
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  padding: 24px;
}

.login-box {
  width: 100%;
  max-width: 860px;
  background: var(--surface-1);
  border: 1px solid var(--border-1);
  border-radius: var(--radius-2);
  box-shadow: var(--shadow-1);
  padding: 28px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr);
  gap: 24px;
}

.login-header {
  margin-bottom: 28px;
  text-align: center;
}

.login-header h1 {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 600;
  color: var(--ink-1);
  margin: 0 0 8px 0;
  letter-spacing: -0.02em;
}

.login-header p {
  font-size: 14px;
  color: var(--muted-1);
  margin: 0;
  font-weight: 400;
}

.login-form {
  margin-bottom: 24px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 16px;
}

.login-form :deep(.el-input__wrapper) {
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid var(--border-1);
  box-shadow: none;
  background: var(--surface-1);
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(15, 23, 42, 0.2);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--accent-1);
  box-shadow: 0 0 0 1px var(--accent-1);
}

.login-form :deep(.el-input__inner) {
  font-size: 15px;
  color: var(--ink-1);
}

.login-form :deep(.el-input__inner::placeholder) {
  color: #9ca3af;
}

.login-button {
  width: 100%;
  height: 44px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  background: var(--accent-1);
  border: none;
  color: #fff;
  margin-top: 6px;
}

.login-button:hover {
  background: #0b5f59;
}

.login-button:active {
  background: #094f4a;
}

.demo-title {
  font-size: 14px;
  color: var(--muted-1);
  margin-bottom: 12px;
  font-weight: 500;
}

.demo-accounts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.demo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px;
  border: 1px solid var(--border-1);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s ease;
  background: var(--surface-2);
  gap: 10px;
}

.demo-item:hover {
  border-color: rgba(15, 23, 42, 0.18);
  background: var(--surface-1);
}

.demo-item:active {
  background: #f2f3f5;
}

.demo-label {
  font-size: 13px;
  color: var(--ink-1);
  font-weight: 500;
}

.demo-credentials {
  font-size: 12px;
  color: var(--muted-1);
  font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
}

.footer {
  text-align: left;
}

.footer :deep(.el-button) {
  font-size: 13px;
  color: var(--muted-1);
  font-weight: 400;
}

.footer :deep(.el-button:hover) {
  color: var(--ink-1);
}

@media (max-width: 860px) {
  .login-box {
    grid-template-columns: 1fr;
  }

  .demo-accounts {
    grid-template-columns: 1fr;
  }
}
</style>
