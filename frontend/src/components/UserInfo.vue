<template>
  <div class="userinfo-page">
    <div class="page-header">
      <h2>用户信息</h2>
      <el-button @click="loadUserInfo" icon="el-icon-refresh">刷新</el-button>
    </div>

    <div class="userinfo-content">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon balance">
            <i class="el-icon-wallet"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">¥{{ userInfo.money || '0.00' }}</div>
            <div class="stat-label">账户余额</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon profit">
            <i class="el-icon-coin"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ userInfo.score || '0.00' }}</div>
            <div class="stat-label">平台积分</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon orders">
            <i class="el-icon-shopping-bag-1"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ userInfo.level || 0 }}</div>
            <div class="stat-label">用户等级</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon phone">
            <i class="el-icon-phone"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ userInfo.mobile || '--' }}</div>
            <div class="stat-label">手机号</div>
          </div>
        </div>
      </div>

      <div class="user-details">
        <h3>用户详情</h3>
        <div class="details-grid">
          <div class="detail-item">
            <span class="detail-label">用户ID:</span>
            <span class="detail-value">{{ userInfo.user_id || '--' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">昵称:</span>
            <span class="detail-value">{{ userInfo.nickname || '--' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">邀请码:</span>
            <span class="detail-value">{{ userInfo.invite_code || '--' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">团队等级:</span>
            <span class="detail-value">{{ userInfo.team_level || 0 }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">交易状态:</span>
            <span class="detail-value">
              <el-tag :type="userInfo.trade_status === 1 ? 'success' : 'danger'">
                {{ userInfo.trade_status === 1 ? '正常' : '禁用' }}
              </el-tag>
            </span>
          </div>
          <div class="detail-item">
            <span class="detail-label">系统状态:</span>
            <span class="detail-value">
              <el-tag :type="userInfo.sys_status === '1' ? 'success' : 'danger'">
                {{ userInfo.sys_status === '1' ? '正常' : '禁用' }}
              </el-tag>
            </span>
          </div>
        </div>
      </div>





      <div class="info-section">
        <p class="update-time">
          最后更新: {{ formatDate(userInfo.updated_at) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import request from '../utils/request'

export default {
  name: 'UserInfo',
  data() {
    return {
      userInfo: {
        money: '0.00',
        score: '0.00',
        level: 0,
        mobile: '',
        user_id: '',
        nickname: '',
        invite_code: '',
        team_level: 0,
        trade_status: 0,
        sys_status: '0'
      },
      user: {}
    }
  },
  mounted() {
    this.user = JSON.parse(localStorage.getItem('user') || '{}')
    this.loadUserInfo()
  },

  methods: {
    async loadUserInfo() {
      try {
        const response = await request.post('/api/GetUserInfo', {})
        
        if (response.data.code === 200) {
          this.userInfo = response.data.data
        } else {
          this.$message.error('加载用户信息失败')
        }
      } catch (error) {
        this.$message.error('加载用户信息失败')
      }
    },
    

    
    formatDate(dateString) {
      if (!dateString) return '暂无数据'
      return new Date(dateString).toLocaleString('zh-CN')
    }
  }
}
</script>

<style scoped>
.userinfo-page {
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

.userinfo-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  -webkit-overflow-scrolling: touch;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: box-shadow 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stat-icon {
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

.stat-icon.balance {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.stat-icon.profit {
  background: linear-gradient(135deg, #10b981, #047857);
}

.stat-icon.profit.negative {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.stat-icon.orders {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.stat-icon.phone {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
  word-break: break-all;
}

.stat-value.positive {
  color: #10b981;
}

.stat-value.negative {
  color: #ef4444;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.info-section {
  text-align: center;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.update-time {
  margin: 0;
  font-size: 12px;
  color: #9ca3af;
}

.user-details {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.user-details h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.detail-value {
  color: #6b7280;
  font-size: 14px;
  text-align: right;
}

/* 移动端适配 */
@media (max-width: 767px) {
  .page-header {
    padding: 16px;
  }
  
  .page-header h2 {
    font-size: 18px;
  }
  
  .userinfo-content {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    margin-bottom: 24px;
  }
  
  .stat-card {
    padding: 16px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .user-details {
    padding: 16px;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .detail-item {
    padding: 8px 0;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    gap: 12px;
  }
  
  .stat-card {
    padding: 12px;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
  
  .stat-value {
    font-size: 18px;
  }
  
  .stat-label {
    font-size: 12px;
  }
}
</style>