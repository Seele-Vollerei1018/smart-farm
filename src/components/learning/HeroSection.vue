<template>
  <section class="hero-section">
   
     <!-- 顶部标题 -->
    
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
</template>

<script setup>
defineProps({
  tabs: Array,
  activeTab: String
})
</script>

<style scoped>
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
</style>