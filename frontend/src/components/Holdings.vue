<template>
  <div class="holdings-page">
    <div class="page-header">
      <h2>我的持仓</h2>
      <el-button @click="loadHoldings" icon="el-icon-refresh" :loading="loading">刷新</el-button>
    </div>

    <div class="holdings-content">
      <!-- 持仓统计 -->
      <div class="holdings-summary">
        <div class="summary-card">
          <div class="summary-icon total-value">
            <i class="el-icon-money"></i>
          </div>
          <div class="summary-content">
            <div class="summary-value">¥{{ totalHoldingsValue }}</div>
            <div class="summary-label">持仓总金额</div>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon total-count">
            <i class="el-icon-shopping-bag-1"></i>
          </div>
          <div class="summary-content">
            <div class="summary-value">{{ totalHoldingsCount }}</div>
            <div class="summary-label">持仓总数量</div>
          </div>
        </div>

        <div class="summary-card">
          <div class="summary-icon total-items">
            <i class="el-icon-goods"></i>
          </div>
          <div class="summary-content">
            <div class="summary-value">{{ holdingsList.length }}</div>
            <div class="summary-label">持仓商品类型</div>
          </div>
        </div>
      </div>

      <!-- 持仓列表 -->
      <div class="holdings-list">
        <div 
          v-for="item in holdingsList" 
          :key="item.goods_id" 
          class="holding-card"
        >
          <div class="holding-header">
            <div class="holding-name">{{ item.goods.name }}</div>
            <div class="holding-status">
              <span 
                :class="['status-badge', item.goods.is_rise === '1' ? 'status-up' : 'status-down']"
              >
                {{ item.goods.is_rise === '1' ? '上涨' : '下跌' }}
              </span>
            </div>
          </div>
          
          <div class="holding-details">
            <div class="detail-row">
              <div class="detail-item">
                <span class="detail-label">商品ID:</span>
                <span class="detail-value">{{ item.goods_id }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">商品类型:</span>
                <span class="detail-value">{{ item.goods.type === '1' ? '可交易' : '不可交易' }}</span>
              </div>
            </div>
            
            <div class="detail-row">
              <div class="detail-item">
                <span class="detail-label">持仓数量:</span>
                <span class="detail-value count">{{ item.count }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">市场最高价:</span>
                <span class="detail-value price">¥{{ getMaxPrice(item) }}</span>
              </div>
            </div>
            
            <div class="detail-row">
              <div class="detail-item">
                <span class="detail-label">持仓总价:</span>
                <span class="detail-value total-price">¥{{ (item.count * parseFloat(item.goods.money)).toFixed(2) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">市场状态:</span>
                <span class="detail-value">{{ item.goods.is_market === '1' ? '可上市' : '不可上市' }}</span>
              </div>
            </div>
          </div>


        </div>
      </div>

      <!-- 持仓日收益 -->
      <div class="daily-profit-section">
        <h3>持仓日收益</h3>
        <div class="profit-summary">
          <div class="profit-card">
            <div class="profit-icon">
              <i class="el-icon-money"></i>
            </div>
            <div class="profit-content">
              <div class="profit-value">¥{{ totalDailyProfit }}</div>
              <div class="profit-label">今日总收益</div>
            </div>
          </div>
          
          <div class="profit-card">
            <div class="profit-icon">
              <i class="el-icon-trends-charts"></i>
            </div>
            <div class="profit-content">
              <div class="profit-value">{{ totalDailyProfitRate }}%</div>
              <div class="profit-label">日收益率</div>
            </div>
          </div>
        </div>
        
        <div class="profit-details">
          <div class="detail-header">
            <span>收益明细</span>
            <small>最高限价×2%×70%×数量</small>
          </div>
          <div class="profit-list">
            <div 
              v-for="item in holdingsList" 
              :key="item.goods_id" 
              class="profit-item"
            >
              <div class="profit-item-info">
                <div class="item-name">{{ item.goods.name }}</div>
                <div class="item-details">
                  <span class="detail-text">持仓: {{ item.count }}张</span>
                  <span class="detail-text">最高价: ¥{{ getMaxPrice(item) }}</span>
                  <span class="detail-text">日收益: ¥{{ getDailyProfit(item) }}</span>
                </div>
              </div>
              <div class="profit-item-status">
                <span 
                  :class="['status-badge', item.goods.is_rise === '1' ? 'status-up' : 'status-down']"
                >
                  {{ item.goods.is_rise === '1' ? '上涨' : '下跌' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="holdingsList.length === 0 && !loading" class="empty-state">
        <i class="el-icon-shopping-bag-1"></i>
        <p>暂无持仓数据</p>
        <small>数据长度: {{ holdingsList.length }}, 加载状态: {{ loading }}</small>
        <el-button type="primary" @click="loadHoldings">重新加载</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import request from '../utils/request'

export default {
  name: 'Holdings',
  data() {
    return {
      loading: false,
      holdingsList: [],
      marketData: {} // 存储市场数据，key为商品ID，value为市场信息
    }
  },
  mounted() {
    this.loadHoldings()
    this.loadMarketData()
    // 添加测试数据用于调试
    console.log('组件已挂载，开始加载数据')
  },
  computed: {
    totalHoldingsValue() {
      return this.holdingsList.reduce((total, item) => {
        return total + (item.count * parseFloat(item.goods.money))
      }, 0).toFixed(2)
    },
    totalHoldingsCount() {
      return this.holdingsList.reduce((total, item) => {
        return total + item.count
      }, 0)
    },
    totalDailyProfit() {
      return this.holdingsList.reduce((total, item) => {
        return total + parseFloat(this.getDailyProfit(item))
      }, 0).toFixed(2)
    },
    totalDailyProfitRate() {
      const totalValue = parseFloat(this.totalHoldingsValue)
      if (totalValue === 0) return '0.00'
      const totalProfit = parseFloat(this.totalDailyProfit)
      return ((totalProfit / totalValue) * 100).toFixed(2)
    }
  },
  methods: {
    async loadHoldings() {
      try {
        this.loading = true
        console.log('开始加载持仓数据')
        
        const response = await request.post('/api/proxy/my_nft_front', {})
        console.log('持仓数据响应:', response.data)
        
        if (response.data.code === 200) {
          this.holdingsList = response.data.data || []
          console.log('设置持仓数据:', this.holdingsList)
          console.log('持仓数据长度:', this.holdingsList.length)
          this.$message.success('持仓数据加载成功')
        } else {
          console.error('接口返回错误:', response.data)
          this.$message.error(response.data.message || '加载失败')
        }
      } catch (error) {
        console.error('加载持仓数据失败:', error)
        this.$message.error('加载持仓数据失败')
      } finally {
        this.loading = false
      }
    },
    
    async loadMarketData() {
      try {
        console.log('开始加载市场数据')
        
        const response = await request.post('/api/proxy/sellMarket/front', {
          price: 1,
          type: 0,
          cate_id: 0,
          keyword: ''
        })
        console.log('市场数据响应:', response.data)
        
        if (response.data.code === 200) {
          // 将市场数据转换为以商品ID为key的对象
          const marketList = response.data.data || []
          const marketMap = {}
          marketList.forEach(market => {
            marketMap[market.id] = market
          })
          this.marketData = marketMap
          console.log('设置市场数据:', this.marketData)
        } else {
          console.error('市场数据接口返回错误:', response.data)
        }
      } catch (error) {
        console.error('加载市场数据失败:', error)
      }
    },
    
    getMaxPrice(item) {
      // 从市场数据中获取最高价
      const marketInfo = this.marketData[item.goods_id]
      if (marketInfo && marketInfo.price_max) {
        return parseFloat(marketInfo.price_max)
      }
      // 如果没有市场数据，使用默认价格
      return 686.33
    },
    
    getDailyProfit(item) {
      // 日收益算法：今日藏品最高限价×0.02×0.7×藏品数量
      const maxPrice = this.getMaxPrice(item)
      const count = item.count
      const dailyRate = 0.02 // 2%
      const afterFeeRate = 0.7 // 70%（扣除30%手续费后）
      
      // 计算：最高限价 × 0.02 × 0.7 × 藏品数量
      const profit = maxPrice * dailyRate * afterFeeRate * count
      return profit.toFixed(2)
    },
    

  }
}
</script>

<style scoped>
.holdings-page {
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

.holdings-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  -webkit-overflow-scrolling: touch;
}

/* 持仓统计 */
.holdings-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.summary-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: box-shadow 0.2s;
}

.summary-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.summary-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
  flex-shrink: 0;
}

.summary-icon.total-value {
  background: linear-gradient(135deg, #10b981, #059669);
}

.summary-icon.total-count {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.summary-icon.total-items {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.summary-content {
  flex: 1;
  min-width: 0;
}

.summary-value {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
}

.summary-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

/* 持仓列表 */
.holdings-list {
  space-y: 16px;
}

.holding-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s ease;
}

.holding-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.holding-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.holding-name {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  line-height: 1.4;
  flex: 1;
  margin-right: 16px;
}

.holding-status {
  flex-shrink: 0;
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

.status-up {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.status-down {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.holding-details {
  margin-bottom: 16px;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 12px;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.detail-value {
  font-size: 14px;
  color: #111827;
  font-weight: 600;
}

.detail-value.count {
  color: #3b82f6;
}

.detail-value.price {
  color: #10b981;
}

.detail-value.total-price {
  color: #f59e0b;
}



  /* 持仓日收益 */
  .daily-profit-section {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
  }

  .daily-profit-section h3 {
    margin: 0 0 20px 0;
    font-size: 18px;
    font-weight: 600;
    color: #111827;
  }

  .profit-summary {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
  }

  .profit-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: box-shadow 0.2s;
  }

  .profit-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .profit-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: white;
    flex-shrink: 0;
  }

  .profit-icon:first-child {
    background: linear-gradient(135deg, #10b981, #059669);
  }

  .profit-icon:last-child {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
  }

  .profit-content {
    flex: 1;
    min-width: 0;
  }

  .profit-value {
    font-size: 24px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 4px;
  }

  .profit-label {
    font-size: 14px;
    color: #6b7280;
    font-weight: 500;
  }

  .profit-details {
    border-top: 1px solid #f3f4f6;
    padding-top: 20px;
  }

  .detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .detail-header span {
    font-size: 16px;
    font-weight: 600;
    color: #111827;
  }

  .detail-header small {
    font-size: 12px;
    color: #6b7280;
  }

  .profit-list {
    space-y: 12px;
  }

  .profit-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
  }

  .profit-item:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .profit-item:last-child {
    margin-bottom: 0;
  }

  .profit-item-info {
    flex: 1;
    min-width: 0;
  }

  .item-name {
    font-size: 16px;
    font-weight: 600;
    color: #111827;
    margin-bottom: 8px;
    word-break: break-all;
  }

  .item-details {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  .detail-text {
    font-size: 14px;
    color: #6b7280;
  }

  .profit-item-status {
    flex-shrink: 0;
    margin-left: 16px;
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
  
  .holdings-content {
    padding: 16px;
  }
  
  .holdings-summary {
    grid-template-columns: 1fr;
    gap: 16px;
    margin-bottom: 24px;
  }
  
  .summary-card {
    padding: 16px;
  }
  
  .summary-value {
    font-size: 20px;
  }
  
  .holding-card {
    padding: 16px;
  }
  
  .holding-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .holding-name {
    margin-right: 0;
    font-size: 16px;
  }
  
  .detail-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  

  
  .daily-profit-section {
    padding: 16px;
  }
  
  .profit-summary {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .profit-card {
    padding: 16px;
  }
  
  .profit-value {
    font-size: 20px;
  }
  
  .profit-item {
    padding: 12px;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .profit-item-status {
    margin-left: 0;
    margin-top: 12px;
  }
  
  .item-details {
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .holdings-summary {
    gap: 12px;
  }
  
  .summary-card {
    padding: 12px;
  }
  
  .summary-icon {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
  
  .summary-value {
    font-size: 18px;
  }
  
  .summary-label {
    font-size: 12px;
  }
  
  .holding-card {
    padding: 12px;
  }
  
  .holding-name {
    font-size: 15px;
  }
}
</style>
