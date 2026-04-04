<template>
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
          <button class="robot-btn" @click="$emit('askKnowledge', item)">🤖</button>
        </div>
      </div>
    </section>
</template>

<script setup>
defineProps({
  knowledgeList: Array
})

defineEmits(['askKnowledge'])
</script>

<style scoped>
.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.knowledge-item {
  display: flex;
  justify-content: space-between;
  padding: 18px;
  border-radius: 18px;
}

.knowledge-title {
  font-size: 18px;
  font-weight: 800;
}

.knowledge-desc {
  margin-top: 6px;
}

.robot-btn {
  width: 48px;
  height: 48px;
  border-radius: 16px;
}
</style>