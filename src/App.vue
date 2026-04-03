<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { getAuthUser, logout } from './utils/auth'
import { getTasks as apiGetTasks, createTask as apiCreateTask, updateTask as apiUpdateTask, deleteTask as apiDeleteTask } from './api/client'
import defaultAvatar from '@/assets/头像.svg'

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
const userAvatar = computed(() => {
  return defaultAvatar
})

// 日历相关
const currentDate = ref(new Date())
const daysInMonth = ref([])
const currentMonth = ref('')
const currentYear = ref('')
const today = ref(new Date())

// 待办任务
const tasks = ref([])
const showAddTask = ref(false)
const editingTask = ref(null)
const newTask = ref({ title: '', description: '' })

watch(
  () => route.fullPath,
  () => {
    currentUser.value = getAuthUser()
  },
)

watch(
  currentUser,
  async () => {
    await loadTasks()
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

// 生成日历
function generateCalendar() {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()

  currentMonth.value = new Intl.DateTimeFormat('zh-CN', { month: 'long' }).format(currentDate.value)
  currentYear.value = year

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - firstDay.getDay())

  const calendarDays = []
  for (let i = 0; i < 42; i++) {
    const date = new Date(startDate)
    date.setDate(startDate.getDate() + i)
    calendarDays.push({
      date: date.getDate(),
      month: date.getMonth(),
      year: date.getFullYear(),
      isToday: date.toDateString() === today.value.toDateString(),
      isCurrentMonth: date.getMonth() === month
    })
  }

  daysInMonth.value = calendarDays
}

// 头像上传处理
function handleAvatarUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }

  // 验证文件大小（限制为2MB）
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过2MB')
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    // 由于后端暂未实现头像上传功能，这里仅做提示
    alert('头像上传功能暂未实现')
  }
  reader.readAsDataURL(file)
}

// 从后端加载任务
async function loadTasks() {
  const user = getAuthUser()
  if (!user) return

  try {
    tasks.value = await apiGetTasks(user.username)
  } catch (error) {
    console.error('加载任务失败:', error)
  }
}

// 添加任务
async function addTask() {
  if (!newTask.value.title.trim()) return

  const user = getAuthUser()
  if (!user) {
    alert('请先登录')
    return
  }

  try {
    const response = await apiCreateTask(user.username, newTask.value.title, newTask.value.description)
    if (response?.data) {
      tasks.value.unshift(response.data)
    } else {
      await loadTasks()
    }
    cancelTaskEdit()
  } catch (error) {
    console.error('添加任务失败:', error)
    alert('添加任务失败，请重试')
  }
}

// 编辑任务
function editTask(task) {
  editingTask.value = { ...task }
  newTask.value = { ...task }
  showAddTask.value = true
}

// 更新任务
async function updateTask() {
  if (!newTask.value.title.trim()) return

  const user = getAuthUser()
  if (!user) {
    alert('请先登录')
    return
  }

  try {
    await apiUpdateTask(user.username, editingTask.value.id, newTask.value.title, newTask.value.description, false)
    await loadTasks()
    cancelTaskEdit()
  } catch (error) {
    console.error('更新任务失败:', error)
    alert('更新任务失败，请重试')
  }
}

// 删除任务
async function deleteTask(id) {
  if (!confirm('确定要删除这个任务吗？')) return

  const user = getAuthUser()
  if (!user) return

  try {
    await apiDeleteTask(user.username, id)
    tasks.value = tasks.value.filter(t => t.id !== id)
  } catch (error) {
    console.error('删除任务失败:', error)
    alert('删除任务失败，请重试')
  }
}

// 切换任务完成状态
async function toggleTaskComplete(taskId) {
  const task = tasks.value.find(t => t.id === taskId)
  if (!task) return

  const user = getAuthUser()
  if (!user) return

  try {
    await apiUpdateTask(user.username, taskId, task.title, task.description, !task.completed)
    task.completed = !task.completed
  } catch (error) {
    console.error('更新任务状态失败:', error)
    alert('更新任务状态失败，请重试')
  }
}

// 取消任务编辑
function cancelTaskEdit() {
  showAddTask.value = false
  editingTask.value = null
  newTask.value = { title: '', description: '' }
}

