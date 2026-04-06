<template>
  <!-- 🌱 初级 -->
  <section
    v-if="level === 'primary'"
    class="content-card tool-section primary-container"
  >
    <!-- 第 1 页：农具讲解 -->
    <div v-if="currentPage === 0" class="category-page">
      <div class="section-title-row">
        <h2 class="section-title">🌾 农具讲解（1/3）</h2>
      </div>

      <div class="tool-scroll-shell">
        <button
          class="inner-scroll-btn inner-left"
          type="button"
          @click.stop="scrollLeft"
        >
          ‹
        </button>

        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="toolScrollRef">
            <div
              v-for="item in filteredTools"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="$emit('selectTool', item)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>

        <button
          class="inner-scroll-btn inner-right"
          type="button"
          @click.stop="scrollRight"
        >
          ›
        </button>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img
                :src="currentTool.image"
                :alt="currentTool.name"
                class="tool-main-image"
              />
            </div>
          </div>

          <div class="tool-detail-right">
            <div class="tool-title-line">
              <h3 class="tool-title">{{ currentTool.name }}</h3>
              <span class="tool-level">{{ currentTool.level }}</span>
            </div>

            <p class="tool-usage">{{ currentTool.usage }}</p>

            <div class="tool-point-list">
              <div
                v-for="(point, index) in currentTool.points"
                :key="index"
                class="tool-point"
              >
                <span class="point-dot"></span>
                <span>{{ point }}</span>
              </div>
            </div>

            <div class="tool-action-row">
              <button class="primary-btn" @click="$emit('toggleDetail')">
                {{ showDetail ? '收起详细' : '查看详细' }}
              </button>

              <button class="ghost-btn" @click="$emit('askToolMore', currentTool)">
                🤖 问 AI 更多
              </button>
            </div>

            <transition name="expand">
              <div v-if="showDetail" class="tool-detail-panel">
                <h4>农具小百科</h4>
                <p>{{ currentTool.detail }}</p>
              </div>
            </transition>
          </div>
        </div>
      </transition>
    </div>

    <!-- 第 2 页：农场萌友 -->
    <div v-if="currentPage === 1" class="category-page">
      <div class="section-title-row">
        <h2 class="section-title">🐥 农场萌友（2/3）</h2>
      </div>

      <div class="tool-scroll-shell">
        <button
          class="inner-scroll-btn inner-left"
          type="button"
          @click.stop="scrollLeft"
        >
          ‹
        </button>

        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="animalScrollRef">
            <div
              v-for="item in animals"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="$emit('selectTool', item)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>

        <button
          class="inner-scroll-btn inner-right"
          type="button"
          @click.stop="scrollRight"
        >
          ›
        </button>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img
                :src="currentTool.image"
                :alt="currentTool.name"
                class="tool-main-image"
              />
            </div>
          </div>

          <div class="tool-detail-right">
            <div class="tool-title-line">
              <h3 class="tool-title">{{ currentTool.name }}</h3>
              <span class="tool-level">{{ currentTool.level }}</span>
            </div>

            <p class="tool-usage">{{ currentTool.usage }}</p>

            <div class="tool-point-list">
              <div
                v-for="(point, index) in currentTool.points"
                :key="index"
                class="tool-point"
              >
                <span class="point-dot"></span>
                <span>{{ point }}</span>
              </div>
            </div>

            <div class="tool-action-row">
              <button class="ghost-btn" @click="$emit('askToolMore', currentTool)">
                🤖 问 AI 更多
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 第 3 页：神奇植物 -->
    <div v-if="currentPage === 2" class="category-page">
      <div class="section-title-row">
        <h2 class="section-title">🌿 神奇植物（3/3）</h2>
      </div>

      <div class="tool-scroll-shell">
        <button
          class="inner-scroll-btn inner-left"
          type="button"
          @click.stop="scrollLeft"
        >
          ‹
        </button>

        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="plantScrollRef">
            <div
              v-for="item in plants"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="$emit('selectTool', item)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>

        <button
          class="inner-scroll-btn inner-right"
          type="button"
          @click.stop="scrollRight"
        >
          ›
        </button>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img
                :src="currentTool.image"
                :alt="currentTool.name"
                class="tool-main-image"
              />
            </div>
          </div>

          <div class="tool-detail-right">
            <div class="tool-title-line">
              <h3 class="tool-title">{{ currentTool.name }}</h3>
              <span class="tool-level">{{ currentTool.level }}</span>
            </div>

            <p class="tool-usage">{{ currentTool.usage }}</p>

            <div class="tool-point-list">
              <div
                v-for="(point, index) in currentTool.points"
                :key="index"
                class="tool-point"
              >
                <span class="point-dot"></span>
                <span>{{ point }}</span>
              </div>
            </div>

            <div class="tool-action-row">
              <button class="ghost-btn" @click="$emit('askToolMore', currentTool)">
                🤖 问 AI 更多
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 外层大按钮 -->
    <button
      v-if="currentPage > 0"
      class="nav-btn nav-left"
      type="button"
      @click="$emit('changePage', currentPage - 1)"
    >
      ◀
    </button>

    <button
      v-if="currentPage < 2"
      class="nav-btn nav-right"
      type="button"
      @click="$emit('changePage', currentPage + 1)"
    >
      ▶
    </button>

    <div class="dots">
      <span
        v-for="i in 3"
        :key="i"
        :class="{ active: currentPage === i - 1 }"
      ></span>
    </div>
  </section>

  <!-- 🌿 中级 -->
  <section
    v-else-if="level === 'middle'"
    class="content-card tool-section primary-container"
  >
    <!-- 第1页 -->
    <div v-if="currentPage === 0" class="category-page">
      <div class="section-title-row">
        <h2 class="section-title">🌸 四季农事（1/3）</h2>
      </div>

      <div class="tool-scroll-shell">
        <button
          class="inner-scroll-btn inner-left"
          type="button"
          @click.stop="scrollLeft"
        >
          ‹
        </button>

        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="middleScrollRef">
            <div
              v-for="item in seasons"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="$emit('selectTool', item)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>

        <button
          class="inner-scroll-btn inner-right"
          type="button"
          @click.stop="scrollRight"
        >
          ›
        </button>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img :src="currentTool.image" :alt="currentTool.name" class="tool-main-image" />
            </div>
          </div>

          <div class="tool-detail-right">
            <div class="tool-title-line">
              <h3 class="tool-title">{{ currentTool.name }}</h3>
              <span class="tool-level">{{ currentTool.level }}</span>
            </div>

            <p class="tool-usage">{{ currentTool.usage }}</p>

            <div class="tool-point-list">
              <div v-for="(p, i) in currentTool.points" :key="i" class="tool-point">
                <span class="point-dot"></span>
                <span>{{ p }}</span>
              </div>
            </div>

            <div class="tool-action-row">
              <button class="ghost-btn" @click="$emit('askToolMore', currentTool)">
                🤖 问 AI 更多
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 第2页 -->
    <div v-if="currentPage === 1" class="category-page">
      <div class="section-title-row">
        <h2 class="section-title">🌾 二十四节气（2/3）</h2>
      </div>

      <div class="tool-scroll-shell">
        <button
          class="inner-scroll-btn inner-left"
          type="button"
          @click.stop="scrollLeft"
        >
          ‹
        </button>

        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="cultureScrollRef">
            <div
              v-for="item in solarTerms"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="$emit('selectTool', item)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>

        <button
          class="inner-scroll-btn inner-right"
          type="button"
          @click.stop="scrollRight"
        >
          ›
        </button>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img :src="currentTool.image" :alt="currentTool.name" class="tool-main-image" />
            </div>
          </div>

          <div class="tool-detail-right">
            <div class="tool-title-line">
              <h3 class="tool-title">{{ currentTool.name }}</h3>
              <span class="tool-level">{{ currentTool.level }}</span>
            </div>

            <p class="tool-usage">{{ currentTool.usage }}</p>

            <div class="tool-point-list">
              <div v-for="(p, i) in currentTool.points" :key="i" class="tool-point">
                <span class="point-dot"></span>
                <span>{{ p }}</span>
              </div>
            </div>

            <div class="tool-action-row">
              <button class="ghost-btn" @click="$emit('askToolMore', currentTool)">
                🤖 问 AI 更多
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 第3页 -->
    <div v-if="currentPage === 2" class="category-page">
      <div class="section-title-row">
        <h2 class="section-title">🌍 地域农业（3/3）</h2>
      </div>

      <div class="tool-scroll-shell">
        <button
          class="inner-scroll-btn inner-left"
          type="button"
          @click.stop="scrollLeft"
        >
          ‹
        </button>

        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="regionScrollRef">
            <div
              v-for="item in regions"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="$emit('selectTool', item)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>

        <button
          class="inner-scroll-btn inner-right"
          type="button"
          @click.stop="scrollRight"
        >
          ›
        </button>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img :src="currentTool.image" :alt="currentTool.name" class="tool-main-image" />
            </div>
          </div>

          <div class="tool-detail-right">
            <div class="tool-title-line">
              <h3 class="tool-title">{{ currentTool.name }}</h3>
              <span class="tool-level">{{ currentTool.level }}</span>
            </div>

            <p class="tool-usage">{{ currentTool.usage }}</p>

            <div class="tool-point-list">
              <div v-for="(p, i) in currentTool.points" :key="i" class="tool-point">
                <span class="point-dot"></span>
                <span>{{ p }}</span>
              </div>
            </div>

            <div class="tool-action-row">
              <button class="ghost-btn" @click="$emit('askToolMore', currentTool)">
                🤖 问 AI 更多
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <button
      v-if="currentPage > 0"
      class="nav-btn nav-left"
      type="button"
      @click="$emit('changePage', currentPage - 1)"
    >
      ◀
    </button>

    <button
      v-if="currentPage < 2"
      class="nav-btn nav-right"
      type="button"
      @click="$emit('changePage', currentPage + 1)"
    >
      ▶
    </button>

    <div class="dots">
      <span
        v-for="i in 3"
        :key="i"
        :class="{ active: currentPage === i - 1 }"
      ></span>
    </div>
  </section>


