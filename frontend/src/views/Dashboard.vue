<template>
  <div class="dashboard">
    <!-- 移动端顶部导航栏 -->
    <div class="mobile-header" v-if="isMobile">
      <div class="mobile-header-content">
        <h1 class="app-title">抢购系统</h1>
        <button class="user-menu-btn" @click="showUserMenu = !showUserMenu">
          <i class="el-icon-user"></i>
        </button>
      </div>
      
      <!-- 用户菜单下拉 -->
      <div v-if="showUserMenu" class="user-menu-dropdown">
        <div class="user-info">
          <span>{{ user.phone }}</span>
        </div>
        <button @click="logout" class="logout-btn">
          <i class="el-icon-switch-button"></i>
          退出登录
        </button>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- 桌面端侧边栏 -->
      <aside v-if="!isMobile" class="desktop-sidebar">
        <div class="sidebar-header">
          <h1>抢购系统</h1>
        </div>
        
        <nav class="sidebar-nav">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="['nav-item', { active: activeTab === tab.key }]"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.label }}</span>
          </button>
        </nav>
        
        <div class="sidebar-footer">
          <div class="user-info">
            <i class="el-icon-user"></i>
            <span>{{ user.phone }}</span>
          </div>
          <button @click="logout" class="logout-btn">
            <i class="el-icon-switch-button"></i>
            退出登录
          </button>
        </div>
      </aside>

      <!-- 主内容区域 -->
      <main class="main-content">
        <!-- 移动端标签导航 -->
        <div v-if="isMobile" class="mobile-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="['tab-item', { active: activeTab === tab.key }]"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.label }}</span>
          </button>
        </div>

        <!-- 页面内容 -->
        <div class="page-content">
          <component :is="currentComponent"></component>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import Management from '../components/Management.vue'
import UserInfo from '../components/UserInfo.vue'
import MarketList from '../components/MarketList.vue'
import GoodsList from '../components/GoodsList.vue'
import Holdings from '../components/Holdings.vue'

export default {
  name: 'Dashboard',
  components: {
    Management,
    UserInfo,
    MarketList,
    GoodsList,
    Holdings
  },
  data() {
    return {
      activeTab: 'market',
      isMobile: false,
      showUserMenu: false,
      user: {},
      tabs: [
        { key: 'market', label: '市场', icon: 'el-icon-shopping-bag-1' },
        { key: 'goods', label: '商品', icon: 'el-icon-goods' },
        { key: 'holdings', label: '持仓', icon: 'el-icon-shopping-bag-1' },
        { key: 'management', label: '托管', icon: 'el-icon-s-tools' },
        { key: 'userinfo', label: '我的', icon: 'el-icon-user-solid' }
      ]
    }
  },
  computed: {
    currentComponent() {
      const componentMap = {
        'market': 'MarketList',
        'goods': 'GoodsList',
        'holdings': 'Holdings',
        'management': 'Management',
        'userinfo': 'UserInfo'
      }
      return componentMap[this.activeTab]
    }
  },
  mounted() {
    this.user = JSON.parse(localStorage.getItem('user') || '{}')
    this.checkScreenSize()
    window.addEventListener('resize', this.checkScreenSize)
    
    // 点击外部关闭用户菜单
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkScreenSize)
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    checkScreenSize() {
      this.isMobile = window.innerWidth < 768
    },
    
    handleClickOutside(event) {
      if (!event.target.closest('.mobile-header')) {
        this.showUserMenu = false
      }
    },
    
    logout() {
      this.$emit('logout')
    }
  }
}
</script>

<style scoped>
.dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
}

/* 移动端头部 */
.mobile-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  position: relative;
  z-index: 50;
}

.mobile-header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
}

.app-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.user-menu-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.user-menu-btn:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.user-menu-dropdown {
  position: absolute;
  top: 100%;
  right: 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  z-index: 60;
}

.user-menu-dropdown .user-info {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
  color: #374151;
}

.logout-btn {
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: none;
  text-align: left;
  color: #ef4444;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #fef2f2;
}

/* 主要内容布局 */
.dashboard-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 桌面端侧边栏 */
.desktop-sidebar {
  width: 240px;
  background: white;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid #f3f4f6;
}

.sidebar-header h1 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
}

.nav-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  background: none;
  border-radius: 8px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 4px;
  font-size: 14px;
  font-weight: 500;
}

.nav-item:hover {
  background: #f3f4f6;
  color: #374151;
}

.nav-item.active {
  background: #eff6ff;
  color: #3b82f6;
}

.nav-item i {
  font-size: 18px;
  width: 20px;
  text-align: center;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #f3f4f6;
}

.sidebar-footer .user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 12px;
}

.sidebar-footer .logout-btn {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-footer .logout-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 移动端标签导航 */
.mobile-tabs {
  display: flex;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.tab-item {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  border: none;
  background: none;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.tab-item:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: transparent;
  transition: background 0.2s;
}

.tab-item.active {
  color: #3b82f6;
}

.tab-item.active:after {
  background: #3b82f6;
}

.tab-item i {
  font-size: 20px;
}

.tab-item span {
  font-size: 12px;
  font-weight: 500;
}

/* 页面内容 */
.page-content {
  flex: 1;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
}

/* 移动端适配 */
@media (max-width: 767px) {
  .desktop-sidebar {
    display: none;
  }
}

@media (min-width: 768px) {
  .mobile-header,
  .mobile-tabs {
    display: none;
  }
}
</style>