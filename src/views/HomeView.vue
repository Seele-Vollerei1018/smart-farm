<script setup>
import { ref, onMounted, computed } from 'vue'
import { getAuthUser, updateUserAvatar, getUserAvatar } from '@/utils/auth'
import { getDiaries, createDiary, updateDiary, deleteDiary as apiDeleteDiary } from '@/api/client'

// 日历相关
const currentDate = ref(new Date())
const daysInMonth = ref([])
const currentMonth = ref('')
const currentYear = ref('')
const today = ref(new Date())

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

// 农场日记
const farmDiaries = ref([])
const isLoading = ref(false)

// 待办任务
const tasks = ref([])
const showAddTask = ref(false)
const editingTask = ref(null)
const newTask = ref({ title: '', description: '' })

// 从本地存储加载任务
function loadTasks() {
  const user = getCurrentUser()
  if (!user) return

  try {
    const storedTasks = localStorage.getItem(`tasks_${user.username}`)
    if (storedTasks) {
      tasks.value = JSON.parse(storedTasks)
    }
  } catch (error) {
    console.error('加载任务失败:', error)
  }
}

// 保存任务到本地存储
function saveTasks() {
  const user = getCurrentUser()
  if (!user) return

  try {
    localStorage.setItem(`tasks_${user.username}`, JSON.stringify(tasks.value))
  } catch (error) {
    console.error('保存任务失败:', error)
  }
}

// 添加任务
function addTask() {
  if (!newTask.value.title.trim()) return

  const user = getCurrentUser()
  if (!user) {
    alert('请先登录')
    return
  }

  const newId = tasks.value.length > 0 ? Math.max(...tasks.value.map(t => t.id)) + 1 : 1

  tasks.value.unshift({
    id: newId,
    title: newTask.value.title,
    description: newTask.value.description,
    completed: false
  })

  saveTasks()
  cancelTaskEdit()
}

// 切换任务完成状态
function toggleTaskComplete(taskId) {
  const task = tasks.value.find(t => t.id === taskId)
  if (task) {
    task.completed = !task.completed
    saveTasks()
  }
}

// 编辑任务
function editTask(task) {
  editingTask.value = { ...task }
  newTask.value = { ...task }
  showAddTask.value = true
}

// 更新任务
function updateTask() {
  if (!newTask.value.title.trim()) return

  const user = getCurrentUser()
  if (!user) {
    alert('请先登录')
    return
  }

  const index = tasks.value.findIndex(t => t.id === editingTask.value.id)
  if (index !== -1) {
    tasks.value[index] = {
      ...tasks.value[index],
      title: newTask.value.title,
      description: newTask.value.description
    }
    saveTasks()
    cancelTaskEdit()
  }
}

// 删除任务
function deleteTask(id) {
  if (!confirm('确定要删除这个任务吗？')) return

  tasks.value = tasks.value.filter(t => t.id !== id)
  saveTasks()
}

// 取消任务编辑
function cancelTaskEdit() {
  showAddTask.value = false
  editingTask.value = null
  newTask.value = { title: '', description: '' }
}

// 日记编辑相关
const showAddDiary = ref(false)
const editingDiary = ref(null)
const newDiary = ref({ title: '', content: '' })

// 获取当前用户
function getCurrentUser() {
  return getAuthUser()
}

// 当前用户信息
const currentUser = computed(() => getAuthUser())
const username = computed(() => currentUser.value?.username || '用户')
const userAvatar = computed(() => getUserAvatar())

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
    const avatarDataUrl = e.target.result
    if (updateUserAvatar(avatarDataUrl)) {
      // 强制刷新计算属性
      currentUser.value = getAuthUser()
    } else {
      alert('头像更新失败，请重试')
    }
  }
  reader.readAsDataURL(file)
}

// 加载日记列表
async function loadDiaries() {
  const user = getCurrentUser()
  if (!user) return

  isLoading.value = true
  try {
    const diaries = await getDiaries(user.username)
    farmDiaries.value = diaries
  } catch (error) {
    console.error('加载日记失败:', error)
  } finally {
    isLoading.value = false
  }
}

// 保存日记
async function saveDiary() {
  if (!newDiary.value.title.trim()) return

  const user = getCurrentUser()
  if (!user) {
    alert('请先登录')
    return
  }

  try {
    if (editingDiary.value) {
      // 更新现有日记
      await updateDiary(user.username, editingDiary.value.id, newDiary.value.title, newDiary.value.content)
    } else {
      // 添加新日记
      const response = await createDiary(user.username, newDiary.value.title, newDiary.value.content)
      // 将新日记添加到列表开头
      if (response?.data) {
        farmDiaries.value.unshift(response.data)
      } else {
        // 如果没有返回数据，重新加载整个列表
        await loadDiaries()
      }
    }

    // 如果是编辑，则重新加载日记列表
    if (editingDiary.value) {
      await loadDiaries()
    }
    // 重置表单
    cancelEdit()
  } catch (error) {
    console.error('保存日记失败:', error)
    alert('保存日记失败，请重试')
  }
}