// 初始化
async function init() {
  generateCalendar()
  await loadTasks()

  // 每天凌晨0点自动更新日期
  const now = new Date()
  const nextMidnight = new Date(now)
  nextMidnight.setHours(24, 0, 0, 0)
  const timeUntilMidnight = nextMidnight - now

  setTimeout(() => {
    setInterval(() => {
      currentDate.value = new Date()
      today.value = new Date()
      generateCalendar()
    }, 24 * 60 * 60 * 1000)

    currentDate.value = new Date()
    today.value = new Date()
    generateCalendar()
  }, timeUntilMidnight)
}

// 组件挂载时初始化
init()
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

    <!-- 全局右边栏 -->
    <aside class="global-sidebar" aria-label="全局信息栏">
      <!-- 用户名 -->
      <div class="user-profile">
        <div class="avatar" @click="$refs.avatarInput.click()">
          <img v-if="userAvatar" :src="userAvatar" alt="用户头像" />
          <div v-else class="avatar-placeholder">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div class="avatar-overlay">
            <span>更换头像</span>
          </div>
        </div>
        <input
          ref="avatarInput"
          type="file"
          accept="image/*"
          style="display: none"
          @change="handleAvatarUpload"
        />
        <div class="user-info">
          <span class="username">{{ displayName }}</span>
          <span class="welcome">欢迎回来</span>
        </div>
      </div>

      <!-- 日历 -->
      <section class="calendar-section">
        <h1>日历</h1>
        <div class="calendar-header">
          <h4>{{ currentYear }}年 {{ currentMonth }}</h4>
        </div>
        <div class="calendar-weekdays">
          <span>日</span>
          <span>一</span>
          <span>二</span>
          <span>三</span>
          <span>四</span>
          <span>五</span>
          <span>六</span>
        </div>
        <div class="calendar-days">
          <div
            v-for="(day, index) in daysInMonth"
            :key="index"
            class="calendar-day"
            :class="{
              'today': day.isToday,
              'other-month': !day.isCurrentMonth
            }"
          >
            {{ day.date }}
          </div>
        </div>
      </section>

      <!-- 待办任务 -->
      <section class="tasks-section">
        <div class="section-header">
          <h1>待办任务</h1>
          <button class="btn-primary" @click="showAddTask = true">添加任务</button>
        </div>

        <!-- 任务编辑表单 -->
        <div v-if="showAddTask" class="diary-edit-form">
          <h4>{{ editingTask ? '编辑任务' : '添加任务' }}</h4>
          <div class="form-group">
            <label for="task-title">标题</label>
            <input type="text" id="task-title" v-model="newTask.title" placeholder="请输入任务标题" />
          </div>
          <div class="form-group">
            <label for="task-description">描述</label>
            <textarea id="task-description" v-model="newTask.description" placeholder="请输入任务描述" rows="3"></textarea>
          </div>
          <div class="form-actions">
            <button class="btn-primary" @click="editingTask ? updateTask() : addTask()">{{ editingTask ? '更新' : '保存' }}</button>
            <button class="btn-secondary" @click="cancelTaskEdit">取消</button>
          </div>
        </div>

        <div class="tasks-list">
          <div v-for="task in tasks" :key="task.id" class="task-item" :class="{ 'task-completed': task.completed }">
            <div
              class="task-dot"
              :class="{ 'task-dot-completed': task.completed }"
              @click="toggleTaskComplete(task.id)"
            >
              <svg v-if="task.completed" class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <div class="task-content">
              <h4>{{ task.title }}</h4>
              <p>{{ task.description }}</p>
            </div>
            <div class="task-actions">
              <button class="btn-edit" @click="editTask(task)">编辑</button>
              <button class="btn-delete" @click="deleteTask(task.id)">删除</button>
            </div>
          </div>
          <div v-if="tasks.length === 0" class="diary-empty">
            暂无任务，点击「添加任务」开始创建
          </div>
        </div>
      </section>
    </aside>
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
  overflow: hidden;
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
  font-size: 1rem;
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
  padding: 0.9rem;
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

.main-content {
  flex: 1;
  margin-left: 252px;
  margin-right: 400px; /* 为右边栏留出空间 */
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 0;
  background: var(--sf-surface);
}

.main-content.sidebar-hidden {
  margin-left: 0;
  margin-right: 400px;
}