<!-- 🤖 高级（统一卡片结构） -->
<section v-else class="content-card tool-section primary-container">
  <div class="section-title-row">
    <h2 class="section-title">🤖 智慧农业系统</h2>
  </div>

  <div class="tool-scroll-shell">
    <button class="inner-scroll-btn inner-left" @click.stop="scrollLeft">‹</button>

    <div class="tool-scroll-viewport">
      <div class="tool-scroll" ref="advancedScrollRef">
        <div
          v-for="item in advancedItems"
          :key="item.id"
          class="tool-card"
          :class="{ selected: currentTool?.id === item.id }"
          @click="$emit('selectTool', item)"
        >
          <div class="tool-image-wrap">
            <img :src="item.image" class="tool-image" />
          </div>
          <div class="tool-name">{{ item.name }}</div>
          <div class="tool-tag">{{ item.tag }}</div>
        </div>
      </div>
    </div>

    <button class="inner-scroll-btn inner-right" @click.stop="scrollRight">›</button>
  </div>

  <!-- ✅ 详情区（关键！） -->
  <transition name="fade-slide">
    <div v-if="currentTool" class="tool-detail">
      <div class="tool-detail-left">
        <div class="tool-main-image-box">
          <img :src="currentTool.image" class="tool-main-image" />
        </div>
      </div>

      <div class="tool-detail-right">
        <div class="tool-title-line">
          <h3 class="tool-title">{{ currentTool.name }}</h3>
        </div>

        <p class="tool-usage">{{ currentTool.usage }}</p>

        <div class="tool-point-list">
          <div v-for="(p,i) in currentTool.points" :key="i" class="tool-point">
            <span class="point-dot"></span>
            <span>{{ p }}</span>
          </div>
        </div>

        <div class="tool-action-row">
          <button class="ghost-btn" @click="$emit('askToolMore', currentTool)">
            🤖 问 AI 更多
          </button>
        </div>
      </div>
    </div>
  </transition>
