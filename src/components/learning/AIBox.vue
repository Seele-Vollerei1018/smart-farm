<template>
  <!-- ================= 聊天记录 ================= -->
  <section class="content-card chat-history-section">
    <div class="section-title-row">
      <h2 class="section-title">💬 AI 对话记录</h2>
      <button class="clear-btn" @click="$emit('clearChat')">🗑️ 清空对话</button>
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

  <!-- ================= 底部安全区 ================= -->
  <div class="bottom-safe-space"></div>

  <!-- ================= 底部输入框（你这段） ================= -->
  <div class="ai-bottom-bar">

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
.chat-history-section {
  display: flex;
  flex-direction: column;
}

.chat-list {
  max-height: 360px;
  overflow-y: auto;
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
  padding: 14px;
  border-radius: 18px;
}

.chat-item.user .bubble {
  background: #4caf50;
  color: #fff;
}

.chat-item.ai .bubble {
  background: #fff;
}

.bottom-safe-space {
  height: 90px;
}

/* ✅ ① 压缩整体高度 */
.ai-bottom-bar {
  position: fixed;
  bottom: 20px;

  left: 260px;
  right: 360px;

  width: auto;

  padding: 10px 14px;   /* 🔥 16 → 10 */

  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);

  border-radius: 16px;

  box-shadow: 0 10px 30px rgba(0,0,0,0.08);

  z-index: 100;
}

/* ✅ ② 关键：让快捷问题和输入框分开 */
.quick-question-row {
  margin-bottom: 8px;   /* 🔥 核心 */
}

/* 快捷按钮 */
.quick-btn {
  background: #fff;
  border: 1px solid rgba(76,175,80,0.2);
  padding: 6px 12px;   /* 🔥 略微压缩 */
  border-radius: 999px;
  cursor: pointer;
}

.quick-btn:hover {
  background: #f3faf3;
}

/* 输入框 */
.input-row {
  display: flex;
  gap: 6px;
  width: 100%;
}

.ai-input {
  flex: 1;
  min-width: 0;

  height: 38px;   /* 🔥 46 → 38 */

  padding: 0 12px;  /* 🔥 去掉上下 padding */

  border-radius: 12px;

  border: 1px solid #ddd;
  outline: none;

  background: #fff;

  font-size: 14px;

  transition: all 0.2s;
}

.ai-input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76,175,80,0.15);
}

.send-btn {
  flex-shrink: 0;
  height: 38px;   /* 🔥 对齐输入框 */
}
</style>