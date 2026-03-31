<template>
  <div class="learning-page">
    <!-- 顶部标题 -->
    <section class="hero-section">
      <div class="hero-badge">🌱 趣味学习</div>
      <h1 class="hero-title">认识农具，轻松学农业知识</h1>
      <p class="hero-desc">从农具讲解、小测试到视频学习，再用 AI 深入提问，形成完整学习闭环。</p>

      <div class="category-tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          class="tab-btn"
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
        >
          {{ tab }}
        </button>
      </div>
    </section>

    <!-- 农具讲解 -->
    <section class="content-card tool-section">
      <div class="section-title-row">
        <h2 class="section-title">🌾 农具讲解</h2>
        <span class="section-subtitle">点击卡片可切换农具，点击按钮可联动 AI</span>
      </div>

      <div class="tool-scroll">
        <div
          v-for="item in filteredTools"
          :key="item.id"
          class="tool-card"
          :class="{ selected: currentTool.id === item.id }"
          @click="selectTool(item)"
        >
          <div class="tool-image-wrap">
            <img :src="item.image" :alt="item.name" class="tool-image" />
          </div>
          <div class="tool-name">{{ item.name }}</div>
          <div class="tool-tag">{{ item.tag }}</div>
        </div>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img :src="currentTool.image" :alt="currentTool.name" class="tool-main-image" />
            </div>
          </div>

          <div class="tool-detail-right">
            <div class="tool-title-line">
              <h3 class="tool-title">{{ currentTool.name }}</h3>
              <span class="tool-level">{{ currentTool.level }}</span>
            </div>

            <p class="tool-usage">{{ currentTool.usage }}</p>

            <div class="tool-point-list">
              <div class="tool-point" v-for="(point, index) in currentTool.points" :key="index">
                <span class="point-dot"></span>
                <span>{{ point }}</span>
              </div>
            </div>

            <div class="tool-action-row">
              <button class="primary-btn" @click="toggleDetail">
                {{ showDetail ? '收起详细' : '查看详细' }}
              </button>
              <button class="ghost-btn" @click="askToolMore(currentTool)">
                🤖 问 AI 更多
              </button>
            </div>

            <transition name="expand">
              <div v-if="showDetail" class="tool-detail-panel">
                <h4>农具小百科</h4>
                <p>{{ currentTool.detail }}</p>
              </div>
            </transition>
          </div>
        </div>
      </transition>
    </section>

    <!-- 小测试 -->
    <section class="content-card quiz-section">
      <div class="section-title-row">
        <h2 class="section-title">🧪 小测试</h2>
        <span class="section-subtitle">做一道轻量题目，马上检验学习效果</span>
      </div>

      <div class="quiz-box">
        <div class="quiz-question">{{ currentQuiz.question }}</div>

        <div class="quiz-options">
          <button
            v-for="(option, index) in currentQuiz.options"
            :key="index"
            class="quiz-option"
            :class="getOptionClass(option)"
            @click="checkAnswer(option)"
            :disabled="quizAnswered"
          >
            {{ option }}
          </button>
        </div>

        <transition name="fade-slide">
          <div v-if="quizAnswered" class="quiz-result" :class="{ correct: isCorrect, wrong: !isCorrect }">
            <div class="quiz-result-title">
              {{ isCorrect ? '✅ 回答正确！' : '❌ 回答不对，再想想' }}
            </div>
            <div class="quiz-result-desc">
              {{ currentQuiz.explanation }}
            </div>
          </div>
        </transition>

        <div class="quiz-action-row">
          <button class="ghost-btn" @click="resetQuiz">重新作答</button>
          <button class="primary-btn" @click="askQuizAI">🤖 让 AI 讲讲这题</button>
        </div>
      </div>
    </section>

    <!-- 推荐视频 -->
    <section class="content-card video-section">
      <div class="section-title-row">
        <h2 class="section-title">🎬 推荐视频</h2>
        <span class="section-subtitle">通过视频进一步理解农具用途与农业实践</span>
      </div>

      <div class="video-layout">
        <div class="video-player-box">
          <iframe
            class="video-frame"
            :src="currentVideoUrl"
            scrolling="no"
            border="0"
            frameborder="no"
            framespacing="0"
            allowfullscreen="true"
          ></iframe>
        </div>

        <div class="video-info">
          <h3 class="video-title">{{ currentTool.videoTitle }}</h3>
          <p class="video-desc">{{ currentTool.videoDesc }}</p>
          <button class="ghost-btn" @click="askVideoAI">🤖 问 AI 总结视频重点</button>
        </div>
      </div>
    </section>

    <!-- 农业小知识 -->
    <section class="content-card knowledge-section">
      <div class="section-title-row">
        <h2 class="section-title">📚 农业小知识</h2>
        <span class="section-subtitle">点击机器人图标可以直接追问 AI</span>
      </div>

      <div class="knowledge-list">
        <div class="knowledge-item" v-for="(item, index) in knowledgeList" :key="index">
          <div class="knowledge-text">
            <div class="knowledge-title">{{ item.title }}</div>
            <div class="knowledge-desc">{{ item.desc }}</div>
          </div>
          <button class="robot-btn" @click="askKnowledge(item)">🤖</button>
        </div>
      </div>
    </section>

    <!-- 聊天记录 -->
    <section class="content-card chat-history-section">
      <div class="section-title-row">
        <h2 class="section-title">💬 AI 对话记录</h2>
        <button class="clear-btn" @click="clearChat">🗑️ 清空对话</button>
      </div>

      <div class="chat-list" ref="chatListRef">
        <div v-if="messages.length === 0" class="chat-empty">
          还没有提问，试试点击“问 AI 更多”或者使用底部输入框。
        </div>

        <div
          v-for="msg in messages"
          :key="msg.id"
          class="chat-item"
          :class="msg.role"
        >
          <div class="bubble" v-if="msg.role === 'user'">
            {{ msg.content }}
          </div>

          <div
            class="bubble markdown-body"
            v-else
            v-html="renderMarkdown(msg.content)"
          ></div>
        </div>
      </div>
    </section>

    <!-- 占位，避免底部输入框遮住内容 -->
    <div class="bottom-safe-space"></div>

    <!-- 底部固定 AI 输入框 -->
    <div class="ai-bottom-bar">
      <div class="quick-question-row">
        <button class="quick-btn" @click="quickAsk('💡 农具怎么用？')">💡 农具怎么用？</button>
        <button class="quick-btn" @click="quickAsk('🌱 作物怎么种？')">🌱 作物怎么种？</button>
        <button class="quick-btn" @click="quickAsk('🧱 为什么要松土？')">🧱 为什么要松土？</button>
      </div>

      <div class="input-row">
        <input
          v-model="input"
          class="ai-input"
          placeholder="问点农业问题，比如：锄头为什么适合松土？"
          @keydown.enter="sendMessage"
        />
        <button class="send-btn" @click="sendMessage" :disabled="isTyping">
          {{ isTyping ? '思考中...' : '发送' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue'

const tabs = ['全部', '小学', '初中']
const activeTab = ref('全部')
const showDetail = ref(false)

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

const knowledgeList = ref([
  {
    title: '为什么要松土？',
    desc: '松土能让空气和水分更容易进入土壤，帮助根系更好呼吸。'
  },
  {
    title: '为什么幼苗不能猛浇水？',
    desc: '幼苗根系较弱，水流太大会冲坏根部和周围土层。'
  },
  {
    title: '为什么要及时除草？',
    desc: '杂草会和农作物争抢养分、水分和阳光。'
  }
])

const currentQuiz = ref({
  question: '锄头最常见的用途是什么？',
  options: ['松土除草', '测量温度', '照明田地', '记录产量'],
  answer: '松土除草',
  explanation: '锄头主要用于松土、除草和浅层翻土，是基础农业劳动中最常见的工具之一。'
})

const quizAnswered = ref(false)
const isCorrect = ref(false)

const input = ref('')
const messages = ref([])
const isTyping = ref(false)
const chatListRef = ref(null)
let messageId = 1

const selectTool = (item) => {
  currentTool.value = item
  showDetail.value = false

  if (item.name === '锄头') {
    currentQuiz.value = {
      question: '锄头最常见的用途是什么？',
      options: ['松土除草', '测量温度', '照明田地', '记录产量'],
      answer: '松土除草',
      explanation: '锄头主要用于松土、除草和浅层翻土，是基础农业劳动中最常见的工具之一。'
    }
  } else if (item.name === '铁锹') {
    currentQuiz.value = {
      question: '铁锹更适合下面哪种工作？',
      options: ['挖坑铲土', '喷灌叶面', '检测虫害', '裁剪枝叶'],
      answer: '挖坑铲土',
      explanation: '铁锹更适合挖坑、铲土和搬运泥土，在播种、移栽等工作中很实用。'
    }
  } else {
    currentQuiz.value = {
      question: '喷壶的主要作用是什么？',
      options: ['柔和浇水', '快速翻地', '收割作物', '压平土壤'],
      answer: '柔和浇水',
      explanation: '喷壶适合给幼苗和小面积区域浇水，能够更好地控制水量，避免伤苗。'
    }
  }

  resetQuiz()
}

const toggleDetail = () => {
  showDetail.value = !showDetail.value
}

const getOptionClass = (option) => {
  if (!quizAnswered.value) return ''
  if (option === currentQuiz.value.answer) return 'right-answer'
  if (option !== currentQuiz.value.answer && option === selectedAnswer.value) return 'wrong-answer'
  return ''
}

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

const quickAsk = (text) => {
  input.value = text
  sendMessage()
}

const askToolMore = (tool) => {
  input.value = `告诉我更多关于${tool.name}的冷知识和使用技巧`
  sendMessage()
}

const askKnowledge = (item) => {
  input.value = `${item.title}？请用简单易懂的方式讲给学生听`
  sendMessage()
}

const askQuizAI = () => {
  input.value = `请解释这道题为什么答案是“${currentQuiz.value.answer}”，并补充一个农业小知识`
  sendMessage()
}

const askVideoAI = () => {
  input.value = `请帮我总结一下关于${currentTool.value.name}视频讲解的重点，分点回答`
  sendMessage()
}

const buildAiReply = (question) => {
  if (question.includes('松土')) {
    return `**✅ 作用：** 松土能让土壤更透气。\n\n**🌱 好处：** 根系更容易呼吸，也更容易吸收水分和养分。\n\n**🚜 场景：** 在播种前、雨后土壤板结时，常常需要松土。`
  }

  if (question.includes('锄头')) {
    return `**✅ 认识农具：锄头**\n\n- 🧹 常见用途：松土、除草、浅层翻地\n- 🌾 使用场景：菜园、花圃、小块农田\n- 💡 小提醒：使用时动作要稳，注意和脚保持安全距离`
  }

  if (question.includes('铁锹')) {
    return `**✅ 认识农具：铁锹**\n\n- ⛏️ 主要功能：挖坑、铲土、搬运泥土\n- 🌱 适用场景：播种、移栽、施肥前整理土地\n- 💡 小提醒：铲土时要注意发力方向，避免伤到周围植物`
  }

  if (question.includes('喷壶')) {
    return `**✅ 认识农具：喷壶**\n\n- 💧 主要功能：柔和浇水\n- 🌿 适合对象：幼苗、小盆栽、小面积种植区\n- 💡 小提醒：少量多次浇水，比一次浇太多更合适`
  }

  return `**✅ AI学习助手回复**\n\n- 🌱 我已经收到你的问题：${question}\n- 📚 建议你结合上面的农具讲解和视频一起理解\n- 🤖 你也可以继续追问“为什么”“怎么用”“有什么区别”这类问题`
}

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

  const finalReply = buildAiReply(question)

  for (let i = 0; i < finalReply.length; i++) {
    aiMessage.content += finalReply[i]
    await wait(finalReply[i] === '\n' ? 20 : 18)
    await scrollChatToBottom()
  }

  isTyping.value = false
}

const clearChat = () => {
  messages.value = []
}

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const scrollChatToBottom = async () => {
  await nextTick()
  if (chatListRef.value) {
    chatListRef.value.scrollTop = chatListRef.value.scrollHeight
  }
}

const escapeHtml = (text) => {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

const renderMarkdown = (text) => {
  let html = escapeHtml(text)

  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/^- (.*)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
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

.hero-section {
  margin-bottom: 24px;
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 18px;
  border-radius: 999px;
  background: rgba(76, 175, 80, 0.12);
  color: #2f7d32;
  font-weight: 700;
  margin-bottom: 14px;
}

.hero-title {
  margin: 0;
  font-size: 36px;
  font-weight: 800;
  color: #223228;
}

.hero-desc {
  margin: 12px auto 0;
  max-width: 720px;
  color: #5f7062;
  font-size: 15px;
  line-height: 1.8;
}

.category-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 22px;
  flex-wrap: wrap;
}

.tab-btn {
  border: none;
  background: rgba(255, 255, 255, 0.82);
  color: #54715a;
  padding: 10px 18px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(76, 175, 80, 0.06);
  transition: all 0.3s ease-in-out;
}

.tab-btn:hover {
  transform: translateY(-2px);
}

.tab-btn.active {
  background: #4caf50;
  color: #fff;
  box-shadow: 0 12px 28px rgba(76, 175, 80, 0.24);
}

.content-card {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(118, 170, 119, 0.12);
  box-shadow: 0 14px 34px rgba(101, 131, 103, 0.08);
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 22px;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease-in-out;
}

.content-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 40px rgba(101, 131, 103, 0.12);
}

.section-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.section-title {
  margin: 0;
  font-size: 24px;
  font-weight: 800;
  color: #253329;
}

.section-subtitle {
  color: #78907b;
  font-size: 13px;
}

.tool-scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 10px;
  margin-bottom: 22px;
}

