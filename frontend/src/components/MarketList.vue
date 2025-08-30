<template>
  <div class="market-list-page">
    <div class="page-header">
      <h2>市场列表</h2>
      <div class="header-actions">
        <el-button @click="showPurchaseSettings" icon="el-icon-setting" size="small">抢购设置</el-button>
        <el-button @click="loadMarketList" icon="el-icon-refresh" :loading="loading">刷新</el-button>
      </div>
    </div>

    <div class="market-content">
      <!-- 商品信息 -->
      <div class="market-info-section">
        <div class="info-header">
          <div class="info-title">
            <i class="el-icon-goods"></i>
            <span>可抢购商品</span>
          </div>
          <div class="info-stats">
            共 {{ marketList.length }} 个商品
          </div>
        </div>
      </div>

      <!-- 市场列表 -->
      <div class="market-grid">
        <div 
          v-for="item in marketList" 
          :key="item.id" 
          class="market-card"
          @click="viewMarketDetail(item)"
        >
          <div class="market-header">
            <div class="market-status">
              <span 
                :class="['status-badge', item.is_rise === '1' ? 'status-up' : 'status-down']"
              >
                {{ item.is_rise === '1' ? '上涨' : '下跌' }}
              </span>
            </div>
          </div>
          
          <div class="market-info">
            <h3 class="market-name">{{ item.name }}</h3>
            <div class="market-stats">
              <div class="stat-item">
                <span class="stat-label">当前价格:</span>
                <span class="stat-value price">¥{{ item.price || '0.00' }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">最高价格:</span>
                <span class="stat-value max-price">¥{{ item.price_max }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">市场编号:</span>
                <span class="stat-value">{{ item.market_number }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">限制数量:</span>
                <span class="stat-value">{{ item.limit_number }}</span>
              </div>
            </div>
            
            <!-- 抢购按钮区域 -->
            <div class="purchase-section">
              <div v-if="!item.purchasing" class="purchase-buttons">
                <button 
                  class="purchase-btn primary-purchase"
                  @click.stop="startAutoPurchase(item)"
                  :disabled="!canPurchase(item)"
                >
                  <div class="btn-content">
                    <i class="el-icon-lightning"></i>
                    <span class="btn-text">智能抢购</span>
                  </div>
                  <div class="btn-subtitle">多线程并发</div>
                </button>
                
                <button 
                  class="purchase-btn super-purchase"
                  @click.stop="startSuperPurchase(item)"
                  :disabled="!canPurchase(item)"
                >
                  <div class="btn-content">
                    <i class="el-icon-rocket"></i>
                    <span class="btn-text">极速抢购</span>
                  </div>
                  <div class="btn-subtitle">后端加速</div>
                </button>
              </div>
              
              <div v-else class="purchasing-status">
                <div class="status-header">
                  <div class="status-icon">
                    <i class="el-icon-loading"></i>
                  </div>
                  <div class="status-text">
                    <div class="status-title">抢购中...</div>
                    <div class="status-progress">{{ item.currentAttempt || 0 }}/{{ purchaseSettings.maxRetries }} 次尝试</div>
                  </div>
                </div>
                
                <button 
                  class="purchase-btn stop-purchase"
                  @click.stop="stopPurchase(item)"
                >
                  <i class="el-icon-close"></i>
                  <span>停止抢购</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 抢购日志 -->
      <div v-if="purchaseLogs.length > 0" class="purchase-logs">
        <div class="logs-header">
          <h3>抢购日志</h3>
          <el-button size="small" @click="clearLogs">清空日志</el-button>
        </div>
        <div class="logs-content">
          <div 
            v-for="(log, index) in purchaseLogs" 
            :key="index" 
            :class="['log-item', log.type]"
          >
            <span class="log-time">{{ log.time }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="marketList.length === 0 && !loading" class="empty-state">
        <i class="el-icon-shopping-bag-1"></i>
        <p>暂无市场数据</p>
        <el-button type="primary" @click="loadMarketList">重新加载</el-button>
      </div>
    </div>
    
    <!-- 抢购设置对话框 -->
    <el-dialog
      title="抢购设置"
      :visible.sync="settingsVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="purchaseSettings" label-width="120px">
        <div class="settings-tip">
          <i class="el-icon-info"></i>
          <span>自动抢购将根据设置的重试次数和间隔时间进行多次抢购尝试</span>
        </div>
        <el-form-item label="抢购密码">
          <el-input 
            v-model="purchaseSettings.password" 
            placeholder="请输入抢购密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="自动抢购">
          <el-switch v-model="purchaseSettings.autoPurchase" />
        </el-form-item>
        <el-form-item label="抢购间隔(毫秒)" v-if="purchaseSettings.autoPurchase">
          <el-input-number 
            v-model="purchaseSettings.interval" 
            :min="100" 
            :max="10000"
            :step="100"
          />
        </el-form-item>
        <el-form-item label="最大重试次数" v-if="purchaseSettings.autoPurchase">
          <el-input-number 
            v-model="purchaseSettings.maxRetries" 
            :min="1" 
            :max="10"
          />
        </el-form-item>
        <el-form-item label="超级抢购线程数">
          <el-input-number 
            v-model="purchaseSettings.superThreadCount" 
            :min="5" 
            :max="20"
            :step="1"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="settingsVisible = false">取消</el-button>
        <el-button type="primary" @click="savePurchaseSettings">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import request from '../utils/request'
import { DEFAULT_SIGN, DEFAULT_PASSWORD, SYSTEM_CONFIG } from '../config/constants'

export default {
  name: 'MarketList',
  data() {
    return {
      loading: false,
      marketList: [],
      // 移除searchForm，直接使用默认搜索参数
      purchaseLogs: [], // 抢购日志
      purchasePassword: DEFAULT_PASSWORD, // 抢购密码
      purchaseSign: DEFAULT_SIGN, // 抢购签名
      settingsVisible: false, // 设置对话框显示状态
      purchaseSettings: {
        password: DEFAULT_PASSWORD,
        sign: DEFAULT_SIGN,
        autoPurchase: false,
        interval: SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_RETRY_INTERVAL,
        maxRetries: SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_MAX_RETRIES,
        superThreadCount: SYSTEM_CONFIG.PURCHASE_CONFIG.DEFAULT_SUPER_THREAD_COUNT
      }
    }
  },
  mounted() {
    this.loadMarketList()
  },
  methods: {
    async loadMarketList() {
      try {
        this.loading = true
        console.log('开始加载市场列表')
        
        // 使用固定的搜索参数
        const searchParams = {
          price: 1,
          type: 0,
          cate_id: 0,
          keyword: ''
        }
        
        const response = await request.post('/api/proxy/sellMarket/front', searchParams)
        console.log('市场列表响应:', response.data)
        
        if (response.data.code === 200) {
          this.marketList = response.data.data || []
          console.log('设置市场列表数据:', this.marketList)
          this.$message.success('商品列表加载成功')
        } else {
          console.error('接口返回错误:', response.data)
          this.$message.error(response.data.message || '加载失败')
        }
      } catch (error) {
        console.error('加载市场列表失败:', error)
        this.$message.error('加载商品列表失败')
      } finally {
        this.loading = false
      }
    },
    

    
    viewMarketDetail(item) {
      this.$message.info(`查看市场详情: ${item.name}`)
      // 这里可以添加跳转到详情页面的逻辑
    },
    
    // 添加日志
    addLog(message, type = 'info') {
      const now = new Date()
      const time = now.toLocaleTimeString()
      this.purchaseLogs.unshift({
        time,
        message,
        type
      })
      // 限制日志数量，最多保留100条
      if (this.purchaseLogs.length > 100) {
        this.purchaseLogs = this.purchaseLogs.slice(0, 100)
      }
    },
    
    // 清空日志
    clearLogs() {
      this.purchaseLogs = []
    },
    
    // 检查是否可以抢购
    canPurchase(item) {
      // 这里可以根据时间、状态等条件判断是否可以抢购
      return true
    },
    
    // 获取抢购按钮文本
    getPurchaseButtonText(item) {
      if (item.purchasing) {
        const current = item.currentAttempt || 0
        const max = this.purchaseSettings.maxRetries
        return `抢购中... (${current}/${max})`
      }
      return '立即抢购'
    },
    
    // 生成签名（使用自定义的sign值）
    generateSign(id, password, timer) {
      // 使用自定义的sign值
      console.log('使用自定义签名值:', this.purchaseSign)
      return this.purchaseSign
    },
    
    
    // 显示抢购设置
    showPurchaseSettings() {
      this.settingsVisible = true
    },
    
    
    // 保存抢购设置
    savePurchaseSettings() {
      this.purchasePassword = this.purchaseSettings.password
      // sign值始终使用默认值，不允许用户修改
      this.purchaseSign = DEFAULT_SIGN
      this.settingsVisible = false
      this.addLog('抢购设置已保存', 'info')
      this.$message.success('设置已保存')
    },
    
    // 开始自动抢购 - 移动端优化版本
    async startAutoPurchase(item) {
      if (item.purchasing) {
        return
      }
      
      // 防抖处理，避免重复点击
      if (item._purchaseDebounce) {
        return
      }
      item._purchaseDebounce = true
      setTimeout(() => { item._purchaseDebounce = false }, 500)
      
      this.$set(item, 'purchasing', true)
      this.$set(item, 'currentAttempt', 0)
      this.addLog(`开始移动端优化抢购: ${item.name}`, 'info')
      
      // 立即提示用户，使用更友好的移动端提示
      this.$message({
        message: '抢购已启动，后台执行中...',
        type: 'info',
        duration: 2000,
        showClose: false
      })
      
      // 使用requestAnimationFrame优化性能
      requestAnimationFrame(() => {
        this.launchMobileOptimizedPurchase(item)
      })
      
      // 设置自动停止定时器（25秒后自动停止，避免长时间占用）
      setTimeout(() => {
        if (item.purchasing) {
          this.$set(item, 'purchasing', false)
          this.$set(item, 'currentAttempt', 0)
          this.addLog(`移动端抢购自动停止: ${item.name}`, 'warning')
        }
      }, 25000)
    },
    
    // 移动端优化的抢购启动
    async launchMobileOptimizedPurchase(item) {
      // 移动端减少线程数量，避免卡死
      const maxRetries = Math.min(this.purchaseSettings.maxRetries, 3)
      this.addLog(`移动端模式: 启动${maxRetries}个优化线程`, 'info')
      
      // 使用更大的间隔，减少手机负担
      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        if (!item.purchasing) {
          break
        }
        
        this.$set(item, 'currentAttempt', attempt)
        this.addLog(`启动移动端线程${attempt}...`, 'info')
        
        // 异步执行，针对移动端优化
        this.executeMobileOptimizedPurchase(item, attempt)
        
        // 移动端使用更大间隔，避免资源竞争
        if (attempt < maxRetries) {
          await this.sleep(100) // 100毫秒间隔，对移动端更友好
        }
      }
    },
    
    // 启动异步抢购线程（保留桌面端使用）
    async launchAsyncPurchaseThreads(item) {
      // 快速启动多个异步抢购线程
      for (let attempt = 1; attempt <= this.purchaseSettings.maxRetries; attempt++) {
        if (!item.purchasing) {
          break
        }
        
        this.$set(item, 'currentAttempt', attempt)
        this.addLog(`启动第${attempt}个异步线程...`, 'info')
        
        // 异步执行，不等待结果
        this.executeAsyncPurchase(item, attempt)
        
        // 快速启动下一个线程
        if (attempt < this.purchaseSettings.maxRetries) {
          await this.sleep(30) // 30毫秒间隔快速启动
        }
      }
    },
    
    // 移动端优化执行
    async executeMobileOptimizedPurchase(item, attempt) {
      try {
        const timer = Date.now()
        const sign = this.generateSign(item.id, this.purchasePassword, timer)
        
        const purchaseData = {
          id: `[${item.id}]`,
          password: this.purchasePassword,
          timer: timer,
          sign: sign
        }
        
        this.addLog(`移动端线程${attempt}发送请求`, 'info')
        
        // 移动端使用更短的超时时间，避免长时间等待
        const timeoutPromise = new Promise((_, reject) => {
          setTimeout(() => reject(new Error('移动端请求超时')), 3000)
        })
        
        const requestPromise = request.post('/api/proxy/sellMarket/smart', purchaseData)
        
        Promise.race([requestPromise, timeoutPromise])
          .then(response => {
            if (response.data && response.data.code === 200) {
              this.addLog(`移动端线程${attempt}成功！`, 'success')
              // 成功时立即停止其他线程
              if (item.purchasing) {
                this.$set(item, 'purchasing', false)
                this.$set(item, 'currentAttempt', 0)
                this.$message({
                  message: `抢购成功！(线程${attempt})`,
                  type: 'success',
                  duration: 3000
                })
              }
            } else {
              this.addLog(`移动端线程${attempt}失败: ${response.data?.message || '未知错误'}`, 'error')
            }
          })
          .catch(error => {
            this.addLog(`移动端线程${attempt}异常: ${error.message}`, 'error')
          })
        
      } catch (error) {
        this.addLog(`移动端线程${attempt}启动异常: ${error.message}`, 'error')
      }
    },
    
    // 异步执行单个抢购
    async executeAsyncPurchase(item, attempt) {
      try {
        const timer = Date.now()
        const sign = this.generateSign(item.id, this.purchasePassword, timer)
        
        const purchaseData = {
          id: `[${item.id}]`,
          password: this.purchasePassword,
          timer: timer,
          sign: sign
        }
        
        this.addLog(`线程${attempt}发送异步请求`, 'info')
        
        // 发起请求但不等待响应，让请求在后台执行
        request.post('/api/proxy/sellMarket/smart', purchaseData)
          .then(response => {
            if (response.data && response.data.code === 200) {
              this.addLog(`线程${attempt}抢购成功！`, 'success')
              // 成功时停止其他线程
              if (item.purchasing) {
                this.$set(item, 'purchasing', false)
                this.$set(item, 'currentAttempt', 0)
                this.$message.success(`抢购成功！(线程${attempt})`)
              }
            } else {
              this.addLog(`线程${attempt}响应失败: ${response.data?.message || '未知错误'}`, 'error')
            }
          })
          .catch(error => {
            this.addLog(`线程${attempt}请求异常: ${error.message}`, 'error')
          })
        
      } catch (error) {
        this.addLog(`线程${attempt}启动异常: ${error.message}`, 'error')
      }
    },
    
    // 单个抢购线程执行
    async executeSinglePurchase(item, attempt) {
      try {
        const timer = Date.now()
        const sign = this.generateSign(item.id, this.purchasePassword, timer)
        
        const purchaseData = {
          id: `[${item.id}]`,
          password: this.purchasePassword,
          timer: timer,
          sign: sign
        }
        
        this.addLog(`线程${attempt}发送抢购请求`, 'info')
        
        // 使用Promise.race实现超时控制
        const purchasePromise = request.post('/api/proxy/sellMarket/smart', purchaseData)
        const timeoutPromise = this.sleep(5000) // 5秒超时
        
        const response = await Promise.race([purchasePromise, timeoutPromise])
        
        if (response && response.data) {
          this.addLog(`线程${attempt}收到响应: ${response.data.code}`, 'info')
          
          if (response.data.code === 200) {
            this.addLog(`线程${attempt}抢购成功！`, 'success')
            return true
          } else {
            this.addLog(`线程${attempt}抢购失败: ${response.data.message}`, 'error')
          }
        } else {
          this.addLog(`线程${attempt}请求超时`, 'warning')
        }
        
        return false
      } catch (error) {
        this.addLog(`线程${attempt}异常: ${error.message}`, 'error')
        return false
      }
    },
    
    // 超级抢购 - 移动端优化版本
    async startSuperPurchase(item) {
      if (item.purchasing) {
        return
      }
      
      // 防抖处理
      if (item._superPurchaseDebounce) {
        return
      }
      item._superPurchaseDebounce = true
      setTimeout(() => { item._superPurchaseDebounce = false }, 1000)
      
      this.$set(item, 'purchasing', true)
      this.addLog(`开始移动端超级抢购: ${item.name}`, 'info')
      
      // 移动端友好提示
      this.$message({
        message: '极速抢购已启动！',
        type: 'warning',
        duration: 2000,
        showClose: false
      })
      
      try {
        const timer = Date.now()
        const sign = this.generateSign(item.id, this.purchasePassword, timer)
        
        const purchaseData = {
          product_id: item.id,
          password: this.purchasePassword,
          sign: sign,
          thread_count: this.purchaseSettings.superThreadCount
        }
        
        this.addLog(`发送异步超级抢购请求: ${purchaseData.thread_count}个线程`, 'info')
        
        // 异步发送请求，不等待响应
        request.post('/api/proxy/multi_purchase', purchaseData)
          .then(response => {
            if (response.data.code === 200) {
              const result = response.data.data
              if (result.success) {
                this.addLog(`超级抢购成功！`, 'success')
                this.addLog(`成功线程数: ${result.results.filter(r => r).length}/${result.thread_count}`, 'success')
                this.$message.success('超级抢购成功！')
              } else {
                this.addLog(`超级抢购失败，所有线程均失败`, 'error')
                this.$message.warning('超级抢购已完成，请查看日志')
              }
            } else {
              this.addLog(`超级抢购请求失败: ${response.data.message}`, 'error')
              this.$message.error(response.data.message || '超级抢购失败')
            }
            
            // 完成后停止状态
            this.$set(item, 'purchasing', false)
          })
          .catch(error => {
            console.error('超级抢购异常:', error)
            this.addLog(`超级抢购异常: ${error.message}`, 'error')
            this.$message.error('超级抢购异常')
            this.$set(item, 'purchasing', false)
          })
        
        // 设置自动停止定时器（60秒后自动停止）
        setTimeout(() => {
          if (item.purchasing) {
            this.$set(item, 'purchasing', false)
            this.addLog(`超级抢购自动停止: ${item.name} (60秒超时)`, 'warning')
          }
        }, 60000)
        
      } catch (error) {
        console.error('超级抢购启动失败:', error)
        this.addLog(`超级抢购启动异常: ${error.message}`, 'error')
        this.$message.error('超级抢购启动失败')
        this.$set(item, 'purchasing', false)
      }
    },
    
    // 停止抢购
    stopPurchase(item) {
      this.$set(item, 'purchasing', false)
      this.$set(item, 'currentAttempt', 0)
      this.addLog(`用户手动停止抢购: ${item.name}`, 'warning')
      this.addLog(`注意: 已发送的请求仍在后台执行`, 'info')
      this.$message.warning('抢购已停止，但已发送的请求仍在后台执行')
    },
    
    // 延时函数
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    
    // 单次抢购（保留原方法）
    async startPurchase(item) {
      if (item.purchasing) {
        return
      }
      
      this.$set(item, 'purchasing', true)
      this.addLog(`开始抢购商品: ${item.name}`, 'info')
      
      try {
        const timer = Date.now()
        const sign = this.generateSign(item.id, this.purchasePassword, timer)
        
        const purchaseData = {
          id: `[${item.id}]`,
          password: this.purchasePassword,
          timer: timer,
          sign: sign
        }
        
        this.addLog(`使用签名: ${this.purchaseSign}`, 'info')
        this.addLog(`发送抢购请求: ${JSON.stringify(purchaseData)}`, 'info')
        
        const response = await request.post('/api/proxy/sellMarket/smart', purchaseData)
        
        this.addLog(`抢购响应: ${JSON.stringify(response.data)}`, 'success')
        
        if (response.data.code === 200) {
          this.addLog(`抢购成功: ${item.name}`, 'success')
          this.$message.success('抢购成功！')
        } else {
          this.addLog(`抢购失败: ${response.data.message}`, 'error')
          this.$message.error(response.data.message || '抢购失败')
        }
      } catch (error) {
        console.error('抢购失败:', error)
        this.addLog(`抢购异常: ${error.message}`, 'error')
        this.$message.error('抢购失败，请重试')
      } finally {
        this.$set(item, 'purchasing', false)
      }
    }
  }
}
</script>

<style scoped>
.market-list-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
}

.page-header {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  margin: 20px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.market-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 20px 20px;
  -webkit-overflow-scrolling: touch;
}

/* 商品信息区域 */
.market-info-section {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.info-title i {
  color: #3b82f6;
  font-size: 20px;
}

.info-stats {
  font-size: 14px;
  color: #6b7280;
  background: #f3f4f6;
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: 500;
}

/* 响应式优化信息区域 */
@media (max-width: 768px) {
  .info-header {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .market-info-section {
    padding: 16px;
  }
}

.market-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.market-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
}

.market-card:hover {
  box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
  border-color: #3b82f6;
}

.market-header {
  position: relative;
  height: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  overflow: hidden;
}

.market-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.market-status {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  min-width: 60px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
}

.status-badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.status-up {
  background: rgba(16, 185, 129, 0.9);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.status-down {
  background: rgba(239, 68, 68, 0.9);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.market-info {
  padding: 24px;
  position: relative;
}

.market-name {
  margin: 0 0 20px 0;
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 50px;
}

.market-stats {
  margin-bottom: 20px;
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 8px 0;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.stat-label::before {
  content: '●';
  color: #3b82f6;
  margin-right: 6px;
  font-size: 12px;
}

.stat-value {
  font-size: 15px;
  color: #111827;
  font-weight: 700;
  font-family: 'Monaco', 'Menlo', monospace;
}

.stat-value.price {
  color: #10b981;
  font-size: 18px;
  text-shadow: 0 1px 2px rgba(16, 185, 129, 0.2);
}

.stat-value.max-price {
  color: #f59e0b;
  font-size: 16px;
}


.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}

.empty-state i {
  font-size: 64px;
  margin-bottom: 16px;
  display: block;
}

.empty-state p {
  margin: 0 0 20px 0;
  font-size: 16px;
}

/* 移动端适配 */
@media (max-width: 767px) {
  .market-list-page {
    background: white;
  }
  
  .page-header {
    margin: 16px;
    padding: 20px;
  }
  
  .page-header h2 {
    font-size: 18px;
  }
  
  .header-actions {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .market-content {
    padding: 0 16px 16px;
  }
  
  .market-info-section {
    margin-bottom: 16px;
  }
  
  .market-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .market-card {
    border-radius: 12px;
  }
  
  .market-info {
    padding: 20px;
  }
  
  .market-name {
    font-size: 18px;
    margin-bottom: 16px;
  }
  
  .market-stats {
    padding: 12px;
  }
  
  .stat-item {
    padding: 6px 0;
    margin-bottom: 8px;
  }
  
  .stat-label,
  .stat-value {
    font-size: 13px;
  }
  
  .purchase-buttons {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .purchase-btn {
    min-height: 80px;
    padding: 16px 12px;
    font-size: 16px;
    border-radius: 12px;
    /* 移动端触控优化 */
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
    user-select: none;
    -webkit-user-select: none;
  }
  
  .purchase-btn:active {
    transform: scale(0.98);
    transition: transform 0.1s ease;
  }
  
  .btn-content {
    margin-bottom: 6px;
  }
  
  .btn-text {
    font-size: 15px;
    font-weight: 700;
  }
  
  .btn-subtitle {
    font-size: 12px;
    opacity: 0.9;
  }
  
  .purchase-btn i {
    font-size: 20px;
  }
  
  /* 移动端抢购状态优化 */
  .purchasing-status {
    padding: 20px;
    border-radius: 12px;
  }
  
  .status-icon {
    width: 48px;
    height: 48px;
  }
  
  .status-icon i {
    font-size: 20px;
  }
  
  .status-title {
    font-size: 18px;
    margin-bottom: 6px;
  }
  
  .status-progress {
    font-size: 15px;
  }
  
  .stop-purchase {
    min-height: 50px;
    font-size: 16px;
    border-radius: 10px;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
  }
  
  .stop-purchase:active {
    transform: scale(0.98);
  }
}

@media (max-width: 480px) {
  .search-form {
    display: flex;
    flex-direction: column;
  }
  
  .search-form .el-form-item {
    margin-right: 0;
    margin-bottom: 12px;
  }
  
  .market-card {
    border-radius: 12px;
  }
  
  .market-header {
    height: 8px;
  }
  
  .market-info {
    padding: 16px;
  }
  
  .market-name {
    font-size: 16px;
    min-height: 48px;
  }
  
  /* 超小屏幕抢购按钮优化 */
  .purchase-section {
    margin-top: 20px;
    padding-top: 16px;
  }
  
  .purchase-buttons {
    gap: 16px;
  }
  
  .purchase-btn {
    min-height: 88px;
    padding: 20px 16px;
    font-size: 17px;
    border-radius: 16px;
    /* 加强触控反馈 */
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .purchase-btn:active {
    transform: scale(0.95);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }
  
  .btn-content {
    margin-bottom: 8px;
  }
  
  .btn-text {
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 0.5px;
  }
  
  .btn-subtitle {
    font-size: 13px;
    font-weight: 600;
    opacity: 0.95;
  }
  
  .purchase-btn i {
    font-size: 22px;
  }
  
  /* 抢购状态在超小屏幕的优化 */
  .purchasing-status {
    padding: 24px 20px;
    border-radius: 16px;
    border-width: 3px;
  }
  
  .status-header {
    margin-bottom: 20px;
    gap: 16px;
  }
  
  .status-icon {
    width: 52px;
    height: 52px;
  }
  
  .status-icon i {
    font-size: 22px;
  }
  
  .status-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 8px;
  }
  
  .status-progress {
    font-size: 16px;
    font-weight: 600;
  }
  
  .stop-purchase {
    min-height: 56px;
    font-size: 17px;
    font-weight: 700;
    border-radius: 12px;
    margin-top: 4px;
  }
  
  .stop-purchase:active {
    transform: scale(0.96);
  }
  
  .stop-purchase i {
    font-size: 18px;
    margin-right: 8px;
  }
}

/* 抢购日志样式 */
.purchase-logs {
  margin-top: 24px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: #fafafa;
}

.logs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #e4e7ed;
  background: #f5f7fa;
  border-radius: 8px 8px 0 0;
}

.logs-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.logs-content {
  max-height: 300px;
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

/* 抢购按钮区域 */
.purchase-section {
  margin-top: 24px;
  border-top: 1px solid #f3f4f6;
  padding-top: 20px;
}

.purchase-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.purchase-btn {
  border: none;
  border-radius: 12px;
  padding: 16px 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
  position: relative;
  overflow: hidden;
  text-align: center;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.purchase-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.purchase-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.purchase-btn:not(:disabled):active {
  transform: translateY(0);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.btn-text {
  font-weight: 700;
  font-size: 14px;
}

.btn-subtitle {
  font-size: 11px;
  opacity: 0.8;
  font-weight: 500;
}

.purchase-btn i {
  font-size: 18px;
}

/* 智能抢购按钮 */
.primary-purchase {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.primary-purchase:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
}

/* 极速抢购按钮 */
.super-purchase {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.super-purchase:hover {
  background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
}

/* 抢购状态显示 */
.purchasing-status {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 12px;
  padding: 16px;
  border: 2px solid #10b981;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.status-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.status-icon i {
  font-size: 18px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.status-text {
  flex: 1;
}

.status-title {
  font-weight: 700;
  color: #111827;
  font-size: 16px;
  margin-bottom: 4px;
}

.status-progress {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

/* 停止按钮 */
.stop-purchase {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  width: 100%;
  min-height: 40px;
}

.stop-purchase:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.stop-purchase i {
  margin-right: 6px;
}


.settings-tip {
  background: #f0f9ff;
  border: 1px solid #bae7ff;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  color: #1890ff;
  font-size: 14px;
}

.settings-tip i {
  margin-right: 8px;
  font-size: 16px;
}
</style>
