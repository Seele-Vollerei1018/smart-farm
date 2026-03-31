<template>
  <div class="home-view">
    <!-- 顶部标题与搜索框同一水平线 -->
    <div class="home-top">
      <div class="title-block">
        <p class="welcome-text">WELCOME BACK</p>
        <h2 class="main-title">你好，今天也来看看农场吧 👋</h2>
      </div>

      <div class="top-search">
        <input type="text" placeholder="搜索农场内容..." />
      </div>
    </div>

    <!-- 三张主卡片 -->
    <div class="hero-grid">
      <div class="hero-card" @click="go('/dashboard')">
        <img
          src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80"
          alt="农场情况"
        />
        <div class="hero-mask"></div>
        <div class="hero-content">
          <h3>农场情况</h3>
          <p>查看整体数据与环境状态</p>
        </div>
      </div>

      <div class="hero-card" @click="go('/control')">
        <img
          src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80"
          alt="我的农场"
        />
        <div class="hero-mask"></div>
        <div class="hero-content">
          <h3>我的农场</h3>
          <p>管理设备、地块与日常事务</p>
        </div>
      </div>

      <div class="hero-card" @click="go('/learning')">
        <img
          src="https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1200&q=80"
          alt="趣味学习"
        />
        <div class="hero-mask"></div>
        <div class="hero-content">
          <h3>趣味学习</h3>
          <p>了解种植知识与农业科普</p>
        </div>
      </div>
    </div>

    <!-- 下方主内容：左侧日记 + 中间IP -->
    <div class="content-grid">
      <section class="diary-panel">
        <div class="panel-head">
          <div>
            <h3>农场日记</h3>
            <p>记录今天的观察、心情和状态</p>
          </div>
          <span class="panel-link">查看更多</span>
        </div>

        <div class="diary-scroll">
          <div class="diary-item" v-for="i in 6" :key="i">
            <div class="diary-thumb"></div>
            <div class="diary-info">
              <div class="diary-title">日记 {{ i }}</div>
              <div class="diary-desc">这里预留给日记接口数据，后续对接增删改查。</div>
            </div>
            <div class="diary-price">¥{{ 100 + i * 20 }}</div>
          </div>
        </div>
      </section>

      <section class="ip-panel">
        <div class="ip-card">
          <div class="ip-avatar-wrap">
            <div class="ip-avatar">IP</div>
          </div>
          <div class="ip-title">农场 IP 形象</div>
          <div class="ip-desc">这里预留给你的角色形象、插画或品牌吉祥物展示位。</div>
          <button class="ip-btn">敬请期待</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const go = (path) => router.push(path)
</script>

<style scoped>
:root {
  --bg-page: #F4F7F6;
  --bg-card: #FFFFFF;
  --primary: #25C18F;
  --text-main: #1E293B;
  --text-sub: #94A3B8;
  --radius-xl: 24px;
  --radius-md: 12px;
  --shadow-soft: 0 10px 30px rgba(15, 23, 42, 0.04);
}

.home-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  overflow: hidden;
  padding: 0;
  min-width: 0;
}

/* 顶部 */
.home-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
}

.title-block {
  min-width: 0;
}

.welcome-text {
  margin: 0 0 10px;
  font-size: 13px;
  letter-spacing: 2px;
  color: var(--text-sub);
}

.main-title {
  margin: 0;
  font-size: 46px;
  line-height: 1.18;
  font-weight: 700;
  color: var(--text-main);
}

.top-search {
  width: 320px;
  flex-shrink: 0;
}

.top-search input {
  width: 100%;
  height: 56px;
  border: none;
  outline: none;
  border-radius: 16px;
  padding: 0 18px;
  background: #eef3f1;
  color: var(--text-main);
  font-size: 14px;
  box-shadow: none;
}

.top-search input::placeholder {
  color: #9aa9b5;
}

/* 三张主卡片 */
.hero-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}

.hero-card {
  position: relative;
  height: 300px;
  border-radius: 24px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--shadow-soft);
  border: none;
  transition: transform 0.28s ease, box-shadow 0.28s ease;
}

