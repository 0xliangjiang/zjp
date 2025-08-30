<template>
  <div id="app">
    <Login v-if="!isLoggedIn" @login="handleLogin" />
    <Dashboard v-else @logout="handleLogout" />
  </div>
</template>

<script>
import Login from './views/Login.vue'
import Dashboard from './views/Dashboard.vue'

export default {
  name: 'App',
  components: {
    Login,
    Dashboard
  },
  data() {
    return {
      isLoggedIn: false
    }
  },
  mounted() {
    const token = localStorage.getItem('token')
    if (token) {
      this.isLoggedIn = true
    }
  },
  methods: {
    handleLogin() {
      this.isLoggedIn = true
    },
    handleLogout() {
      // 用户手动退出时才清除登录状态和本地存储
      this.isLoggedIn = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.$message.success('已成功退出登录')
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
  overflow-x: hidden;
}

#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #1f2937;
  height: 100vh;
  width: 100vw;
  background: #f8fafc;
}

/* 现代化按钮样式 */
.el-button {
  border-radius: 8px !important;
  font-weight: 500 !important;
  padding: 10px 20px !important;
  border: 1px solid transparent !important;
  transition: all 0.2s ease !important;
  font-size: 14px !important;
}

.el-button--primary {
  background: #3b82f6 !important;
  border-color: #3b82f6 !important;
}

.el-button--primary:hover {
  background: #2563eb !important;
  border-color: #2563eb !important;
  transform: none !important;
}

.el-button--default {
  background: white !important;
  border-color: #d1d5db !important;
  color: #374151 !important;
}

.el-button--default:hover {
  border-color: #9ca3af !important;
  background: #f9fafb !important;
}

/* 现代化输入框 */
.el-input__inner {
  border-radius: 8px !important;
  border: 1px solid #d1d5db !important;
  padding: 10px 12px !important;
  font-size: 14px !important;
  transition: all 0.2s ease !important;
}

.el-input__inner:focus {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* 现代化表格 */
.el-table {
  border: 1px solid #e5e7eb !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}

.el-table th {
  background: #f9fafb !important;
  color: #374151 !important;
  font-weight: 600 !important;
  border-bottom: 1px solid #e5e7eb !important;
}

.el-table td {
  border-bottom: 1px solid #f3f4f6 !important;
  padding: 12px !important;
}

.el-table tr:hover td {
  background-color: #f9fafb !important;
}

/* 现代化标签 */
.el-tag {
  border-radius: 6px !important;
  font-weight: 500 !important;
  font-size: 12px !important;
  padding: 4px 8px !important;
}

.el-tag--success {
  background: #dcfce7 !important;
  color: #166534 !important;
  border: 1px solid #bbf7d0 !important;
}

.el-tag--warning {
  background: #fef3c7 !important;
  color: #92400e !important;
  border: 1px solid #fde68a !important;
}

.el-tag--danger {
  background: #fee2e2 !important;
  color: #991b1b !important;
  border: 1px solid #fecaca !important;
}

/* 现代化对话框 */
.el-dialog {
  border-radius: 12px !important;
  border: none !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
}

.el-dialog__header {
  background: white !important;
  border-bottom: 1px solid #e5e7eb !important;
  padding: 20px 24px !important;
}

.el-dialog__title {
  font-weight: 600 !important;
  font-size: 18px !important;
  color: #111827 !important;
}

.el-dialog__body {
  padding: 24px !important;
}

/* 表单样式 */
.el-form-item__label {
  font-weight: 500 !important;
  color: #374151 !important;
  font-size: 14px !important;
}

.el-form-item__error {
  font-size: 12px !important;
  margin-top: 4px !important;
}

/* 菜单样式 */
.el-menu {
  border: none !important;
}

.el-menu-item {
  border-radius: 6px !important;
  margin: 2px 8px !important;
  transition: all 0.2s ease !important;
}

.el-menu-item:hover {
  background: #f3f4f6 !important;
}

.el-menu-item.is-active {
  background: #eff6ff !important;
  color: #3b82f6 !important;
}

/* 现代化radio按钮 */
.el-radio-button__inner {
  border-radius: 6px !important;
  border: 1px solid #d1d5db !important;
  background: white !important;
  color: #374151 !important;
  padding: 8px 16px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
}

.el-radio-button__orig-radio:checked + .el-radio-button__inner {
  background: #3b82f6 !important;
  border-color: #3b82f6 !important;
  color: white !important;
}

/* 响应式辅助类 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

@media (min-width: 640px) {
  .container {
    padding: 0 24px;
  }
}
</style>