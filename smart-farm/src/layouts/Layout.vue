<template>
  <div class="app-shell">
    <!-- 左侧导航 -->
    <aside class="sidebar">
      <div class="sidebar-inner">
        <div class="brand">
          <div class="brand-title">智慧农场</div>
        </div>

        <nav class="nav-list">
          <div
            v-for="item in menus"
            :key="item.path"
            class="nav-item"
            :class="{ active: route.path === item.path }"
            @click="go(item.path)"
          >
            <span class="nav-text">{{ item.name }}</span>
          </div>
        </nav>

        <div class="sidebar-footer">
          <button v-if="!isLogin" class="auth-btn" @click="goLogin">
            登录
          </button>
          <button v-else class="auth-btn logout-btn" @click="logout">
            退出登录
          </button>
        </div>
      </div>
    </aside>

    <!-- 中间主区域 -->
    <main class="main-area">
      <router-view />
    </main>

<!-- 右侧栏：头像 / 日历 / 待办 -->
<aside class="rightbar">
  <div class="rightbar-inner">

    <div class="user-card" v-if="isLogin">
      <div class="user-meta">
        <div class="avatar-wrap">
          <img
            class="avatar"
            src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80"
            alt="avatar"
          />
        </div>
        <div class="user-text">
          <div class="user-name">用户名</div>
          <div class="user-role">欢迎回来</div>
        </div>
      </div>
    </div>

    <div class="calendar-card">
      <aside class="right-panel">
        <DutyPanel />
      </aside>
      
    </div>

    <!-- ⭐ 农场活跃度 -->
    <div class="todo-card">
      <div class="card-title">农场活跃度</div>

      <div class="farmer-wrap">
        <img src="@/assets/farmer.png" class="farmer-img" />
      </div>

      <div class="sun-list">
        <span
          v-for="sun in suns"
          :key="sun.id"
          class="sun"
          @click="collectSun($event, sun.id)"
        >
          ☀️
        </span>
      </div>

      <div class="agri-info">
        <div class="score">阳光值：{{ score }}</div>
        <div class="status">{{ status }}</div>
      </div>
    </div>

  </div> <!-- ⭐ rightbar-inner 结束 -->
</aside>
</div> 
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import DutyPanel from '@/components/DutyPanel.vue'
// ✅ 用你自己的 auth.js
import {
  isAuthenticated,
  getAuthUser,
  logout as authLogout
} from '@/utils/auth'


const suns = ref([])
const score = ref(0)
let id = 0

const generateSun = () => {
  if (suns.value.length < 5) {
    suns.value.push({ id: id++ })
  }
}

const collectSun = (e, sunId) => {
  // ⭐ 获取点击位置（用于动画）
  const el = e.target
  const rect = el.getBoundingClientRect()

  const fly = document.createElement('div')
  fly.innerText = '☀️'
  fly.style.position = 'fixed'
  fly.style.left = rect.left + 'px'
  fly.style.top = rect.top + 'px'
  fly.style.fontSize = '20px'
  fly.style.transition = 'all 0.6s ease'

  document.body.appendChild(fly)

  // 飞向小人
  const farmer = document.querySelector('.farmer-img')
  const target = farmer.getBoundingClientRect()

  setTimeout(() => {
    fly.style.left = target.left + 'px'
    fly.style.top = target.top + 'px'
    fly.style.opacity = 0
    fly.style.transform = 'scale(0.5)'
  }, 10)

  setTimeout(() => {
    document.body.removeChild(fly)
  }, 600)

  suns.value = suns.value.filter(s => s.id !== sunId)
  score.value++
}

const status = computed(() => {
  if (score.value < 5) return '农场较空闲'
  if (score.value < 10) return '农场正常运行'
  return '农场活跃度高'
})

onMounted(() => {
  setInterval(generateSun, 3000)
})
const router = useRouter()
const route = useRoute()

/* ===== 用户状态 ===== */
const user = ref(null)

/* 初始化 */
const initUser = () => {
  user.value = getAuthUser()
}

/* 页面加载时读取 */
onMounted(() => {
  initUser()
})

/* ===== 是否登录 ===== */
const isLogin = computed(() => !!user.value)

/* ===== 当前用户名 ===== */
const username = computed(() => {
  return user.value?.displayName || user.value?.username || ''
})

/* ===== 路由跳转 ===== */
const go = (path) => {
  if (route.path === path) return
  router.push(path)
}

/* ===== 登录跳转 ===== */
const goLogin = () => {
  router.push('/login')
}

/* ===== 退出登录 ===== */
const logout = () => {
  authLogout() // ✅ 用你 auth.js 的
  user.value = null
  router.push('/login')
}

