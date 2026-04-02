<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { getAuthUser, logout } from './utils/auth'

const route = useRoute()
const router = useRouter()
const currentUser = ref(getAuthUser())
const isSidebarVisible = ref(true)

const pageTitles = {
  login: '登录',
  dashboard: '农场情况',
  control: '我的农场',
  learning: '趣味学习',
  home: '首页',
  about: '关于',
}

const currentPageTitle = computed(() => pageTitles[route.name] || '智慧农业')
const isLoginPage = computed(() => route.name === 'login')
const isLoggedIn = computed(() => !!currentUser.value)
const displayName = computed(() => currentUser.value?.displayName || 'admin')

watch(
  () => route.fullPath,
  () => {
    currentUser.value = getAuthUser()
  },
)

const handleLogout = () => {
  logout()
  currentUser.value = null
  router.replace('/login')
}

const toggleSidebar = () => {
  isSidebarVisible.value = !isSidebarVisible.value
}
</script>

<template>
  <RouterView v-if="isLoginPage" />
  <div v-else class="app">
    <aside class="sidebar" v-show="isSidebarVisible" aria-label="主导航">
      <div class="sidebar-header">
        <div class="brand">
          <div class="brand-text">
            <span class="brand-name">智慧农业</span>
          </div>
        </div>
        <button type="button" class="sidebar-collapse-btn" @click="toggleSidebar" aria-label="收起侧边栏">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 18l-6-6 6-6" />
          </svg>
          <span></span>
        </button>
      </div>

      <nav class="sidebar-nav">
        <RouterLink to="/" class="nav-link" active-class="nav-link--active">
          <span>首页</span>
        </RouterLink>
        <RouterLink to="/dashboard" class="nav-link" active-class="nav-link--active">
          <span>农场情况</span>
        </RouterLink>
        <RouterLink to="/control" class="nav-link" active-class="nav-link--active">
          <span>我的农场</span>
        </RouterLink>
        <RouterLink to="/learning" class="nav-link" active-class="nav-link--active">
          <span>趣味学习</span>
        </RouterLink>
      </nav>

      <div class="sidebar-bottom">
        <div class="user-info">
          <span class="username">{{ displayName }}</span>
        </div>
        <button v-if="isLoggedIn" type="button" class="logout-btn" @click="handleLogout">
          <span class="nav-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
          </span>
          <span>退出登录</span>
        </button>
      </div>
    </aside>

    <div
      class="main-content"
      :class="{ 'sidebar-visible': isSidebarVisible, 'sidebar-hidden': !isSidebarVisible }"
    >
      <main class="content-area">
        <button v-if="!isSidebarVisible" type="button" class="sidebar-expand-btn" @click="toggleSidebar" aria-label="展开侧边栏">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18l6-6-6-6" />
          </svg>
          <span>展开侧边栏</span>
        </button>
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app {
  --sf-green: #0f5132;
  --sf-green-mid: #25c18f;
  --sf-green-soft: #c7efdf;
  --sf-surface: #f2f5f4;
  display: flex;
  min-height: 100vh;
  font-family:
    'Segoe UI',
    system-ui,
    -apple-system,
    sans-serif;
  color: #1a2e24;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  display: flex;
  flex-direction: column;
  width: 252px;
  max-width: 50vw;
  height: 100vh;
  padding: 1.5rem 1rem 1rem;
  box-sizing: border-box;
  background: #ffffff;
  border-right: 1px solid #e0e0e0;
  box-shadow: 4px 0 32px rgba(0, 0, 0, 0.08);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
  padding: 0 0.35rem;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: var(--sf-green-mid);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(37, 193, 143, 0.3);
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.brand-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: #000000;
  letter-spacing: 0.02em;
}

.brand-sub {
  font-size: 0.72rem;
  font-weight: 600;
  color: #666666;
  margin-top: 2px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.sidebar-collapse-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  align-items: center;
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.75);
  color: var(--sf-green-mid);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
  z-index: 10;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.sidebar-nav span {
  font-weight: 400;
  font-size: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.7rem 0.9rem;
  border-radius: 12px;
  text-decoration: none;
  color: #000000;
  font-weight: 600;
  font-size: 0.95rem;
  border: 1px solid transparent;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease;
}

.nav-link:hover {
  background: #f5f5f5;
  border-color: #e0e0e0;
}

.nav-link--active {
  background: var(--sf-green-mid);
  color: #ffffff;
  border-color: var(--sf-green-mid);
  box-shadow: 0 4px 12px rgba(37, 193, 143, 0.3);
}

.nav-link--active:hover {
  background: var(--sf-green-mid);
  color: #ffffff;
  border-color: var(--sf-green-mid);
}

.nav-icon {
  display: flex;
  opacity: 0.9;
}

.sidebar-bottom {
  padding-top: 30px;
  border-top: 1px solid #e0e0e0;
}

.user-info {
  padding: 0 0.9rem 1rem;
}

.username {
  font-size: 0.9rem;
  font-weight: 600;
  color: #000000;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  width: 100%;
  padding: 0.7rem 0.9rem;
  border: none;
  border-radius: 12px;
  background: #000000;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-bottom: 1rem;
}

.logout-btn:hover {
  background: #333333;
}

.sidebar-foot {
  font-size: 0.68rem;
  color: #999999;
  padding: 0 0.5rem;
  line-height: 1.4;
}

.main-content {
  flex: 1;
  margin-left: 252px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0;
  background: var(--sf-surface);
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1.5rem;
  background: linear-gradient(90deg, #157347 0%, #1e7e4a 42%, #2d9d5f 100%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 4px 20px rgba(21, 115, 71, 0.25);
  color: #fff;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
}

.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  border: none;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  cursor: pointer;
  transition: background 0.2s ease;
}

.sidebar-toggle:hover {
  background: rgba(255, 255, 255, 0.22);
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: 0.02em;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.welcome-text {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.92);
  font-weight: 500;
}

.login-btn {
  padding: 0.45rem 1rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  border: 2px solid rgba(255, 255, 255, 0.85);
  background: transparent;
  color: #fff;
}

.login-btn:not(.logged-in) {
  background: #e85d4c;
  border-color: #e85d4c;
  color: #fff;
}

.login-btn.logged-in {
  background: #fff;
  color: #157347;
  border-color: #fff;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.content-area {
  flex: 1;
  padding: 1.35rem 1.5rem 2rem;
  overflow-y: auto;
}

.sidebar-expand-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 1.2rem;
  border: none;
  border-radius: 12px;
  background: var(--sf-green-mid);
  color: #ffffff;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(37, 193, 143, 0.3);
}

.sidebar-expand-btn:hover {
  background: #1db882;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(37, 193, 143, 0.4);
}

.main-content.sidebar-hidden {
  margin-left: 0;
}

@media (max-width: 900px) {
  .sidebar {
    width: 220px;
  }

  .main-content {
    margin-left: 220px;
  }
}

@media (max-width: 640px) {
  .sidebar {
    width: 100%;
    max-width: min(280px, 88vw);
  }

  .main-content.sidebar-visible {
    margin-left: 0;
  }

  .welcome-text {
    display: none;
  }

  .content-area {
    padding: 1rem;
  }
}
</style>