// 编辑日记
function editDiary(diary) {
  editingDiary.value = { ...diary }
  newDiary.value = { ...diary }
  showAddDiary.value = true
}

// 删除日记
async function deleteDiary(id) {
  if (!confirm('确定要删除这篇日记吗？')) return

  const user = getCurrentUser()
  if (!user) {
    alert('请先登录')
    return
  }

  try {
    await apiDeleteDiary(user.username, id)
    // 重新加载日记列表
    await loadDiaries()
  } catch (error) {
    console.error('删除日记失败:', error)
    alert('删除日记失败，请重试')
  }
}

// 取消编辑
function cancelEdit() {
  showAddDiary.value = false
  editingDiary.value = null
  newDiary.value = { title: '', content: '' }
}

// 解析 Markdown 为 HTML
function parseMarkdown(text) {
  if (!text) return ''

  // 简单的 Markdown 解析
  return text
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2" target="_blank">$1</a>')
    .replace(/^- (.*$)/gim, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/\n/gim, '<br>')
}

onMounted(() => {
  generateCalendar()
  loadDiaries()
  loadTasks()

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
})
</script>

<template>
  <div class="home">
    <div class="home-header">
      <div class="welcome-section">
        <span>welcome</span>
        <h1>你好，今天也来看看农场吧 👋</h1>
      </div>
    </div>

    <div class="home-main">
      <!-- 左侧主要内容 -->
      <main class="home-content">
        <!-- 主要功能卡片 -->
        <section class="feature-cards">
          <router-link to="/dashboard" class="feature-card">
            <div class="card-image">
              <!-- 后续添加图片 -->
            </div>
            <div class="card-content">
              <h1>农场情况</h1>
              <p>查看整体数据与环境状态</p>
            </div>
          </router-link>

          <router-link to="/control" class="feature-card">
            <div class="card-image">
              <!-- 后续添加图片 -->
            </div>
            <div class="card-content">
              <h1>我的农场</h1>
              <p>管理设备、地块与日常事务</p>
            </div>
          </router-link>

          <router-link to="/learning" class="feature-card">
            <div class="card-image">
              <!-- 后续添加图片 -->
            </div>
            <div class="card-content">
              <h1>趣味学习</h1>
              <p>了解种植知识与农业科普</p>
            </div>
          </router-link>
        </section>

        <!-- 农场日记 -->
        <section class="farm-diary">
          <div class="section-header">
            <h3>农场日记</h3>
            <div class="diary-actions">
              <button class="btn-primary" @click="showAddDiary = true">添加日记</button>
            </div>
          </div>

          <!-- 日记编辑表单 -->
          <div v-if="showAddDiary" class="diary-edit-form">
            <h4>{{ editingDiary ? '编辑日记' : '添加日记' }}</h4>
            <div class="form-group">
              <label for="diary-title">标题</label>
              <input type="text" id="diary-title" v-model="newDiary.title" placeholder="请输入日记标题" />
            </div>
            <div class="form-group">
              <label for="diary-content">内容（支持 Markdown 格式）</label>
              <textarea id="diary-content" v-model="newDiary.content" placeholder="请输入日记内容，支持 Markdown 格式" rows="6"></textarea>
            </div>
            <div class="form-actions">
              <button class="btn-primary" @click="saveDiary">{{ editingDiary ? '更新' : '保存' }}</button>
              <button class="btn-secondary" @click="cancelEdit">取消</button>
            </div>
          </div>

          <!-- 日记列表 -->
          <div class="diary-list">
            <div v-for="diary in farmDiaries" :key="diary.id" class="diary-item">
              <div class="diary-header">
                <h4>{{ diary.title }}</h4>
                <div class="diary-item-actions">
                  <button class="btn-edit" @click="editDiary(diary)">编辑</button>
                  <button class="btn-delete" @click="deleteDiary(diary.id)">删除</button>
                </div>
              </div>
              <div class="diary-content" v-html="parseMarkdown(diary.content)"></div>
              <div v-if="diary.createdAt" class="diary-meta">
                {{ new Date(diary.createdAt).toLocaleString() }}
              </div>
            </div>
            <div v-if="farmDiaries.length === 0" class="diary-empty">
              暂无日记，点击「添加日记」开始记录
            </div>
          </div>
        </section>
      </main>

      <!-- 右侧固定栏 -->
      <aside class="home-sidebar">
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
            <span class="username">{{ username }}</span>
            <span class="welcome">欢迎回来</span>
          </div>
        </div>

        <!-- 日历 -->
        <section class="calendar-section">
          <h3>日历</h3>
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
            <h3>待办任务</h3>
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
  </div>