/* ===== 监听登录变化（关键！） ===== */
/* 当从 login 页面回来时刷新用户状态 */
router.afterEach(() => {
  initUser()
})

/* ===== 菜单 ===== */
const menus = [
  { name: '首页', path: '/' },
  { name: '农场情况', path: '/dashboard' },
  { name: '我的农场', path: '/control' },
  { name: '趣味学习', path: '/learning' }
]
</script>
<style>
:root {
  --bg-page: #F4F7F6;
  --bg-card: #FFFFFF;
  --primary: #25C18F;
  --text-main: #1E293B;
  --text-sub: #94A3B8;
  --radius-xl: 24px;
  --radius-md: 12px;
  --shadow-soft: 0 10px 30px rgba(15, 23, 42, 0.04);
  --gap-main: 24px;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  height: 100%;
  font-family: "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
  background: var(--bg-page);
  color: var(--text-main);
}

body {
  overflow: hidden;
}

.app-shell {
  height: 100vh;
  overflow: hidden;
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr) 320px;
  gap: 24px;
  padding: 24px 40px;
  background: var(--bg-page);
}

/* 左侧导航 */
.sidebar {
  min-width: 0;
}

.sidebar-inner {
  height: 100%;
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-soft);
  padding: 24px 18px;
  display: flex;
  flex-direction: column;
}

.brand {
  margin-bottom: 24px;
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--text-main);
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav-item {
  min-height: 52px;
  border-radius: 16px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.25s ease;
  color: var(--text-main);
  background: transparent;
}

.nav-item:hover {
  transform: translateY(-1px);
  background: rgba(37, 193, 143, 0.08);
}

.nav-item.active {
  background: var(--primary);
  color: #fff;
  box-shadow: 0 8px 20px rgba(37, 193, 143, 0.3);
}

.nav-text {
  font-size: 16px;
  font-weight: 600;
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 24px;
}

.auth-btn {
  width: 100%;
  height: 48px;
  border: none;
  border-radius: 14px;
  background: var(--primary);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(37, 193, 143, 0.2);
  transition: all 0.25s ease;
}

.auth-btn:hover {
  transform: translateY(-1px);
}

.logout-btn {
  background: #0f172a;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.12);
}

/* 中间 */
.main-area {
  
  height: 100%;
  overflow-y: auto;  /* ✅ 关键 */
  min-width: 0;
}


/* 右侧栏 */
.rightbar {
  min-width: 0;
}

.rightbar-inner {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.user-card,
.calendar-card,
.todo-card {
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-soft);
  border: none;
}

.user-card {
  padding: 18px 20px;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 14px;
}

.avatar-wrap {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: #e8f7f1;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-main);
}

.user-role {
  margin-top: 4px;
  font-size: 13px;
  color: var(--text-sub);
}

.calendar-card {
  padding: 20px;
}

.todo-card {
  padding: 20px;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 20px;
  line-height: 1.2;
}

.week-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  margin-bottom: 10px;
  color: var(--text-sub);
  font-size: 12px;
  text-align: center;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-grid span {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #475569;
  font-size: 14px;
}

.calendar-grid span.active {
  background: var(--primary);
  color: #fff;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  min-height: 0;
  padding-right: 4px;
}

.todo-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.todo-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--primary);
  margin-top: 8px;
  flex-shrink: 0;
}

.todo-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main);
}

.todo-time {
  margin-top: 4px;
  font-size: 13px;
  color: var(--text-sub);
}

/* 平板 */
@media (max-width: 1200px) {
  .app-shell {
    grid-template-columns: 240px minmax(0, 1fr);
    padding: 20px 24px;
  }

  .rightbar {
    display: none;
  }
}

/* 手机 / 小程序风格单列 */
@media (max-width: 768px) {
  body {
    overflow: auto;
  }

  .app-shell {
    display: block;
    height: auto;
    min-height: 100vh;
    padding: 16px;
  }

  .sidebar {
    display: none;
  }

  .rightbar {
    display: none;
  }

  .main-area {
    height: auto;
    overflow: visible;
  }
}

.farmer-wrap {
  display: flex;
  justify-content: center;
}

.farmer-img {
  width: 60px;
  height: 60px;
  object-fit: contain;

  animation: breathe 2.5s ease-in-out infinite;
}

@keyframes breathe {
  0% { transform: scale(1) }
  50% { transform: scale(1.08) }
  100% { transform: scale(1) }
}

.sun {
  font-size: 18px;
  cursor: pointer;
  animation: fadeIn 0.5s ease;
  transition: transform 0.2s;
}

.sun:active {
  transform: scale(1.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.sun-list {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin: 8px 0;
  min-height: 30px;
}

.agri-info {
  text-align: center;
  font-size: 13px;
}
</style>