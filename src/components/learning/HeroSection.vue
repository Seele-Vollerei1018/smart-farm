<template>
  <section class="hero-section">
    <div class="hero-kicker">fun learning</div>
    <h1 class="hero-title">轻松学农业知识</h1>
    <p class="hero-desc">
      通过图文讲解、视频推荐和 AI 问答，更轻松地理解农业知识。
    </p>
  </section>
</template>

<script setup>
</script>

<style scoped>
.hero-kicker {
  font-size: 14px;
  color: #333a;
  margin-bottom: 8px;
  font-weight: 400;
  padding-left: 2px;
  font-size: .8rem;
}

.hero-title {
  margin: 0 0 10px;
  font-size: 2rem;
  line-height: 1.1;
  font-weight: 800;
  letter-spacing: -1px;
}

.hero-desc {
  margin: 0;
  font-size: 1rem;
  line-height: 1.6;
  color: #333a;
}

@media (max-width: 900px) {
  .hero-section {
    margin-bottom: 20px;
  }

  .hero-kicker {
    font-size: 13px;
    margin-bottom: 6px;
  }

  .hero-title {
    font-size: 34px;
    line-height: 1.2;
    letter-spacing: 0;
  }
}
</style>
