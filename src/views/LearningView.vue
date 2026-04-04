<template>
  <div class="learning-page">

    <HeroSection
      :tabs="tabs"
      :activeTab="activeTab"
      @changeTab="val => activeTab = val"
    />

    <ToolSection
      :filteredTools="filteredTools"
      :currentTool="currentTool"
      :showDetail="showDetail"
      @selectTool="selectTool"
      @toggleDetail="toggleDetail"
      @askToolMore="askToolMore"
    />

    <QuizSection
      :currentQuiz="currentQuiz"
      :quizAnswered="quizAnswered"
      :isCorrect="isCorrect"
      :selectedAnswer="selectedAnswer"
      @checkAnswer="checkAnswer"
      @resetQuiz="resetQuiz"
      @askQuizAI="askQuizAI"
      :getOptionClass="getOptionClass"
    />

    <VideoSection
      :currentTool="currentTool"
      :currentVideoUrl="currentVideoUrl"
      @askVideoAI="askVideoAI"
    />

    <KnowledgeSection
      :knowledgeList="knowledgeList"
      @askKnowledge="askKnowledge"
    />

    <AIBox
      :messages="messages"
      :input="input"
      :isTyping="isTyping"
      :chatListRef="chatListRef"
      :renderMarkdown="renderMarkdown"
      @sendMessage="sendMessage"
      @quickAsk="quickAsk"
      @clearChat="clearChat"
      @update:input="val => input = val"
    />

  </div>
</template>


<script setup>
import HeroSection from '@/components/learning/HeroSection.vue'
import ToolSection from '@/components/learning/ToolSection.vue'
import QuizSection from '@/components/learning/QuizSection.vue'
import VideoSection from '@/components/learning/VideoSection.vue'
import KnowledgeSection from '@/components/learning/KnowledgeSection.vue'
import AIBox from '@/components/learning/AIBox.vue'
import { computed, nextTick, ref, onMounted } from 'vue'
const askKnowledge = () => {}
/* ================== 基础 ================== */
const tabs = ['全部', '小学', '初中']
const activeTab = ref('全部')
const showDetail = ref(false)

/* ================== 农具 ================== */
const tools = ref([
  
  {
    id: 1,
    name: '锄头',
    tag: '松土工具',
    level: '入门农具',
    usage: '用于松土、除草、翻土，是最常见的基础农具之一。',
    detail:
      '锄头适合用于田间浅层土壤整理，可以帮助土壤变松，提升空气和水分渗透能力，也便于清理杂草。',
    points: ['适合松土翻地', '可用于清理杂草', '使用方式直观易学'],
    image: 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=800&q=80',
    category: '小学',
    videoBvid: 'BV1xx411c7mD',
    videoTitle: '锄头的基础使用讲解',
    videoDesc: '通过短视频理解锄头的结构、用途以及使用时的动作要点。'
  },
  {
    id: 2,
    name: '铁锹',
    tag: '挖掘工具',
    level: '基础农具',
    usage: '用于铲土、挖坑、搬运泥土，在播种和移栽时很常见。',
    detail:
      '铁锹适合做较深的挖掘工作，例如挖种植坑、翻动泥土、搬运堆肥等，实用性很强。',
    points: ['可挖坑与铲土', '适合播种前整理', '用于搬运泥土堆肥'],
    image: 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=800&q=80',
    category: '小学',
    videoBvid: 'BV1xx411c7mD',
    videoTitle: '铁锹在播种中的作用',
    videoDesc: '了解铁锹如何帮助挖坑、翻土和完成基本田间劳动。'
  },
  {
    id: 3,
    name: '喷壶',
    tag: '灌溉工具',
    level: '轻便工具',
    usage: '用于给幼苗浇水，适合控制水量，避免冲坏嫩苗。',
    detail:
      '喷壶喷出的水较柔和，特别适合育苗阶段或小面积种植区域，便于学生观察浇水的变化。',
    points: ['适合幼苗浇灌', '水流柔和', '便于演示浇水过程'],
    image: 'https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&w=800&q=80',
    category: '初中',
    videoBvid: 'BV1xx411c7mD',
    videoTitle: '喷壶浇水小技巧',
    videoDesc: '从浇水力度到频率，快速掌握喷壶的正确使用方式。'
  }
])


const currentTool = ref(tools.value[0])