.hero-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 38px rgba(15, 23, 42, 0.07);
}

.hero-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transform: scale(1.02);
  filter: saturate(0.95);
}

.hero-mask {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent 55%);
}

.hero-content {
  position: absolute;
  left: 20px;
  right: 20px;
  bottom: 18px;
  color: #fff;
  z-index: 2;
}

.hero-content h3 {
  margin: 0 0 8px;
  font-size: 32px;
  line-height: 1.15;
  font-weight: 700;
}

.hero-content p {
  margin: 0;
  font-size: 15px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.92);
}

/* 下方内容 */
.content-grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) 320px;
  gap: 24px;
}

/* 日记面板 */
.diary-panel {
  min-width: 0;
  min-height: 0;
  background: var(--bg-card);
  border-radius: 24px;
  box-shadow: var(--shadow-soft);
  border: none;
  padding: 24px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.panel-head h3 {
  margin: 0;
  font-size: 30px;
  line-height: 1.2;
  color: var(--text-main);
}

.panel-head p {
  margin: 8px 0 0;
  font-size: 14px;
  color: var(--text-sub);
}

.panel-link {
  color: var(--primary);
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
}

.diary-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding-right: 4px;
}

.diary-item {
  display: grid;
  grid-template-columns: 64px minmax(0, 1fr) auto;
  align-items: center;
  gap: 16px;
  padding: 18px 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.14);
}

.diary-item:last-child {
  border-bottom: none;
}

.diary-thumb {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #d7f5ea, #b7e9d4);
}

.diary-info {
  min-width: 0;
}

.diary-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 8px;
}

.diary-desc {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-sub);
}

.diary-price {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary);
  white-space: nowrap;
}

/* IP 卡 */
.ip-panel {
  min-width: 0;
}

.ip-card {
  height: 100%;
  border-radius: 24px;
  background: linear-gradient(180deg, #202a57 0%, #141b39 100%);
  box-shadow: var(--shadow-soft);
  border: none;
  padding: 28px 24px;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 18px;
}

.ip-avatar-wrap {
  width: 148px;
  height: 148px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2ae3aa, #34c3f1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.ip-avatar {
  width: 118px;
  height: 118px;
  border-radius: 50%;
  background: #ffd37a;
  color: #24324b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
  font-weight: 800;
}

.ip-title {
  font-size: 30px;
  line-height: 1.25;
  font-weight: 700;
}

.ip-desc {
  font-size: 14px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.82);
  max-width: 240px;
}

.ip-btn {
  margin-top: 6px;
  height: 50px;
  padding: 0 28px;
  border: none;
  border-radius: 14px;
  background: var(--primary);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(37, 193, 143, 0.28);
}

/* 平板 */
@media (max-width: 1200px) {
  .main-title {
    font-size: 38px;
  }

  .hero-grid {
    grid-template-columns: 1fr;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .ip-panel {
    height: 320px;
  }
}

/* 手机 / 小程序 */
@media (max-width: 768px) {
  .home-view {
    height: auto;
    overflow: visible;
    gap: 20px;
  }

  .home-top {
    flex-direction: column;
    align-items: stretch;
  }

  .main-title {
    font-size: 30px;
  }

  .top-search {
    width: 100%;
  }

  .hero-grid {
    display: flex;
    gap: 16px;
    overflow-x: auto;
    padding-bottom: 4px;
  }

  .hero-card {
    min-width: 280px;
    height: 260px;
  }

  .content-grid {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .diary-panel {
    min-height: 420px;
  }

  .diary-scroll {
    overflow: visible;
  }

  .diary-item {
    grid-template-columns: 56px minmax(0, 1fr);
  }

  .diary-price {
    grid-column: 2 / 3;
  }

  .ip-panel {
    height: 280px;
  }

  .panel-head h3,
  .hero-content h3,
  .ip-title {
    font-size: 24px;
  }
}
</style>