/* 全局右边栏样式 */
.global-sidebar {
  width: 350px;
  position: fixed;
  right: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  z-index: 10;
  background: white;
  border-radius: 0 0 0 12px;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  padding: 0.8rem;
  height: 100vh;
  box-sizing: border-box;
  overflow-y: auto;
}

.user-profile {
  background: white;
  border-radius: 12px;
  padding: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  height: 70px;
  box-sizing: border-box;
}

.user-profile .avatar {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-profile .avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.avatar-overlay span {
  color: white;
  font-size: 0.55rem;
  font-weight: 500;
}

.user-profile .avatar:hover .avatar-overlay {
  opacity: 1;
}

.user-profile .user-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-profile .username {
  font-weight: 600;
  color: #333;
  font-size: 1rem;
}

.user-profile .welcome {
  font-size: 0.8rem;
  color: #666;
}

.calendar-section {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  flex-shrink: 0;
  overflow: hidden;
}

.calendar-section h1 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  flex-shrink: 0;
}

.calendar-header h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.8rem;
  font-weight: 500;
  color: #666;
  flex-shrink: 0;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.2rem;
  margin-bottom: 0.2rem;
  flex-shrink: 0;
}

.calendar-weekdays span {
  text-align: center;
  font-size: 0.65rem;
  font-weight: 600;
  color: #666;
  padding: 0.3rem;
  min-height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.2rem;
  flex: 1;
  min-height: 0;
}

.calendar-day {
  text-align: center;
  padding: 0.3rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #333;
  transition: background 0.2s;
  min-height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-day:hover {
  background: #f0f0f0;
}

.calendar-day.today {
  background: #25c18f;
  color: white;
  text-align: center;
  padding: 0.3rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  min-height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.calendar-day.other-month {
  color: #ccc;
}

.tasks-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  box-sizing: border-box;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.tasks-section::-webkit-scrollbar {
  display: none;
}

.tasks-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-y: auto;
  max-height: calc(100% - 2rem);
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.tasks-list::-webkit-scrollbar {
  display: none;
}

.task-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.task-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-left: auto;
}

.task-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #ff4444;
  margin-top: 0.25rem;
  flex-shrink: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
}

.task-dot:hover {
  transform: scale(1.1);
  box-shadow: 0 0 8px rgba(255, 68, 68, 0.4);
}

.task-dot-completed {
  background: #25c18f;
  animation: pulse 0.4s ease;
}

.task-dot-completed:hover {
  box-shadow: 0 0 8px rgba(37, 193, 143, 0.4);
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1);
  }
}

.check-icon {
  width: 14px;
  height: 14px;
  color: white;
  animation: checkDraw 0.3s ease forwards;
}

@keyframes checkDraw {
  0% {
    stroke-dasharray: 20;
    stroke-dashoffset: 20;
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    stroke-dasharray: 20;
    stroke-dashoffset: 0;
    opacity: 1;
  }
}

.task-completed .task-content h4 {
  text-decoration: line-through;
  color: #999;
}

.task-completed .task-content p {
  color: #bbb;
}

.task-content h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  word-break: break-word;
  transition: all 0.3s ease;
}

.task-content p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
  word-break: break-word;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #25c18f;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #1db882;
}

.btn-secondary {
  background: #000000;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #333333;
}

.btn-edit {
  background: #25c18f;
  color: white;
  border: none;
  padding: 0.35rem 0.7rem;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-delete {
  background: #000000;
  color: white;
  border: none;
  padding: 0.35rem 0.7rem;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-delete:hover {
  background: #333333;
}

.diary-edit-form {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid #e0e0e0;
}

.diary-edit-form h4 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: inherit;
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.diary-empty {
  text-align: center;
  padding: 3rem;
  color: #999;
  background: #f5f5f5;
  border-radius: 8px;
  border: 2px dashed #ddd;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h1 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

@media (max-width: 900px) {
  .sidebar {
    width: 220px;
  }

  .main-content {
    margin-left: 220px;
    margin-right: 400px; /* 为右边栏留出空间 */
  }

  .main-content.sidebar-hidden {
    margin-left: 0;
    margin-right: 400px;
  }
}

@media (max-width: 640px) {
  .sidebar {
    width: 100%;
    max-width: min(280px, 88vw);
  }

  .main-content {
    margin-right: 0;
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
