<template>
  <div class="video-section">

    <!-- 标题 -->
    <div class="section-header">
      <h1>🎬 农业视频推荐</h1>
      <button class="refresh-btn" @click="refreshVideos">换一批</button>
    </div>

    <!-- 视频列表 -->
    <div class="video-grid">
      <div
        v-for="video in visibleVideos"
        :key="video.id"
        class="video-card"
        @click="playVideo(video)"
      >
        <div class="video-cover">
          <img :src="video.cover" loading="lazy" />
          <div class="play-btn">▶</div>
        </div>

        <div class="video-info">
          <div class="video-title">{{ video.title }}</div>
          <div class="video-author">{{ video.author }}</div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const allVideos = ref([])
const visibleVideos = ref([])

// ===== 视频数据 =====
// ===== 视频数据（本地稳定版）=====
const generateVideos = () => {
  const videoSource = [
    {
      bvid: 'BV16A411N7Qk',
      title: '栽培一株好苗，为阳台菜园做好准备',
      cover: new URL('@/assets/bilibili/1.png', import.meta.url).href
    },
    {
      bvid: 'BV1SZ4y1s7x7', // ✅ 修正（原来错）
      title: '发芽！植物一生的开始',
      cover: new URL('@/assets/bilibili/2.png', import.meta.url).href
    },
    {
      bvid: 'BV1VP4y1R72v', // ✅ 修正
      title: '从零开始种番茄',
      cover: new URL('@/assets/bilibili/3.png', import.meta.url).href
    },
    {
      bvid: 'BV1XL411a7Jk',
      title: '生菜，从播种到收获全过程',
      cover: new URL('@/assets/bilibili/4.png', import.meta.url).href
    },
    {
      bvid: 'BV1aZXMYDEnJ', // ✅ 修正（完全错的）
      title: '不可思议的种子生长过程',
      cover: new URL('@/assets/bilibili/5.png', import.meta.url).href
    },
    {
      bvid: 'BV1yUQgYrEfQ', // ✅ 修正
      title: '胡萝卜切下来会发生什么？',
      cover: new URL('@/assets/bilibili/6.png', import.meta.url).href
    },
    {
      bvid: 'BV1vc41167yM',
      title: '中国饭碗（农业纪录）',
      cover: new URL('@/assets/bilibili/7.png', import.meta.url).href
    },
    {
      bvid: 'BV1U3K7z8EwE', // ✅ 修正
      title: '相信土地的力量（农业主题）',
      cover: new URL('@/assets/bilibili/8.png', import.meta.url).href
    }
  ]

  return videoSource.map((item, i) => ({
    id: i,
    ...item,
    author: '农业科普'
  }))
}

// ===== 换一批 =====
const refreshVideos = () => {
  allVideos.value = generateVideos().sort(() => Math.random() - 0.5)
  visibleVideos.value = allVideos.value.slice(0, 6)
}

// ===== 点击跳转B站 =====
const playVideo = (video) => {
  window.open(
    `https://www.bilibili.com/video/${video.bvid}`,
    '_blank'
  )
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
  padding: 16px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.05);
}

/* ================== 标题 ================== */

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h1 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
}

.refresh-btn {
  background: #25c18f;
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

/* ================== 手机适配 ================== */

@media (max-width: 900px) {
  .video-grid {
    grid-template-columns: 1fr;
  }
}
</style>