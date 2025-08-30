<template>
  <div class="goods-list-page">
    <div class="page-header">
      <h2>商品抢购</h2>
      <el-button @click="loadGoodsList" icon="el-icon-refresh" :loading="loading">刷新</el-button>
    </div>

    <div class="goods-content">
      <!-- 商品列表 -->
      <div class="goods-grid">
        <div 
          v-for="item in goodsList" 
          :key="item.id" 
          class="goods-card"
          @click="viewGoodsDetail(item)"
        >
          <div class="goods-header">
            <div class="goods-status">
              <span 
                :class="['status-badge', `status-${getStatusType(item)}`]"
              >
                {{ getStatusText(item) }}
              </span>
            </div>
          </div>
          
          <div class="goods-info">
            <h3 class="goods-name">{{ item.name }}</h3>
            <div class="goods-stats">
              <div class="stat-item">
                <span class="stat-label">价格:</span>
                <span class="stat-value price">¥{{ item.money }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">库存:</span>
                <span class="stat-value stock">{{ item.stock }}/{{ item.all_stock }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">商品ID:</span>
                <span class="stat-value">{{ item.id }}</span>
              </div>
            </div>
            
            <div class="goods-time">
              <div class="time-item">
                <i class="el-icon-time"></i>
                <span>开始: {{ formatTime(item.start_time) }}</span>
              </div>
              <div class="time-item">
                <i class="el-icon-time"></i>
                <span>结束: {{ formatTime(item.end_time) }}</span>
              </div>
              <div class="time-item">
                <i class="el-icon-time"></i>
                <span>运行: {{ formatTime(item.run_time) }}</span>
              </div>
              <div class="time-item">
                <i class="el-icon-time"></i>
                <span>支付截止: {{ formatTime(item.pay_limit) }}</span>
              </div>
            </div>

            <div class="goods-actions">
              <el-button 
                type="primary" 
                size="small" 
                :disabled="!canPurchase(item)"
                @click.stop="purchaseGoods(item)"
              >
                {{ getActionText(item) }}
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="goodsList.length === 0 && !loading" class="empty-state">
        <i class="el-icon-shopping-bag-1"></i>
        <p>暂无商品数据</p>
        <el-button type="primary" @click="loadGoodsList">重新加载</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import request from '../utils/request'

export default {
  name: 'GoodsList',
  data() {
    return {
      loading: false,
      goodsList: []
    }
  },
  mounted() {
    this.loadGoodsList()
  },
  methods: {
    async loadGoodsList() {
      try {
        this.loading = true
        console.log('开始加载商品列表')
        
        const response = await request.post('/api/proxy/goods/list', {})
        console.log('商品列表响应:', response.data)
        
        if (response.data.code === 200) {
          this.goodsList = response.data.data || []
          console.log('设置商品列表数据:', this.goodsList)
          this.$message.success('商品列表加载成功')
        } else {
          console.error('接口返回错误:', response.data)
          this.$message.error(response.data.message || '加载失败')
        }
      } catch (error) {
        console.error('加载商品列表失败:', error)
        this.$message.error('加载商品列表失败')
      } finally {
        this.loading = false
      }
    },
    
    formatTime(timeString) {
      if (!timeString) return '--'
      return timeString.replace('2025-08-11 ', '')
    },
    
    getStatusType(item) {
      const now = new Date().getTime() / 1000
      const start = item.start
      const end = item.end
      const run = item.run
      
      if (now < start) return 'warning' // 未开始
      if (now >= start && now < end) return 'success' // 进行中
      if (now >= end && now < run) return 'info' // 已结束，等待运行
      return 'danger' // 已运行
    },
    
    getStatusText(item) {
      const now = new Date().getTime() / 1000
      const start = item.start
      const end = item.end
      const run = item.run
      
      if (now < start) return '未开始'
      if (now >= start && now < end) return '抢购中'
      if (now >= end && now < run) return '等待运行'
      return '已结束'
    },
    
    canPurchase(item) {
      const now = new Date().getTime() / 1000
      const start = item.start
      const end = item.end
      
      return now >= start && now < end && item.stock > 0
    },
    
    getActionText(item) {
      if (!this.canPurchase(item)) {
        if (item.stock <= 0) return '已售罄'
        return '不可购买'
      }
      return '立即抢购'
    },
    
    purchaseGoods(item) {
      this.$message.info(`抢购商品: ${item.name}`)
      // 这里可以添加抢购逻辑
    },
    
    viewGoodsDetail(item) {
      this.$message.info(`查看商品详情: ${item.name}`)
      // 这里可以添加跳转到详情页面的逻辑
    }
  }
}
</script>

<style scoped>
.goods-list-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid #f3f4f6;
  flex-shrink: 0;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.goods-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  -webkit-overflow-scrolling: touch;
}

.goods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.goods-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
  cursor: pointer;
}

.goods-card:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.goods-header {
  position: relative;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
}

.goods-status {
  position: static;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  min-width: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.status-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.status-info {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
}

.status-danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.goods-info {
  padding: 20px;
}

.goods-name {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.goods-stats {
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-size: 14px;
  color: #111827;
  font-weight: 600;
}

.stat-value.price {
  color: #10b981;
}

.stat-value.stock {
  color: #f59e0b;
}

.goods-time {
  border-top: 1px solid #f3f4f6;
  padding-top: 16px;
  margin-bottom: 16px;
}

.time-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #6b7280;
}

.time-item:last-child {
  margin-bottom: 0;
}

.time-item i {
  margin-right: 8px;
  font-size: 16px;
}

.goods-actions {
  border-top: 1px solid #f3f4f6;
  padding-top: 16px;
  text-align: center;
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
  .page-header {
    padding: 16px;
  }
  
  .page-header h2 {
    font-size: 18px;
  }
  
  .goods-content {
    padding: 16px;
  }
  
  .goods-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .goods-header {
    height: 50px;
  }
  
  .goods-info {
    padding: 16px;
  }
  
  .goods-name {
    font-size: 16px;
    margin-bottom: 12px;
  }
  
  .stat-item {
    margin-bottom: 6px;
  }
  
  .stat-label,
  .stat-value {
    font-size: 13px;
  }
  
  .time-item {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .goods-card {
    border-radius: 8px;
  }
  
  .goods-header {
    height: 45px;
  }
  
  .goods-info {
    padding: 12px;
  }
  
  .goods-name {
    font-size: 15px;
  }
}
</style>
