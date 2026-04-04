<template>
  <!-- 农具讲解 -->
  <section class="content-card tool-section">
    <div class="section-title-row">
      <h2 class="section-title">🌾 农具讲解</h2>
      <span class="section-subtitle">
        点击卡片可切换农具，点击按钮可联动 AI
      </span>
    </div>

    <!-- 卡片 -->
    <div class="tool-scroll">
      <div
        v-for="item in filteredTools"
        :key="item.id"
        class="tool-card"
        :class="{ selected: currentTool.id === item.id }"
        @click="$emit('selectTool', item)"
      >
        <div class="tool-image-wrap">
          <img :src="item.image" :alt="item.name" class="tool-image" />
        </div>
        <div class="tool-name">{{ item.name }}</div>
        <div class="tool-tag">{{ item.tag }}</div>
      </div>
    </div>

    <!-- 详情 -->
    <transition name="fade-slide" mode="out-in">
      <div class="tool-detail" :key="currentTool.id">

        <!-- 左 -->
        <div class="tool-detail-left">
          <div class="tool-main-image-box">
            <img
              :src="currentTool.image"
              :alt="currentTool.name"
              class="tool-main-image"
            />
          </div>
        </div>

        <!-- 右 -->
        <div class="tool-detail-right">

          <div class="tool-title-line">
            <h3 class="tool-title">{{ currentTool.name }}</h3>
            <span class="tool-level">{{ currentTool.level }}</span>
          </div>

          <p class="tool-usage">{{ currentTool.usage }}</p>

          <div class="tool-point-list">
            <div
              class="tool-point"
              v-for="(point, index) in currentTool.points"
              :key="index"
            >
              <span class="point-dot"></span>
              <span>{{ point }}</span>
            </div>
          </div>

          <div class="tool-action-row">
            <button class="primary-btn" @click="$emit('toggleDetail')">
              {{ showDetail ? '收起详细' : '查看详细' }}
            </button>

            <button
              class="ghost-btn"
              @click="$emit('askToolMore', currentTool)"
            >
              🤖 问 AI 更多
            </button>
          </div>

          <!-- 展开 -->
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
</template>

<script setup>
defineProps({
  filteredTools: Array,
  currentTool: Object,
  showDetail: Boolean
})

defineEmits([
  'selectTool',
  'toggleDetail',
  'askToolMore'
])
</script>

<style scoped>
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
}

.tool-card.selected {
  border-color: #4caf50;
}

.tool-image-wrap {
  width: 100%;
  height: 120px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 12px;
}

.tool-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tool-name {
  font-size: 18px;
  font-weight: 800;
}

.tool-tag {
  margin-top: 6px;
  font-size: 13px;
}

.tool-detail {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

.tool-main-image-box {
  height: 260px;
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
}

.tool-title {
  font-size: 30px;
}

.tool-level {
  background: rgba(76, 175, 80, 0.12);
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 12px;
}

.tool-usage {
  line-height: 1.9;
}

.tool-point-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tool-point {
  display: flex;
  gap: 10px;
}

.point-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4caf50;
}

.tool-action-row {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.tool-detail-panel {
  margin-top: 18px;
}
</style>