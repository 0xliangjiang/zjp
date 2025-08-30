<template>
  <div class="management-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h2 class="page-title">
            <i class="el-icon-s-tools"></i>
            托管管理
          </h2>
          <p class="page-subtitle">管理您的定时抢购任务，自动执行抢购</p>
        </div>
        <div class="header-right">
          <el-button @click="showAddTask" type="primary" icon="el-icon-plus" size="medium">
            添加托管
          </el-button>
          <el-button @click="loadTasks" icon="el-icon-refresh" size="medium">
            刷新
          </el-button>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon waiting">
          <i class="el-icon-time"></i>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ getTaskCountByStatus('waiting') }}</div>
          <div class="stat-label">等待中</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon running">
          <i class="el-icon-loading"></i>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ getTaskCountByStatus('running') }}</div>
          <div class="stat-label">执行中</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon success">
          <i class="el-icon-success"></i>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ getTaskCountByStatus('success') }}</div>
          <div class="stat-label">成功</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon failed">
          <i class="el-icon-error"></i>
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ getTaskCountByStatus('failed') }}</div>
          <div class="stat-label">失败</div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="content-card">
        <!-- 筛选器 -->
        <div class="filter-section">
          <div class="filter-header">
            <h3>任务筛选</h3>
            <span class="task-count">共 {{ filteredTasks.length }} 个任务</span>
          </div>
          <div class="filter-content">
            <el-radio-group v-model="statusFilter" @change="filterTasks" size="medium">
              <el-radio-button label="all">
                <i class="el-icon-menu"></i>
                全部
              </el-radio-button>
              <el-radio-button label="waiting">
                <i class="el-icon-time"></i>
                等待中
              </el-radio-button>
              <el-radio-button label="running">
                <i class="el-icon-loading"></i>
                执行中
              </el-radio-button>
              <el-radio-button label="success">
                <i class="el-icon-success"></i>
                成功
              </el-radio-button>
              <el-radio-button label="failed">
                <i class="el-icon-error"></i>
                失败
              </el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <!-- 任务表格 -->
        <div class="table-section">
          <el-table 
            :data="filteredTasks" 
            style="width: 100%"
            :header-cell-style="{ background: '#f8fafc', color: '#374151', fontWeight: '600' }"
            :row-class-name="getRowClassName"
          >
            <el-table-column prop="id" label="任务ID" width="80" align="center">
              <template slot-scope="scope">
                <span class="task-id">#{{ scope.row.id }}</span>
              </template>
            </el-table-column>
            
            <el-table-column prop="product_name" label="商品名称" min-width="180">
              <template slot-scope="scope">
                <div class="product-info">
                  <div class="product-name">{{ scope.row.product_name }}</div>
                  <div class="product-id">ID: {{ scope.row.product_id }}</div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="target_time" label="目标时间" width="180" align="center">
              <template slot-scope="scope">
                <div class="time-info">
                  <div class="target-time">{{ formatDateTime(scope.row.target_time) }}</div>
                  <div class="time-status" :class="getTimeStatusClass(scope.row)">
                    {{ getTimeStatusText(scope.row) }}
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="retry_count" label="重试进度" width="120" align="center">
              <template slot-scope="scope">
                <div class="retry-progress">
                  <el-progress 
                    :percentage="getRetryPercentage(scope.row)" 
                    :status="getRetryStatus(scope.row)"
                    :stroke-width="8"
                    :show-text="false"
                  />
                  <div class="retry-text">
                    {{ scope.row.current_attempt || 0 }}/{{ scope.row.max_retries }}
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="status" label="状态" width="120" align="center">
              <template slot-scope="scope">
                <div class="status-badge" :class="getStatusClass(scope.row.status)">
                  <i :class="getStatusIcon(scope.row.status)"></i>
                  {{ getStatusText(scope.row.status) }}
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="created_at" label="创建时间" width="160" align="center">
              <template slot-scope="scope">
                <div class="time-info">
                  <div class="created-time">{{ formatDate(scope.row.created_at) }}</div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="200" align="center">
              <template slot-scope="scope">
                <div class="action-buttons">
                  <el-button
                    v-if="scope.row.status === 'waiting'"
                    size="mini"
                    type="success"
                    icon="el-icon-video-play"
                    @click="startTask(scope.row)"
                  >
                    立即执行
                  </el-button>
                  <el-button
                    v-if="scope.row.status === 'waiting'"
                    size="mini"
                    type="danger"
                    icon="el-icon-close"
                    @click="cancelTask(scope.row)"
                  >
                    取消
                  </el-button>
                  <el-button
                    size="mini"
                    type="info"
                    icon="el-icon-document"
                    @click="viewLogs(scope.row)"
                  >
                    查看日志
                  </el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 空状态 -->
          <div v-if="filteredTasks.length === 0" class="empty-state">
            <div class="empty-icon">
              <i class="el-icon-s-tools"></i>
            </div>
            <div class="empty-text">
              <h3>暂无托管任务</h3>
              <p>点击"添加托管"创建您的第一个定时抢购任务</p>
            </div>
            <el-button @click="showAddTask" type="primary" icon="el-icon-plus">
              添加托管任务
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加托管任务对话框 -->
    <el-dialog
      title="添加托管任务"
      :visible.sync="addTaskVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="newTask" label-width="120px" :rules="taskRules" ref="taskForm">
        <el-form-item label="商品选择" prop="product_id">
          <el-select v-model="newTask.product_id" placeholder="选择商品" style="width: 100%">
            <el-option
              v-for="product in availableProducts"
              :key="product.id"
              :label="product.name"
              :value="product.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="目标时间" prop="target_time">
          <el-date-picker
            v-model="newTask.target_time"
            type="datetime"
            placeholder="选择抢购时间"
            style="width: 100%"
            format="yyyy-MM-dd HH:mm:ss"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
        </el-form-item>
        
        <el-form-item label="抢购密码" prop="password">
          <el-input 
            v-model="newTask.password" 
            placeholder="请输入抢购密码"
            show-password
          />
        </el-form-item>
        
        <!-- 签名值已隐藏，自动使用默认值 -->
        
        <el-form-item label="最大重试次数" prop="max_retries">
          <el-input-number 
            v-model="newTask.max_retries" 
            :min="1" 
            :max="5000"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="重试间隔(毫秒)" prop="retry_interval">
          <el-input-number 
            v-model="newTask.retry_interval" 
            :min="100" 
            :max="10000"
            :step="50"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="addTaskVisible = false">取消</el-button>
        <el-button type="primary" @click="addTask">添加任务</el-button>
      </div>
    </el-dialog>

    <!-- 查看日志对话框 -->
    <el-dialog
      title="执行日志"
      :visible.sync="logsVisible"
      width="800px"
    >
      <div class="logs-content">
        <div 
          v-for="(log, index) in taskLogs" 
          :key="index" 
          :class="['log-item', log.type]"
        >
          <span class="log-time">{{ log.time }}</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import request from '../utils/request'
