<template>
  <section class="hero-section">
    <div class="hero-kicker">fun learning</div>
    <h1 class="hero-title">轻松学农业知识</h1>
    <p class="hero-desc">
      通过图文讲解、视频推荐和 AI 问答，帮助用户更轻松地理解农业知识。
    </p>
  </section>
</template>

<script setup>
</script>

<style scoped>
.hero-section {
  margin-bottom: 24px;
}

.hero-kicker {
  font-size: 14px;
  color: #7c8f81;
  margin-bottom: 8px;
  font-weight: 500;
}

.hero-title {
  margin: 0 0 10px;
  font-size: 38px;
  line-height: 1.1;
  font-weight: 800;
  color: #223228;
  letter-spacing: -1px;
}

.hero-desc {
  margin: 0;
  font-size: 16px;
  line-height: 1.7;
  color: #5f7062;
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

  .hero-desc {
    font-size: 15px;
    line-height: 1.6;
  }
}
</style>