.tool-scroll::-webkit-scrollbar {
  height: 8px;
}

.tool-scroll::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.28);
  border-radius: 999px;
}

.tool-card {
  min-width: 180px;
  background: #f8fcf8;
  border: 1px solid rgba(76, 175, 80, 0.12);
  border-radius: 20px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  flex-shrink: 0;
}

.tool-card:hover {
  transform: translateY(-4px) scale(1.01);
  border-color: rgba(76, 175, 80, 0.32);
  box-shadow: 0 14px 26px rgba(76, 175, 80, 0.12);
}

.tool-card.selected {
  border-color: #4caf50;
  background: linear-gradient(180deg, #f9fff9 0%, #f0faef 100%);
  box-shadow: 0 14px 26px rgba(76, 175, 80, 0.16);
}

.tool-image-wrap {
  width: 100%;
  height: 120px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 12px;
  background: #eef5ef;
}

.tool-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tool-name {
  font-size: 18px;
  font-weight: 800;
  color: #243128;
}

.tool-tag {
  margin-top: 6px;
  color: #6f8b72;
  font-size: 13px;
}

.tool-detail {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  align-items: start;
}

.tool-main-image-box {
  width: 100%;
  height: 260px;
  border-radius: 22px;
  overflow: hidden;
  background: #edf6ee;
}

.tool-main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tool-title-line {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.tool-title {
  margin: 0;
  font-size: 30px;
  font-weight: 800;
  color: #223228;
}

.tool-level {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(76, 175, 80, 0.12);
  color: #2f7d32;
  font-size: 12px;
  font-weight: 700;
}

.tool-usage {
  color: #5e725f;
  line-height: 1.9;
  margin: 14px 0 18px;
}

.tool-point-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tool-point {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #455b48;
}

.point-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4caf50;
  flex-shrink: 0;
}

.tool-action-row,
.quiz-action-row {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.primary-btn,
.ghost-btn,
.clear-btn,
.robot-btn,
.quick-btn,
.send-btn,
.quiz-option {
  transition: all 0.3s ease-in-out;
}

.primary-btn {
  border: none;
  background: #4caf50;
  color: #fff;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 22px rgba(76, 175, 80, 0.22);
}

.primary-btn:hover {
  transform: translateY(-2px);
}

.ghost-btn {
  border: 1px solid rgba(76, 175, 80, 0.24);
  background: #fff;
  color: #2f7d32;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
}

.ghost-btn:hover {
  background: #f4fbf4;
  transform: translateY(-2px);
}

.tool-detail-panel {
  margin-top: 18px;
  background: #f7fbf7;
  border: 1px dashed rgba(76, 175, 80, 0.28);
  border-radius: 18px;
  padding: 16px;
  color: #546856;
  line-height: 1.9;
}

.tool-detail-panel h4 {
  margin: 0 0 8px;
  color: #2b4030;
}

.quiz-box {
  background: linear-gradient(180deg, #fbfefb 0%, #f4fbf5 100%);
  border-radius: 20px;
  padding: 22px;
  border: 1px solid rgba(76, 175, 80, 0.12);
}

.quiz-question {
  font-size: 22px;
  font-weight: 800;
  color: #243028;
  margin-bottom: 18px;
}

.quiz-options {
  display: grid;
  grid-template-columns: repeat(2, minmax(180px, 1fr));
  gap: 14px;
}

.quiz-option {
  border: 1px solid rgba(76, 175, 80, 0.16);
  background: #fff;
  color: #38503d;
  padding: 16px;
  border-radius: 16px;
  text-align: left;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
}

.quiz-option:hover:not(:disabled) {
  transform: translateY(-2px);
  border-color: rgba(76, 175, 80, 0.36);
  box-shadow: 0 10px 20px rgba(76, 175, 80, 0.10);
}

.quiz-option:disabled {
  cursor: not-allowed;
}

.right-answer {
  background: rgba(76, 175, 80, 0.12);
  border-color: #4caf50;
  color: #2f7d32;
}

.wrong-answer {
  background: rgba(244, 67, 54, 0.08);
  border-color: rgba(244, 67, 54, 0.4);
  color: #b23a32;
}

.quiz-result {
  margin-top: 18px;
  padding: 16px 18px;
  border-radius: 16px;
  animation: popIn 0.35s ease;
}

.quiz-result.correct {
  background: rgba(76, 175, 80, 0.10);
  color: #2f7d32;
}

.quiz-result.wrong {
  background: rgba(244, 67, 54, 0.08);
  color: #9a352e;
}

.quiz-result-title {
  font-weight: 800;
  margin-bottom: 6px;
}

.video-layout {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 22px;
  align-items: start;
}

.video-player-box {
  border-radius: 22px;
  overflow: hidden;
  background: #eef5ef;
  min-height: 320px;
}

.video-frame {
  width: 100%;
  height: 320px;
}

.video-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.video-title {
  margin: 0 0 12px;
  font-size: 24px;
  color: #243129;
}

.video-desc {
  color: #607460;
  line-height: 1.9;
  margin-bottom: 18px;
}

.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.knowledge-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  padding: 18px;
  border-radius: 18px;
  background: #f8fcf8;
  border: 1px solid rgba(76, 175, 80, 0.10);
}

.knowledge-title {
  font-size: 18px;
  font-weight: 800;
  color: #253228;
}

.knowledge-desc {
  margin-top: 6px;
  color: #6d846e;
  line-height: 1.7;
}

.robot-btn {
  border: none;
  background: rgba(76, 175, 80, 0.12);
  color: #2f7d32;
  width: 48px;
  height: 48px;
  border-radius: 16px;
  cursor: pointer;
  font-size: 20px;
  flex-shrink: 0;
}

.robot-btn:hover {
  transform: scale(1.08);
  background: rgba(76, 175, 80, 0.18);
}

.chat-history-section {
  display: flex;
  flex-direction: column;
}

.clear-btn {
  border: none;
  background: rgba(76, 175, 80, 0.12);
  color: #2f7d32;
  border-radius: 12px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
}

.clear-btn:hover {
  transform: translateY(-2px);
}

.chat-list {
  max-height: 360px;
  overflow-y: auto;
  padding-right: 6px;
}

.chat-list::-webkit-scrollbar {
  width: 8px;
}

.chat-list::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.22);
  border-radius: 999px;
}