const filteredTools = computed(() => {
  if (activeTab.value === '全部') return tools.value
  return tools.value.filter(item => item.category === activeTab.value)
})

const currentVideoUrl = computed(() => {
  return `//player.bilibili.com/player.html?bvid=${currentTool.value.videoBvid}&page=1`
})

/* ================== 小测试（你丢的核心） ================== */

const currentQuiz = ref({
  question: '锄头最常见的用途是什么？',
  options: ['松土除草', '测量温度', '照明田地', '记录产量'],
  answer: '松土除草',
  explanation: '锄头主要用于松土、除草和翻土'
})

const quizAnswered = ref(false)
const isCorrect = ref(false)
const selectedAnswer = ref('')

const checkAnswer = (option) => {
  if (quizAnswered.value) return
  selectedAnswer.value = option
  quizAnswered.value = true
  isCorrect.value = option === currentQuiz.value.answer
}

const resetQuiz = () => {
  quizAnswered.value = false
  isCorrect.value = false
  selectedAnswer.value = ''
}

const getOptionClass = (option) => {
  if (!quizAnswered.value) return ''
  if (option === currentQuiz.value.answer) return 'right-answer'
  if (option === selectedAnswer.value) return 'wrong-answer'
  return ''
}

/* ================== 农具交互 ================== */

const selectTool = (item) => {
  currentTool.value = item
  showDetail.value = false
  resetQuiz()
}

const toggleDetail = () => {
  showDetail.value = !showDetail.value
}
/* ================== 农业小知识 ================== */
const knowledgeList = ref([
  {
    title: '什么是土壤？',
    desc: '土壤是植物生长的基础环境'
  },
  {
    title: '为什么要松土？',
    desc: '松土可以让空气进入土壤'
  }
])
/* ================== 聊天 ================== */

const input = ref('')
const messages = ref([])
const isTyping = ref(false)
const chatListRef = ref(null)
let messageId = 1

const STORAGE_KEY = 'learning-chat-history'

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) messages.value = JSON.parse(saved)
})

function saveHistory() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.value))
}

/* ================== ⭐ AI ================== */

/* 👉 推荐你用通义千问（国内稳定） */
const API_KEY = import.meta.env.VITE_AI_API_KEY

async function callAI(question) {
  try {
    const res = await fetch('http://localhost:8000/api/v1/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: question
      })
    })

    const data = await res.json()

    if (data.code === 200) {
      return data.data
    } else {
      return 'AI返回异常'
    }

  } catch (err) {
    console.error(err)
    return '❌ AI请求失败'
  }
}

/* ================== 发送消息 ================== */

const sendMessage = async () => {
  const question = input.value.trim()
  if (!question || isTyping.value) return

  messages.value.push({
    id: messageId++,
    role: 'user',
    content: question
  })

  input.value = ''
  await scrollChatToBottom()

  const aiMessage = {
    id: messageId++,
    role: 'ai',
    content: ''
  }

  messages.value.push(aiMessage)
  isTyping.value = true

  try {
    const reply = await callAI(question)

    for (let i = 0; i < reply.length; i++) {
      aiMessage.content += reply[i]
      await wait(15)
      await scrollChatToBottom()
    }

  } catch (e) {
    aiMessage.content = '❌ AI请求失败'
  }

  isTyping.value = false
  saveHistory()
}

/* ================== 快捷提问 ================== */

const quickAsk = (text) => {
  input.value = text
  sendMessage()
}

const askToolMore = (tool) => {
  input.value = `介绍一下${tool.name}的使用技巧`
  sendMessage()
}

const askQuizAI = () => {
  input.value = `解释为什么答案是${currentQuiz.value.answer}`
  sendMessage()
}

const askVideoAI = () => {
  input.value = `总结一下${currentTool.value.name}视频重点`
  sendMessage()
}

/* ================== 工具 ================== */

const wait = (ms) => new Promise(r => setTimeout(r, ms))

const scrollChatToBottom = async () => {
  await nextTick()
  if (chatListRef.value) {
    chatListRef.value.scrollTop = chatListRef.value.scrollHeight
  }
}

const clearChat = () => {
  messages.value = []
  localStorage.removeItem(STORAGE_KEY)
}

/* ================== Markdown ================== */

const escapeHtml = (text) =>
  text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

