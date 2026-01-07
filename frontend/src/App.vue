<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

onMounted(() => {
  // 检查本地存储的登录状态
  authStore.checkAuth()
})
</script>

<style>
:root {
  --font-display: "DM Sans", "Manrope", "Sora", sans-serif;
  --font-body: "Source Sans 3", "Work Sans", "Noto Sans", sans-serif;
  --ink-1: #111827;
  --ink-2: #1f2937;
  --muted-1: #6b7280;
  --bg-1: #f7f5f2;
  --bg-2: #f1f2f4;
  --surface-1: #ffffff;
  --surface-2: #fbfbfa;
  --border-1: #e6e3de;
  --accent-1: #0f766e;
  --shadow-1: 0 10px 30px rgba(15, 23, 42, 0.08);
  --shadow-2: 0 6px 18px rgba(15, 23, 42, 0.06);
  --radius-1: 14px;
  --radius-2: 18px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: var(--font-body);
  color: var(--ink-1);
}

body {
  background: linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
}

#app {
  position: relative;
  isolation: isolate;
}

a {
  color: inherit;
}

/* Form width tuning for inline search + dialogs */
.search-form .el-form-item {
  min-width: 220px;
}

.search-form .el-input,
.search-form .el-select,
.search-form .el-date-editor {
  width: 220px;
}

.search-form .el-input-number {
  width: 160px;
}

.el-dialog .el-form-item .el-input,
.el-dialog .el-form-item .el-select,
.el-dialog .el-form-item .el-date-editor {
  width: 260px;
}

@media (max-width: 768px) {
  .search-form .el-form-item,
  .search-form .el-input,
  .search-form .el-select,
  .search-form .el-date-editor,
  .el-dialog .el-form-item .el-input,
  .el-dialog .el-form-item .el-select,
  .el-dialog .el-form-item .el-date-editor {
    width: 100%;
    min-width: 0;
  }
}
</style>