</section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  level: String,
  filteredTools: { type: Array, default: () => [] },
  animals: { type: Array, default: () => [] },
  plants: { type: Array, default: () => [] },
  seasons: { type: Array, default: () => [] },
  solarTerms: { type: Array, default: () => [] },
  regions: { type: Array, default: () => [] },
  
  currentTool: { type: Object, default: null },
  showDetail: { type: Boolean, default: false },
  advancedItems: { type: Array, default: () => [] },
  currentPage: { type: Number, default: 0 }
})

const emit = defineEmits([
  'selectTool',
  'changePage',
  'askToolMore',
  'toggleDetail'
])

const toolScrollRef = ref(null)
const animalScrollRef = ref(null)
const plantScrollRef = ref(null)
const middleScrollRef = ref(null)
const cultureScrollRef = ref(null)
const regionScrollRef = ref(null)
const highTechScrollRef = ref(null)
const highEcoScrollRef = ref(null)
const advancedScrollRef = ref(null)
const scrollLeft = () => {
  let el = null

  if (props.level === 'advanced') {
    el = advancedScrollRef.value
  } else {
    el = document.querySelector('.category-page .tool-scroll')
  }

  if (!el) return
  el.scrollLeft -= 320
}

const scrollRight = () => {
  let el = null

  if (props.level === 'advanced') {
    el = advancedScrollRef.value
  } else {
    el = document.querySelector('.category-page .tool-scroll')
  }

  if (!el) return
  el.scrollLeft += 320
}