</template>

<style scoped>
.home {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 2rem 2rem 0;
}

.home-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.welcome-section h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.welcome-section span {
  font-size: 1rem;
  font-weight: 400;
  color: #333a;
  margin: 0;
}

.search-box input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 0.9rem;
  width: 200px;
}

.home-main {
  display: flex;
  gap: 2rem;
  margin-right: 320px; /* 为右侧固定栏留出空间 */
}

.home-content {
  flex: 1;
  min-width: 0;
}

.home-sidebar {
  width: 400px;
  position: fixed;
  right: 2rem;
  top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  z-index: 10;
}

.user-profile {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-profile .avatar {
  position: relative;
  width: 50px;
  height: 50px;
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
  font-size: 0.75rem;
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
  font-weight: 700;
  color: #000;
  font-size: 1.2rem;
}

.user-profile .welcome {
  font-size: 0.8rem;
  color: #666;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.feature-card {
  display: block;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  text-decoration: none;
  color: inherit;
  position: relative;
  height: 280px;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-image {
  height: 100%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  background: transparent;
}

.card-content h1 {
  margin: 0 0 0.2rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #000;
}

.card-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #000;
}

.farm-diary {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.view-more {
  background: none;
  border: none;
  color: #25c18f;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0;
}

.diary-actions {
  display: flex;
  gap: 0.5rem;
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

.btn-secondary {
  background: #000000;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1rem;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #333333;
}

.diary-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.diary-item {
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  transition: box-shadow 0.2s;
}

.diary-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.diary-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.diary-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.diary-item-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit {
  background: #25c18f;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-delete {
  background: #000000;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-delete:hover {
  background: #333333;
}

.diary-content {
  margin-bottom: 0.75rem;
  line-height: 1.5;
  color: #333;
}

.diary-content h1,
.diary-content h2,
.diary-content h3 {
  margin: 1rem 0 0.5rem 0;
  color: #333;
}

.diary-content h1 {
  font-size: 1.4rem;
}

.diary-content h2 {
  font-size: 1.2rem;
}

.diary-content h3 {
  font-size: 1.1rem;
}

.diary-content em {
  font-style: italic;
}

.diary-content strong {
  font-weight: bold;
}

.diary-content a {
  color: #25c18f;
  text-decoration: none;
}

.diary-content a:hover {
  text-decoration: underline;
}

.diary-content ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.diary-content li {
  margin-bottom: 0.25rem;
}

.diary-meta {
  font-size: 0.8rem;
  color: #999;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e0e0e0;
}

.diary-empty {
  text-align: center;
  padding: 3rem;
  color: #999;
  background: #f5f5f5;
  border-radius: 8px;
  border: 2px dashed #ddd;
}

.farm-diary {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.btn-primary {
  background: #25c18f;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1rem;
  transition: background 0.2s;
}

.calendar-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  aspect-ratio: 1/1;
  display: flex;
  flex-direction: column;
}

.calendar-section h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
}

.calendar-header h4 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #666;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.3rem;
  margin-bottom: 0.3rem;
}

.calendar-weekdays span {
  text-align: center;
  font-size: 0.7rem;
  font-weight: 600;
  color: #666;
  padding: 0.3rem;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.3rem;
  flex: 1;
}

.calendar-day {
  text-align: center;
  padding: 0.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  transition: background 0.2s;
  min-height: 32px;
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
  font-weight: 600;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  padding: 0;
  margin: 0 auto;
}

.calendar-day.other-month {
  color: #ccc;
}

.tasks-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
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
  width: 20px;
  height: 20px;
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

@media (max-width: 1024px) {
  .home-main {
    flex-direction: column;
    margin-right: 0;
  }

  .home-sidebar {
    width: 100%;
    position: static;
    flex-direction: row;
    flex-wrap: wrap;
    right: auto;
    top: auto;
    bottom: auto;
  }

  .user-profile,
  .calendar-section,
  .tasks-section {
    flex: 1;
    min-width: 250px;
  }


}

@media (max-width: 768px) {
  .home {
    padding: 1rem;
  }

  .home-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .search-box input {
    width: 100%;
  }

  .feature-cards {
    grid-template-columns: 1fr;
  }

  .home-sidebar {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .user-profile {
    width: 100%;
    justify-content: flex-end;
  }

  .calendar-section,
  .tasks-section {
    flex: 1;
    min-width: calc(50% - 0.5rem);
    height: 300px;
  }

  .tasks-list {
    overflow-y: auto;
    max-height: calc(100% - 2rem);
  }


}
</style>