.chat-empty {
  padding: 22px;
  border-radius: 18px;
  text-align: center;
  color: #7c8f7d;
  background: #f8fcf8;
}

.chat-item {
  display: flex;
  margin-bottom: 14px;
}

.chat-item.user {
  justify-content: flex-end;
}

.chat-item.ai {
  justify-content: flex-start;
}

.bubble {
  max-width: min(82%, 760px);
  padding: 14px 16px;
  border-radius: 18px;
  line-height: 1.8;
  word-break: break-word;
  box-shadow: 0 10px 22px rgba(77, 112, 79, 0.06);
}

.chat-item.user .bubble {
  background: #4caf50;
  color: #fff;
  border-bottom-right-radius: 6px;
}

.chat-item.ai .bubble {
  background: #fff;
  color: #344635;
  border: 1px solid rgba(76, 175, 80, 0.10);
  border-bottom-left-radius: 6px;
}

.markdown-body strong {
  color: #2c6b30;
}

.markdown-body ul {
  margin: 8px 0 8px 18px;
  padding: 0;
}

.markdown-body li {
  margin-bottom: 4px;
}

.bottom-safe-space {
  height: 90px;
}

.ai-bottom-bar {
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 18px;
  width: min(1100px, calc(100vw - 420px));
  z-index: 50;
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(76, 175, 80, 0.12);
  box-shadow: 0 16px 36px rgba(84, 122, 85, 0.16);
  border-radius: 24px;
  padding: 14px;
}

