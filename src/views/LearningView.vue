<script setup>
const articles = [
  {
    title: '温室环境参数与作物生长的关系',
    excerpt: '温度、湿度、光照与 CO₂ 浓度如何协同影响光合效率与产量。',
    tag: '基础',
    mins: 6,
  },
  {
    title: '营养液 pH 与 EC 的日常管理',
    excerpt: '简易校准流程、常见漂移原因与调整策略，降低肥害风险。',
    tag: '水培',
    mins: 8,
  },
  {
    title: '物联网传感器布点与维护',
    excerpt: '避免盲区与热源干扰，延长探针寿命的检查清单。',
    tag: '硬件',
    mins: 10,
  },
  {
    title: '告警阈值设定与季节性策略',
    excerpt: '从固定阈值到滑动窗口，减少误报的同时不漏掉风险。',
    tag: '运维',
    mins: 7,
  },
]
</script>

<template>
  <div class="learn">
    <header class="learn-head">
      <div>
        <h2 class="learn-title">学习园地</h2>
        <p class="learn-sub">精选农业物联网与温室管理短文 · 内容可后续接入 CMS 或接口</p>
      </div>
    </header>

    <div class="article-grid">
      <article v-for="(a, i) in articles" :key="i" class="proto-card article-card">
        <span class="article-tag">{{ a.tag }}</span>
        <h3 class="article-title">{{ a.title }}</h3>
        <p class="article-excerpt">{{ a.excerpt }}</p>
        <div class="article-meta">
          <span>约 {{ a.mins }} 分钟阅读</span>
          <button type="button" class="linkish">查看详情</button>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.learn {
  max-width: 1100px;
  margin: 0 auto;
}

.learn-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f5132;
  margin: 0 0 0.35rem;
}

.learn-sub {
  margin: 0 0 1.25rem;
  font-size: 0.88rem;
  color: rgba(26, 46, 36, 0.65);
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.article-card {
  padding: 1.2rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  min-height: 200px;
}

.article-tag {
  align-self: flex-start;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #0a58ca;
  background: rgba(13, 110, 253, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.article-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: #143d2e;
  line-height: 1.35;
}

.article-excerpt {
  margin: 0;
  flex: 1;
  font-size: 0.88rem;
  line-height: 1.55;
  color: rgba(26, 46, 36, 0.75);
}

.article-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  font-size: 0.78rem;
  color: rgba(26, 46, 36, 0.5);
}

.linkish {
  border: none;
  background: none;
  padding: 0;
  font: inherit;
  font-weight: 700;
  color: #198754;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.linkish:hover {
  color: #146c43;
}

@media (max-width: 720px) {
  .article-grid {
    grid-template-columns: 1fr;
  }
}
</style>