import { DEFAULT_SIGN, DEFAULT_PASSWORD, SYSTEM_CONFIG } from '../config/constants'

export default {
  name: 'Management',
  data() {
    return {
      tasks: [],
      filteredTasks: [],
      statusFilter: 'all',
      addTaskVisible: false,
      logsVisible: false,
      taskLogs: [],
      availableProducts: [],
      newTask: {
        product_id: '',
        target_time: '',
        password: DEFAULT_PASSWORD,
        sign: DEFAULT_SIGN,
        max_retries: SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_MAX_RETRIES,
        retry_interval: SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_RETRY_INTERVAL
      },
      taskRules: {
        product_id: [
          { required: true, message: '请选择商品', trigger: 'change' }
        ],
        target_time: [
          { required: true, message: '请选择目标时间', trigger: 'change' }
        ],
        password: [
          { required: true, message: '请输入抢购密码', trigger: 'blur' }
        ],
      }
    }
  },
  mounted() {
    this.loadTasks()
    this.loadProducts()
  },
  methods: {
    // 生成默认目标时间（当天17:59:58 中国时间 UTC+8）
    getDefaultTargetTime() {
      const today = new Date()
      today.setHours(17, 59, 58, 0)
      
      // 格式化为中国时间格式 YYYY-MM-DD HH:mm:ss
      const year = today.getFullYear()
      const month = String(today.getMonth() + 1).padStart(2, '0')
      const day = String(today.getDate()).padStart(2, '0')
      const hours = String(today.getHours()).padStart(2, '0')
      const minutes = String(today.getMinutes()).padStart(2, '0')
      const seconds = String(today.getSeconds()).padStart(2, '0')
      
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    },
    
    async loadTasks() {
      try {
        const response = await request.get('/api/proxy/tasks')
        this.tasks = response.data.data || []
        this.filterTasks()
      } catch (error) {
        console.error('加载托管任务失败:', error)
        // 模拟数据用于演示
        this.tasks = [
          {
            id: 1,
            product_name: '城市甜心「泡泡糖ORB-X」',
            target_time: '2025-08-28 10:00:00',
            status: 'waiting',
            current_attempt: 0,
            max_retries: 3,
            created_at: '2025-08-28 09:30:00'
          }
        ]
        this.filterTasks()
      }
    },
    
    async loadProducts() {
      try {
        const response = await request.post('/api/proxy/sellMarket/front', {
          price: 1,
          type: 0,
          cate_id: 0,
          keyword: ''
        })
        this.availableProducts = response.data.data || []
      } catch (error) {
        console.error('加载商品列表失败:', error)
      }
    },
    
    filterTasks() {
      if (this.statusFilter === 'all') {
        this.filteredTasks = this.tasks
      } else {
        this.filteredTasks = this.tasks.filter(task => task.status === this.statusFilter)
      }
    },
    
    showAddTask() {
      // 设置默认时间为当天的17:59:58
      this.newTask.target_time = this.getDefaultTargetTime()
      
      this.addTaskVisible = true
    },
    
    async addTask() {
      try {
        await this.$refs.taskForm.validate()
        
        // 获取选中商品的名称
        const selectedProduct = this.availableProducts.find(p => p.id == this.newTask.product_id)
        const productName = selectedProduct ? selectedProduct.name : '未知商品'
        
        const taskData = {
          ...this.newTask,
          product_name: productName,
          user_token: localStorage.getItem('token')
        }
        
        const response = await request.post('/api/proxy/tasks', taskData)
        
        if (response.data.code === 200) {
          this.$message.success('托管任务添加成功')
          this.addTaskVisible = false
          this.loadTasks()
          
          // 重置表单
          this.newTask = {
            product_id: '',
            target_time: this.getDefaultTargetTime(),
            password: DEFAULT_PASSWORD,
            sign: DEFAULT_SIGN,
            max_retries: SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_MAX_RETRIES,
            retry_interval: SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_RETRY_INTERVAL
          }
        } else {
          this.$message.error(response.data.message || '添加失败')
        }
      } catch (error) {
        console.error('添加托管任务失败:', error)
        this.$message.error('添加托管任务失败')
      }
    },
    
    async startTask(task) {
      try {
        await this.$confirm('确定立即执行该托管任务？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        this.$message.info('正在执行抢购任务，请稍候...')
        
        const response = await request.post(`/api/proxy/tasks/${task.id}/start`)
        
        if (response.data.code === 200) {
          const result = response.data.data
          if (result.status === 'success') {
            this.$message.success('抢购成功！')
          } else if (result.status === 'failed') {
            this.$message.error('抢购失败，请查看日志了解详情')
          }
          this.loadTasks()
        } else {
          this.$message.error(response.data.message || '执行失败')
        }
      } catch (error) {
        console.error('执行任务失败:', error)
        this.$message.error('执行任务失败')
      }
    },
    
    async cancelTask(task) {
      try {
        await this.$confirm('确定取消该托管任务？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        const response = await request.post(`/api/proxy/tasks/${task.id}/cancel`)
        
        if (response.data.code === 200) {
          this.$message.success('任务已取消')
          this.loadTasks()
        } else {
          this.$message.error(response.data.message || '取消失败')
        }
      } catch (error) {
        console.error('取消任务失败:', error)
        this.$message.error('取消任务失败')
      }
    },
    
    async viewLogs(task) {
      try {
        const response = await request.get(`/api/proxy/tasks/${task.id}/logs`)
        this.taskLogs = response.data.data || []
        this.logsVisible = true
      } catch (error) {
        console.error('获取任务日志失败:', error)
        // 模拟日志数据
        this.taskLogs = [
          { time: '10:00:00', message: '任务开始执行', type: 'info' },
          { time: '10:00:01', message: '发送抢购请求', type: 'info' },
          { time: '10:00:02', message: '抢购成功', type: 'success' }
        ]
        this.logsVisible = true
      }
    },
    
    getStatusType(status) {
      const typeMap = {
        'waiting': 'warning',
        'running': 'primary',
        'success': 'success',
        'failed': 'danger'
      }
      return typeMap[status] || ''
    },
    
    getStatusText(status) {
      const textMap = {
        'waiting': '等待中',
        'running': '执行中',
        'success': '成功',
        'failed': '失败'
      }
      return textMap[status] || status
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('zh-CN')
    },
    
    formatDateTime(dateString) {
      return new Date(dateString).toLocaleString('zh-CN')
    },
    
    // 新增的方法
    getTaskCountByStatus(status) {
      if (status === 'all') {
        return this.tasks.length
      }
      return this.tasks.filter(task => task.status === status).length
    },
    
    getRowClassName({ row }) {
      if (row.status === 'running') {
        return 'running-row'
      } else if (row.status === 'success') {
        return 'success-row'
      } else if (row.status === 'failed') {
        return 'failed-row'
      }
      return ''
    },
    
    getTimeStatusClass(task) {
      const targetTime = new Date(task.target_time)
      const now = new Date()
      
      if (task.status === 'success' || task.status === 'failed') {
        return 'completed'
      } else if (targetTime <= now) {
        return 'overdue'
      } else if (targetTime - now < 60000) { // 1分钟内
        return 'urgent'
      } else {
        return 'normal'
      }
    },
    
    getTimeStatusText(task) {
      const targetTime = new Date(task.target_time)
      const now = new Date()
      
      if (task.status === 'success' || task.status === 'failed') {
        return '已完成'
      } else if (targetTime <= now) {
        return '已过期'
      } else if (targetTime - now < 60000) { // 1分钟内
        return '即将执行'
      } else {
        const diff = targetTime - now
        const hours = Math.floor(diff / 3600000)
        const minutes = Math.floor((diff % 3600000) / 60000)
        return `${hours}小时${minutes}分钟后`
      }
    },
    
    getRetryPercentage(task) {
      if (task.status === 'success' || task.status === 'failed') {
        return 100
      }
      return Math.round(((task.current_attempt || 0) / task.max_retries) * 100)
    },
    
    getRetryStatus(task) {
      if (task.status === 'success') {
        return 'success'
      } else if (task.status === 'failed') {
        return 'exception'
      } else if (task.status === 'running') {
        return 'warning'
      }
      return ''
    },
    
    getStatusClass(status) {
      const classMap = {
        'waiting': 'status-waiting',
        'running': 'status-running',
        'success': 'status-success',
        'failed': 'status-failed'
      }
      return classMap[status] || ''
    },
    
    getStatusIcon(status) {
      const iconMap = {
        'waiting': 'el-icon-time',
        'running': 'el-icon-loading',
        'success': 'el-icon-success',
        'failed': 'el-icon-error'
      }
      return iconMap[status] || 'el-icon-question'
    }
  }
}
</script>

<style scoped>
.management-container {
  padding: 24px;
  height: 100%;
  background: #f8fafc;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
}

.page-title {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title i {
  color: #3b82f6;
  font-size: 32px;
}

.page-subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

.header-right {
  display: flex;
  gap: 12px;
}

/* 统计卡片 */
.stats-section {
  margin-bottom: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
  cursor: default;
}

.stat-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #d1d5db;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.waiting {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
}

.stat-icon.running {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  animation: pulse 2s infinite;
}

.stat-icon.success {
  background: linear-gradient(135deg, #10b981, #059669);
}

.stat-icon.failed {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.stat-label {
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}

/* 主要内容区域 */
.main-content {
  /* 无需额外样式 */
}

.content-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

/* 筛选器 */
.filter-section {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.filter-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
}

.task-count {
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
}

.filter-content {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

/* 表格样式 */
.table-section {
  position: relative;
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.el-table th {
  background: #f9fafb !important;
  color: #374151 !important;
  font-weight: 600 !important;
  border-bottom: 1px solid #e5e7eb;
}

.el-table td {
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.2s ease;
}

.el-table tbody tr:hover td {
  background-color: #f8fafc !important;
}

/* 行样式 */
.running-row {
  background: rgba(59, 130, 246, 0.05) !important;
}

.success-row {
  background: rgba(16, 185, 129, 0.05) !important;
}

.failed-row {
  background: rgba(239, 68, 68, 0.05) !important;
}

/* 任务ID */
.task-id {
  font-weight: 600;
  color: #667eea;
  font-family: 'Monaco', 'Menlo', monospace;
}

/* 商品信息 */
.product-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  font-weight: 600;
  color: #1f2937;
  line-height: 1.4;
}

.product-id {
  font-size: 12px;
  color: #6b7280;
  font-family: 'Monaco', 'Menlo', monospace;
}

/* 时间信息 */
.time-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
}

.target-time, .created-time {
  font-weight: 500;
  color: #1f2937;
  font-size: 14px;
}

.time-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.time-status.normal {
  background: #dbeafe;
  color: #1d4ed8;
}

.time-status.urgent {
  background: #fef3c7;
  color: #d97706;
  animation: blink 1s infinite;
}

.time-status.overdue {
  background: #fee2e2;
  color: #dc2626;
}

.time-status.completed {
  background: #d1fae5;
  color: #059669;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.5; }
}

/* 重试进度 */
.retry-progress {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
}

.retry-text {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

/* 状态徽章 */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-waiting {
  background: #fef3c7;
  color: #d97706;
}

.status-running {
  background: #dbeafe;
  color: #1d4ed8;
  animation: pulse 2s infinite;
}

.status-success {
  background: #d1fae5;
  color: #059669;
}

.status-failed {
  background: #fee2e2;
  color: #dc2626;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 4px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  transition: all 0.2s ease;
}

.action-buttons .el-button:hover {
  transform: translateY(-1px);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #6b7280;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 24px;
  color: #d1d5db;
}

.empty-text h3 {
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 600;
  color: #374151;
}

.empty-text p {
  margin: 0 0 32px 0;
  font-size: 16px;
  color: #6b7280;
}

/* 日志样式 */
.logs-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 0;
}

.log-item {
  display: flex;
  align-items: center;
  padding: 8px 20px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
  line-height: 1.4;
}

.log-item:last-child {
  border-bottom: none;
}

.log-time {
  color: #909399;
  margin-right: 12px;
  font-family: monospace;
  min-width: 80px;
}

.log-message {
  flex: 1;
  word-break: break-all;
}

.log-item.info {
  background: #f0f9ff;
  color: #1890ff;
}

.log-item.success {
  background: #f6ffed;
  color: #52c41a;
}

.log-item.error {
  background: #fff2f0;
  color: #ff4d4f;
}

.log-item.warning {
  background: #fffbe6;
  color: #faad14;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .management-container {
    padding: 16px;
  }
  
  .page-header {
    padding: 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .stat-card {
    padding: 16px;
  }
  
  .stat-number {
    font-size: 24px;
  }
  
  .content-card {
    padding: 20px;
  }
  
  .filter-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .filter-content {
    flex-wrap: wrap;
  }
  
  .el-table {
    font-size: 14px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
}

@media (max-width: 480px) {
  .management-container {
    padding: 12px;
  }
  
  .stats-section {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 20px;
  }
  
  .content-card {
    padding: 16px;
  }
  
  .el-table {
    font-size: 12px;
  }
  
  .el-table /deep/ .el-table__cell {
    padding: 6px 2px;
  }
  
  .el-table /deep/ .cell {
    word-break: break-all;
  }
}
</style>