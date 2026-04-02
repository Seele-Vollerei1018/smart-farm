<template>
  <div class="about">
    <header class="about-head">
      <div>
        <h2 class="about-title">关于我们</h2>
        <p class="about-sub">智慧农业监测系统的开发与愿景</p>
      </div>
    </header>
    <section class="proto-card about-content">
      <h3>项目介绍</h3>
      <p>智慧农业监测系统是一个基于Vue 3和Vite开发的前端项目，旨在为农场管理者提供实时的环境监测和设备控制功能。</p>
      <h3>主要功能</h3>
      <ul>
        <li>实时环境数据监测（温度、湿度、光照等）</li>
        <li>设备远程控制（风扇、水泵、补光灯等）</li>
        <li>农场日记管理</li>
        <li>数据趋势分析</li>
        <li>学习资源中心</li>
      </ul>
      <h3>技术栈</h3>
      <p>前端：Vue 3, Vite, Pinia, Vue Router</p>
      <p>后端：可对接各种API接口</p>
    </section>
  </div>
</template>

<style scoped>
.about {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.about-head {
  margin-bottom: 1rem;
}

.about-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #000000;
  margin: 0 0 0.35rem;
}

.about-sub {
  margin: 0;
  font-size: 0.88rem;
  color: rgba(0, 0, 0, 0.65);
}

.about-content {
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.about-content h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #000000;
  margin: 1.5rem 0 0.5rem;
}

.about-content p {
  margin: 0 0 1rem;
  font-size: 0.95rem;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.75);
}

.about-content ul {
  margin: 0 0 1rem;
  padding-left: 1.5rem;
}

.about-content li {
  margin-bottom: 0.5rem;
  color: rgba(0, 0, 0, 0.75);
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
  }
}
</style>
