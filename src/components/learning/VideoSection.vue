<template>
  <div class="video-section">

    <!-- 标题 -->
    <div class="section-header">
      <h2>🎬 农业视频推荐</h2>
      <button class="refresh-btn" @click="refreshVideos">🔄 换一批</button>
    </div>

    <!-- 视频列表（固定6个） -->
    <div class="video-grid">
      <div
        v-for="video in visibleVideos"
        :key="video.id"
        class="video-card"
        @click="playVideo(video)"
      >
        <div class="video-cover">
          <img :src="video.cover" />
          <div class="play-btn">▶</div>
        </div>

        <div class="video-info">
          <div class="video-title">{{ video.title }}</div>
          <div class="video-author">{{ video.author }}</div>
        </div>
      </div>
    </div>

    <!-- 播放弹窗 -->
    <div v-if="currentBvid" class="video-modal" @click.self="closeVideo">
      <div class="video-player">
        <iframe
          :src="`https://player.bilibili.com/player.html?bvid=${currentBvid}`"
          frameborder="0"
          allowfullscreen
        ></iframe>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const allVideos = ref([])
const visibleVideos = ref([])
const currentBvid = ref(null)

// ===== 视频池（稳定）=====
const generateVideos = () => {
  const titles = [
    '智慧农业系统解析',
    '草莓种植全过程',
    '水稻是怎么种出来的',
    '无人机如何喷洒农药',
    '现代农业灌溉技术',
    '大棚种植技巧',
    '农场自动化设备',
    '农作物生长周期讲解',
    '农业机械使用指南',
    '农田管理技巧'
  ]

  return titles.map((title, i) => ({
    id: i,
    bvid: 'BV1xK4y1C7yH', // 可播放
    title,
    author: '农业频道',
    cover: `https://picsum.photos/400/300?random=${i + Math.random()}`
  }))
}

// ===== 换一批（核心）=====
const refreshVideos = () => {
  allVideos.value = generateVideos().sort(() => Math.random() - 0.5)
  visibleVideos.value = allVideos.value.slice(0, 6)
}

// ===== 播放 =====
const playVideo = (video) => {
  currentBvid.value = video.bvid
}

const closeVideo = () => {
  currentBvid.value = null
}

// ===== 初始化 =====
onMounted(() => {
  refreshVideos()
})
</script>

<style scoped>

/* ================== 整体 ================== */

.video-section {
  margin: 0;
  margin-bottom: 140px;
  padding: 16px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.05);
}

/* ================== 标题 ================== */

.section-header {
  display: block;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
}

.refresh-btn {
  background: #4caf50;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
}

/* ================== 网格 ================== */

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

/* ================== 卡片 ================== */

.video-card {
  border-radius: 16px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: 0.25s;
}

.video-card:hover {
  transform: translateY(-6px);
}

/* ================== 封面 ================== */

.video-cover {
  aspect-ratio: 16/9;
  position: relative;
}

.video-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 播放按钮 */
.play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0,0,0,0.5);
  color: #fff;
  padding: 8px 12px;
  border-radius: 50%;
}

/* ================== 信息 ================== */

.video-info {
  padding: 10px;
}

.video-title {
  font-size: 14px;
  font-weight: 600;
}

.video-author {
  font-size: 12px;
  color: #888;
}

/* ================== 播放弹窗 ================== */

.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-player {
  width: 80%;
  max-width: 900px;
  aspect-ratio: 16/9;
}

.video-player iframe {
  width: 100%;
  height: 100%;
}

/* ================== 手机 ================== */

@media (max-width: 900px) {
  .video-grid {
    grid-template-columns: 1fr;
  }
}
</style>