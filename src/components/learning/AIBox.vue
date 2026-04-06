<template>
  <!-- ✅ 一个完整卡片 -->
  <section class="content-card chat-history-section">

    <!-- 标题 -->
    <div class="section-title-row">
      <h2 class="section-title">💬 AI 对话记录</h2>
      <button class="clear-btn" @click="$emit('clearChat')">🗑️ 清空对话</button>
    </div>

    <!-- 聊天内容 -->
    <div class="chat-list" ref="chatListRef">
      <div v-if="messages.length === 0" class="chat-empty">
        还没有提问，试试点击“问 AI 更多”或者使用下方输入框。
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

    <!-- ✅ 快捷问题（移进卡片） -->
    <div class="quick-question-row">
      <button class="quick-btn" @click="$emit('quickAsk', '💡 农具怎么用？')">
        💡 农具怎么用？
      </button>
      <button class="quick-btn" @click="$emit('quickAsk', '🌱 作物怎么种？')">
        🌱 作物怎么种？
      </button>
      <button class="quick-btn" @click="$emit('quickAsk', '🧱 为什么要松土？')">
        🧱 为什么要松土？
      </button>
    </div>

    <!-- ✅ 输入框（移进卡片） -->
    <div class="ai-bottom-bar">
      <div class="input-row">
        <input
          :value="input"
          class="ai-input"
          placeholder="问点农业问题，比如：锄头为什么适合松土？"
          @input="$emit('update:input', $event.target.value)"
          @keydown.enter="$emit('sendMessage')"
        />

        <button
          class="send-btn"
          @click="$emit('sendMessage')"
          :disabled="isTyping"
        >
          {{ isTyping ? '思考中...' : '发送' }}
        </button>
      </div>
    </div>

  </section>
</template>

<script setup>
defineProps({
  messages: Array,
  input: String,
  isTyping: Boolean,
  chatListRef: Object,
  renderMarkdown: Function
})

defineEmits([
  'sendMessage',
  'quickAsk',
  'clearChat',
  'update:input'
])
</script>

<style scoped>

/* ================== 整体卡片 ================== */

.chat-history-section {
  display: flex;
  flex-direction: column;
  padding: 18px 20px;

  background: #ffffff;
  border-radius: 16px;

  box-shadow: 0 6px 18px rgba(0,0,0,0.05);
  border: 1px solid rgba(0,0,0,0.04);
}

/* ================== 聊天区域 ================== */

.chat-list {
  min-height: 140px;   /* ⭐关键：预留空间 */
  max-height: 260px;
  overflow-y: auto;

  padding: 12px 6px;
}

/* 空状态 */
.chat-empty {
  color: #8aa095;
  font-size: 14px;
  line-height: 1.6;
}

/* ================== 聊天气泡 ================== */

.chat-item {
  display: flex;
  margin-bottom: 12px;
}

.chat-item.user {
  justify-content: flex-end;
}

.chat-item.ai {
  justify-content: flex-start;
}

.bubble {
  max-width: 70%;
  padding: 12px 14px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.6;
}

/* 用户气泡 */
.chat-item.user .bubble {
  background: #4caf50;
  color: #fff;
}

/* AI气泡 */
.chat-item.ai .bubble {
  background: #f6f8f7;
  color: #2f3e2f;
}

/* ================== 快捷问题 ================== */

.quick-question-row {
  margin: 10px 0 6px;
}

/* 按钮统一风格 */
.quick-btn {
  background: #f6fbf7;
  border: 1px solid rgba(76,175,80,0.25);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-btn:hover {
  background: #eaf6ee;
}

/* ================== 输入区域 ================== */

.ai-bottom-bar {
  margin: 0;
}

/* 输入行 */
.input-row {
  display: flex;
  gap: 8px;
}

/* 输入框 */
.ai-input {
  flex: 1;
  height: 38px;
  padding: 0 12px;

  border-radius: 12px;
  border: 1px solid #e0e6e2;

  background: #f9fbfa;
  font-size: 14px;

  transition: all 0.2s;
}

.ai-input:focus {
  border-color: #4caf50;
  background: #fff;
  box-shadow: 0 0 0 2px rgba(76,175,80,0.12);
}

/* 发送按钮 */
.send-btn {
  flex-shrink: 0;
  height: 38px;
  padding: 0 14px;

  border-radius: 10px;
  border: none;

  background: #4caf50;
  color: #fff;
  font-size: 13px;
  cursor: pointer;

  transition: all 0.2s;
}

.send-btn:hover {
  background: #43a047;
}

.send-btn:disabled {
  background: #a5d6a7;
  cursor: not-allowed;
}

</style>