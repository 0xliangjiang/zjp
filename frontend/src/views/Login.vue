<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>抢购系统</h1>
        <p>输入手机号码和密码开始使用</p>
      </div>
      
      <div class="login-form">
        <el-form :model="form" :rules="rules" ref="loginForm">
          <el-form-item prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号"
              size="large"
              maxlength="11"
            >
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password
            >
            </el-input>
          </el-form-item>
          
          <el-button
            type="primary"
            @click="login"
            :loading="loading"
            size="large"
            class="login-btn"
          >
            登录
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import request from '../utils/request'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        phone: '',
        password: ''
      },
      rules: {
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3456789]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码至少6位', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    async login() {
      try {
        const valid = await new Promise((resolve) => {
          this.$refs.loginForm.validate((valid) => {
            resolve(valid)
          })
        })
        if (!valid) return
        
        this.loading = true
        
        const response = await request.post('/api/login_password', {
          mobile: this.form.phone,
          password: this.form.password
        })
        
        // 检查抢购平台登录是否成功
        if (response.data.code === 200) {
          // 保存抢购平台的token
          localStorage.setItem('token', response.data.data.token)
          localStorage.setItem('user', JSON.stringify({
            phone: this.form.phone,
            ...response.data.data
          }))
        } else {
          throw new Error(response.data.message || '登录失败')
        }
        
        this.$message.success('登录成功')
        this.$emit('login')
        
      } catch (error) {
        if (error.response) {
          this.$message.error(error.response.data.error || '登录失败')
        } else {
          this.$message.error('登录失败')
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.login-header p {
  color: #6b7280;
  font-size: 14px;
}

.login-form {
  space-y: 20px;
}

.login-form .el-form-item {
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
  height: 44px;
  font-weight: 600;
}

/* 移动端优化 */
@media (max-width: 480px) {
  .login-page {
    padding: 16px;
  }
  
  .login-container {
    padding: 32px 24px;
  }
  
  .login-header h1 {
    font-size: 20px;
  }
  

}
</style>