const currentHigh = ref(null)




</script>

<style scoped>
.inner-scroll-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);

  z-index: 9999 !important;
  pointer-events: auto !important;

  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;

  background: rgba(255, 255, 255, 0.98);
  color: #4caf50;
  font-size: 26px;

  cursor: pointer;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);

  display: flex;
  align-items: center;
  justify-content: center;
}

/* 左按钮 */
.inner-left {
  left: 10px;
}

/* 右按钮 */
.inner-right {
  right: 10px;
}

/* ====== 关键修复 ====== */

/* 不裁剪按钮 */
.tool-scroll-viewport {
  overflow: visible !important;
  
  pointer-events: auto;
}

/* 滚动层降级 */
.tool-scroll {
  position: relative;
  z-index: 1;
}

/* 按钮抬到最上层 */
.inner-scroll-btn {
  z-index: 9999 !important;
  pointer-events: auto !important;
  position: absolute;
}

/* 防止卡片盖住按钮 */
.tool-card {
  position: relative;
  z-index: 1;
}


.tool-section.primary-container {
  position: relative;
  padding: 24px 28px 20px;
  overflow: visible !important;
  position: relative;
  z-index: 10;
  
}

.category-page {
  width: 100%;
  min-height: 100%;
  overflow: visible;
}

.section-title-row {
  display: flex;
  align-items: center;
  
}

.section-title {
  margin: 0;
  font-size: 24px;
  font-weight: 800;
  color: #253329;
}

.tool-scroll-shell {
  position: relative;
  

  padding-left: 62px;
  padding-right: 96px;   /* ⭐关键：给右按钮留空间 */

  overflow: visible !important;
}

.inner-right {
  right: 56px;
}

.second-scroll-wrap {
  margin-top: 8px;
}

.tool-scroll {
  display: flex;
  gap: 18px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 6px 4px 10px;
  position: relative;
  z-index: 1;
}

.tool-scroll::-webkit-scrollbar {
  display: none;
}

.inner-scroll-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 9999 !important;
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.98);
  color: #4caf50;
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  pointer-events: auto !important;
  display: flex;
  align-items: center;
  justify-content: center;
}



.inner-scroll-btn:hover {
  transform: translateY(-50%) scale(1.06);
}