const renderMarkdown = (text) => {
  let html = escapeHtml(text)
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\n/g, '<br>')
  return html
}
</script>

<style scoped>
.learning-page {
  min-height: 100vh;
  padding: 28px 28px 160px;
  background:
    radial-gradient(circle at top left, rgba(128, 188, 111, 0.10), transparent 28%),
    radial-gradient(circle at top right, rgba(76, 175, 80, 0.08), transparent 24%),
    linear-gradient(180deg, #f9fbfa 0%, #f1f8f2 55%, #ebf5ed 100%);
  overflow-y: auto;
  box-sizing: border-box;
}

@media (max-width: 900px) {
  .learning-page {
    padding: 20px 16px 150px;
  }
}

/* ===== 共享卡片 ===== */
.learning-page :deep(.content-card) {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(118, 170, 119, 0.12);
  box-shadow: 0 14px 34px rgba(101, 131, 103, 0.08);
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 22px;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease-in-out;
}

.learning-page :deep(.content-card:hover) {
  transform: translateY(-2px);
  box-shadow: 0 18px 40px rgba(101, 131, 103, 0.12);
}

/* ===== 共享标题 ===== */
.learning-page :deep(.section-title-row) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.learning-page :deep(.section-title) {
  margin: 0;
  font-size: 24px;
  font-weight: 800;
  color: #253329;
}

.learning-page :deep(.section-subtitle) {
  color: #78907b;
  font-size: 13px;
}

/* ===== 共享按钮动画 ===== */
.learning-page :deep(.primary-btn),
.learning-page :deep(.ghost-btn),
.learning-page :deep(.clear-btn),
.learning-page :deep(.robot-btn),
.learning-page :deep(.quick-btn),
.learning-page :deep(.send-btn),
.learning-page :deep(.quiz-option) {
  transition: all 0.3s ease-in-out;
}

.learning-page :deep(.primary-btn) {
  border: none;
  background: #4caf50;
  color: #fff;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 22px rgba(76, 175, 80, 0.22);
}

.learning-page :deep(.primary-btn:hover) {
  transform: translateY(-2px);
}

.learning-page :deep(.ghost-btn) {
  border: 1px solid rgba(76, 175, 80, 0.24);
  background: #fff;
  color: #2f7d32;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
}

.learning-page :deep(.ghost-btn:hover) {
  background: #f4fbf4;
  transform: translateY(-2px);
}

.learning-page :deep(.clear-btn) {
  border: none;
  background: rgba(76, 175, 80, 0.12);
  color: #2f7d32;
  border-radius: 12px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
}

.learning-page :deep(.clear-btn:hover) {
  transform: translateY(-2px);
}

/* ===== 动画：必须 deep ===== */
.learning-page :deep(.fade-slide-enter-active),
.learning-page :deep(.fade-slide-leave-active) {
  transition: all 0.3s ease-in-out;
}

.learning-page :deep(.fade-slide-enter-from),
.learning-page :deep(.fade-slide-leave-to) {
  opacity: 0;
  transform: translateY(12px);
}

.learning-page :deep(.expand-enter-active),
.learning-page :deep(.expand-leave-active) {
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}

.learning-page :deep(.expand-enter-from),
.learning-page :deep(.expand-leave-to) {
  opacity: 0;
  max-height: 0;
}

.learning-page :deep(.expand-enter-to),
.learning-page :deep(.expand-leave-from) {
  opacity: 1;
  max-height: 220px;
}

/* ===== quiz 动画 ===== */
.learning-page :deep(.quiz-result) {
  animation: popIn 0.35s ease;
}

@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0.96);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* ===== 响应式共享布局 ===== */
@media (max-width: 1200px) {
  .learning-page :deep(.tool-detail),
  .learning-page :deep(.video-layout) {
    grid-template-columns: 1fr;
  }

  .learning-page :deep(.ai-bottom-bar) {
    width: calc(100vw - 360px);
  }
}

@media (max-width: 900px) {
  .learning-page :deep(.hero-title) {
    font-size: 28px;
  }

  .learning-page :deep(.quiz-options) {
    grid-template-columns: 1fr;
  }

  .learning-page :deep(.ai-bottom-bar) {
    width: calc(100vw - 32px);
    left: 16px;
    right: 16px;
    transform: none;
  }
  .learning-page {
  padding-bottom: 160px;
}
}
</style>