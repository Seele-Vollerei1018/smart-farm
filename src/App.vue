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
  dashboard: '仪表盘',
  control: '设备控制',
  learning: '学习园地',
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
      <div class="brand">
        <span class="brand-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 3v18M8 9c0-2 2-4 4-4s4 2 4 4" />
            <path d="M6 15c2-3 5-4 6-4s4 1 6 4" />
          </svg>
        </span>
        <div class="brand-text">
          <span class="brand-name">智慧农业</span>
          <span class="brand-sub">监测系统</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <RouterLink to="/dashboard" class="nav-link" active-class="nav-link--active">
          <span class="nav-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="9" />
              <path d="M12 7v5l3 2" />
            </svg>
          </span>
          <span>仪表盘</span>
        </RouterLink>
        <RouterLink to="/control" class="nav-link" active-class="nav-link--active">
          <span class="nav-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>
          </span>
          <span>设备控制</span>
        </RouterLink>
        <RouterLink to="/learning" class="nav-link" active-class="nav-link--active">
          <span class="nav-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 6h16M4 10h16M4 14h10M4 18h8" />
              <path d="M18 14l2 2-2 2" />
            </svg>
          </span>
          <span>学习园地</span>
        </RouterLink>
      </nav>

      <p class="sidebar-foot">原型数据 · 可对接后端 API</p>
    </aside>

    <div
      class="main-content"
      :class="{ 'sidebar-visible': isSidebarVisible, 'sidebar-hidden': !isSidebarVisible }"
    >
      <header class="top-bar">
        <div class="left-section">
          <button type="button" class="sidebar-toggle" @click="toggleSidebar" aria-label="切换侧边栏">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 class="page-title">{{ currentPageTitle }}</h1>
        </div>
        <div class="user-section">
          <span v-if="isLoggedIn" class="welcome-text">欢迎，{{ displayName }}</span>
          <button v-if="isLoggedIn" type="button" class="login-btn logged-in" @click="handleLogout">
            退出
          </button>
        </div>
      </header>

      <main class="content-area">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app {
  --sf-green: #0f5132;
  --sf-green-mid: #198754;
  --sf-green-soft: #d1e7dd;
  --sf-surface: #f4f7f5;
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
  height: 100vh;
  padding: 1.5rem 1rem 1rem;
  box-sizing: border-box;
  background: linear-gradient(165deg, #ecfdf3 0%, #d8f3dc 45%, #b7e4c7 100%);
  border-right: 1px solid rgba(15, 81, 50, 0.12);
  box-shadow: 4px 0 32px rgba(15, 81, 50, 0.08);
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
  background: rgba(255, 255, 255, 0.75);
  color: var(--sf-green-mid);
  box-shadow: 0 4px 12px rgba(25, 135, 84, 0.2);
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.brand-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--sf-green);
  letter-spacing: 0.02em;
}

.brand-sub {
  font-size: 0.72rem;
  font-weight: 600;
  color: rgba(15, 81, 50, 0.65);
  margin-top: 2px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.7rem 0.9rem;
  border-radius: 12px;
  text-decoration: none;
  color: #1b4332;
  font-weight: 600;
  font-size: 0.95rem;
  border: 1px solid transparent;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.55);
  border-color: rgba(25, 135, 84, 0.2);
}

.nav-link--active {
  background: linear-gradient(135deg, #fff 0%, rgba(255, 255, 255, 0.92) 100%);
  color: var(--sf-green-mid);
  border-color: rgba(25, 135, 84, 0.35);
  box-shadow: 0 6px 20px rgba(25, 135, 84, 0.18);
}

.nav-icon {
  display: flex;
  opacity: 0.9;
}

.sidebar-foot {
  font-size: 0.68rem;
  color: rgba(15, 81, 50, 0.5);
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