.tool-card {
  flex: 0 0 300px;
  background: #f8fcf8;
  border: 1px solid rgba(76, 175, 80, 0.12);
  border-radius: 24px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

.tool-card:hover {
  transform: translateY(-4px);
}

.tool-card.selected {
  border-color: #4caf50;
  box-shadow: 0 10px 24px rgba(76, 175, 80, 0.1);
}

.tool-image-wrap {
  width: 100%;
  height: 160px;
  border-radius: 18px;
  overflow: hidden;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #f5f7f5;  /* 👉 给个底色更高级 */
}

.tool-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;   /* ⭐核心 */
}

.tool-name {
  font-size: 18px;
  font-weight: 800;
  color: #233126;
}

.tool-tag {
  margin-top: 8px;
  font-size: 13px;
  color: #6f8571;
}

.tool-detail {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 26px;
  align-items: start;
}

.tool-detail-left,
.tool-detail-right {
  min-width: 0;
}

.tool-main-image-box {
  height: 340px;
  border-radius: 22px;
  overflow: hidden;
}

.tool-main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.tool-title-line {
  display: flex;
  align-items: center;
  gap: 12px;
  
  flex-wrap: wrap;
}

.tool-title {
  margin: 0;
  font-size: 30px;
  font-weight: 800;
  color: #233126;
}

.tool-level {
  background: rgba(76, 175, 80, 0.12);
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 12px;
  color: #39713b;
}

.tool-usage {
  line-height: 1.9;
  margin: 12px 0 18px;
  color: #34423a;
}

.tool-point-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tool-point {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  color: #34423a;
}

.point-dot {
  width: 8px;
  height: 8px;
  margin-top: 8px;
  border-radius: 50%;
  background: #4caf50;
  flex-shrink: 0;
}

.tool-action-row {
  display: flex;
  gap: 12px;
  margin-top: 18px;
  flex-wrap: wrap;
}

.primary-btn,
.ghost-btn {
  padding: 10px 18px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  transition: 0.25s ease;
}

.primary-btn {
  border: none;
  background: #4caf50;
  color: #fff;
}

.primary-btn:hover {
  opacity: 0.92;
}

.ghost-btn {
  border: 1px solid rgba(76, 175, 80, 0.22);
  background: #fff;
  color: #2e7d32;
}

.ghost-btn:hover {
  background: #f3fbf3;
}

.tool-detail-panel {
  margin-top: 18px;
  padding: 16px 18px;
  border-radius: 16px;
  background: #f7fbf7;
}

.tool-detail-panel h4 {
  margin: 0 0 10px;
  color: #253329;
}

.tool-detail-panel p {
  margin: 0;
  line-height: 1.8;
  color: #34423a;
}

.nav-btn {
  position: absolute;
  top: calc(50% + 60px);
  z-index: 9998;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(76, 175, 80, 0.16);
  background: rgba(255, 255, 255, 0.96);
  color: #2e7d32;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-left {
  left: 10px;
}

.nav-right {
  right: 10px;
}

.nav-btn:hover {
  background: #4caf50;
  color: #fff;
}

.dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 18px;
}

.dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(76, 175, 80, 0.22);
  transition: all 0.25s ease;
}

.dots span.active {
  width: 22px;
  border-radius: 4px;
  background: #4caf50;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease-in-out;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 240px;
}

@media (max-width: 1200px) {
  .tool-detail {
    grid-template-columns: 1fr;
  }

  .nav-btn {
    top: auto;
    bottom: 64px;
  }
}

@media (max-width: 768px) {
  .tool-section.primary-container {
    padding: 20px 18px 16px;
  }

  .tool-scroll-shell {
    padding: 0 50px;
  }

  .tool-card {
    flex: 0 0 240px;
  }

  .tool-main-image-box {
    height: 260px;
  }

  .section-title {
    font-size: 20px;
  }

  .tool-title {
    font-size: 24px;
  }

  .nav-left {
    left: 6px;
  }

  .nav-right {
    right: 6px;
  }
  
}



</style>