.quick-question-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.quick-btn {
  border: none;
  background: rgba(76, 175, 80, 0.10);
  color: #2f7d32;
  border-radius: 999px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
}

.quick-btn:hover {
  transform: translateY(-2px);
  background: rgba(76, 175, 80, 0.16);
}

.input-row {
  display: flex;
  gap: 12px;
}

.ai-input {
  flex: 1;
  border: 1px solid rgba(76, 175, 80, 0.18);
  background: #fff;
  height: 52px;
  border-radius: 16px;
  padding: 0 16px;
  outline: none;
  color: #2f3b30;
  font-size: 15px;
  transition: all 0.3s ease-in-out;
}

.ai-input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.10);
}

.send-btn {
  border: none;
  background: #4caf50;
  color: #fff;
  min-width: 120px;
  height: 52px;
  border-radius: 16px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 12px 22px rgba(76, 175, 80, 0.22);
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.send-btn:disabled {
  background: #9dbf9e;
  cursor: not-allowed;
  box-shadow: none;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease-in-out;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 220px;
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

@media (max-width: 1200px) {
  .tool-detail,
  .video-layout {
    grid-template-columns: 1fr;
  }

  .ai-bottom-bar {
    width: calc(100vw - 360px);
  }
}

@media (max-width: 900px) {
  .learning-page {
    padding: 20px 16px 150px;
  }

  .hero-title {
    font-size: 28px;
  }

  .quiz-options {
    grid-template-columns: 1fr;
  }

  .ai-bottom-bar {
    width: calc(100vw - 32px);
    left: 16px;
    right: 16px;
    transform: none;
  }
}
</style>