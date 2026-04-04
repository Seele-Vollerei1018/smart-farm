<template>
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
          <button class="ghost-btn" @click="$emit('askVideoAI')">🤖 问 AI 总结视频重点</button>
        </div>
      </div>
    </section>
</template>

<script setup>
defineProps({
  currentTool: Object,
  currentVideoUrl: String
})

defineEmits(['askVideoAI'])
</script>

<style scoped>
.video-layout {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 22px;
}

.video-player-box {
  border-radius: 22px;
  overflow: hidden;
}

.video-frame {
  width: 100%;
  height: 320px;
}

.video-title {
  font-size: 24px;
}

.video-desc {
  line-height: 1.9;
}
</style>