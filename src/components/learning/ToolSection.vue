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
        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="toolScrollRef" @wheel="handleWheel">
            <div
              v-for="item in filteredTools"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="selectTool(item, $event)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" loading="lazy" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img
                :src="currentTool.image"
                :alt="currentTool.name"
                class="tool-main-image"
                loading="lazy"
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
        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="animalScrollRef" @wheel="handleWheel">
            <div
              v-for="item in animals"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="selectTool(item, $event)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" loading="lazy" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img
                :src="currentTool.image"
                :alt="currentTool.name"
                class="tool-main-image"
                loading="lazy"
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
        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="plantScrollRef" @wheel="handleWheel">
            <div
              v-for="item in plants"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="selectTool(item, $event)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" loading="lazy" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>
      </div>

      <transition name="fade-slide" mode="out-in">
        <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
          <div class="tool-detail-left">
            <div class="tool-main-image-box">
              <img
                :src="currentTool.image"
                :alt="currentTool.name"
                class="tool-main-image"
                loading="lazy"
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
        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="middleScrollRef" @wheel="handleWheel">
            <div
              v-for="item in seasons"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="selectTool(item, $event)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" loading="lazy" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>
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
        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="cultureScrollRef" @wheel="handleWheel">
            <div
              v-for="item in solarTerms"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="selectTool(item, $event)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" loading="lazy" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>
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
        <div class="tool-scroll-viewport">
          <div class="tool-scroll" ref="regionScrollRef" @wheel="handleWheel">
            <div
              v-for="item in regions"
              :key="item.id"
              class="tool-card"
              :class="{ selected: currentTool?.id === item.id }"
              @click="selectTool(item, $event)"
            >
              <div class="tool-image-wrap">
                <img :src="item.image" :alt="item.name" class="tool-image" loading="lazy" />
              </div>
              <div class="tool-name">{{ item.name }}</div>
              <div class="tool-tag">{{ item.tag }}</div>
            </div>
          </div>
        </div>
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
    <div class="tool-scroll-viewport">
      <div class="tool-scroll" ref="advancedScrollRef" @wheel="handleWheel">
        <div
          v-for="item in advancedItems"
          :key="item.id"
          class="tool-card"
          :class="{ selected: currentTool?.id === item.id }"
          @click="$emit('selectTool', item)"
        >
          <div class="tool-image-wrap">
            <img :src="item.image" class="tool-image" loading="lazy" />
          </div>
          <div class="tool-name">{{ item.name }}</div>
          <div class="tool-tag">{{ item.tag }}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ✅ 详情区（关键！） -->
  <transition name="fade-slide" mode="out-in">
    <div v-if="currentTool" class="tool-detail" :key="currentTool.id">
      <div class="tool-detail-left">
        <div class="tool-main-image-box">
          <img :src="currentTool.image" class="tool-main-image" loading="lazy" />
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


const currentHigh = ref(null)

const handleWheel = (event) => {
  event.preventDefault()
  const delta = event.deltaY
  event.currentTarget.scrollLeft += delta
}

const selectTool = (item, event) => {
  // 触发 selectTool 事件
  emit('selectTool', item)

  // 滚动点击的卡片到最前面
  const cardElement = event.currentTarget
  const scrollContainer = cardElement.closest('.tool-scroll')

  if (scrollContainer) {
    // 计算卡片相对于滚动容器的位置
    const cardRect = cardElement.getBoundingClientRect()
    const containerRect = scrollContainer.getBoundingClientRect()

    // 计算滚动距离，使卡片移动到容器左侧
    const scrollLeft = scrollContainer.scrollLeft + (cardRect.left - containerRect.left) - 20

    // 平滑滚动
    scrollContainer.scrollTo({
      left: scrollLeft,
      behavior: 'smooth'
    })
  }
}

// 监听currentPage或level变化，自动选择对应分类的第一个工具
watch([() => props.currentPage, () => props.level], ([newPage, newLevel]) => {
  let firstTool = null

  // 根据当前页面和级别选择第一个工具
  if (newLevel === 'primary') {
    if (newPage === 0 && props.filteredTools.length > 0) {
      firstTool = props.filteredTools[0]
    } else if (newPage === 1 && props.animals.length > 0) {
      firstTool = props.animals[0]
    } else if (newPage === 2 && props.plants.length > 0) {
      firstTool = props.plants[0]
    }
  } else if (newLevel === 'middle') {
    if (newPage === 0 && props.seasons.length > 0) {
      firstTool = props.seasons[0]
    } else if (newPage === 1 && props.solarTerms.length > 0) {
      firstTool = props.solarTerms[0]
    } else if (newPage === 2 && props.regions.length > 0) {
      firstTool = props.regions[0]
    }
  } else {
    // 高级级别
    if (props.advancedItems.length > 0) {
      firstTool = props.advancedItems[0]
    }
  }

  // 如果找到第一个工具，触发selectTool事件
  if (firstTool) {
    emit('selectTool', firstTool)
  }
}, { immediate: true })




</script>

<style scoped>
/* ====== 滚动区域样式 ====== */

/* 滚动层 */
.tool-scroll {
  position: relative;
  z-index: 1;
}

/* 防止卡片盖住其他元素 */
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
  padding: 0;
  overflow: hidden;
}

.tool-scroll-viewport {
  overflow: hidden;
  width: 100%;
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

/* .tool-scroll::-webkit-scrollbar {
  display: none;
} */

.tool-card {
  flex: 0 0 300px;
  background: #f8fcf8;
  border: 1px solid rgba(37, 193, 143, 0.12);
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
  border-color: #25c18f;
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
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 26px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 1200px) {
  .tool-detail {
    flex-direction: column;
    align-items: center;
  }
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
  background: rgba(37, 193, 143, 0.12);
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 12px;
  color: #1a8f67;
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
  background: #25c18f;
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
  background: #25c18f;
  color: #fff;
}

.primary-btn:hover {
  opacity: 0.92;
}

.ghost-btn {
  border: 1px solid rgba(37, 193, 143, 0.22);
  background: #fff;
  color: #25c18f;
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
  top: calc(50% + 120px);
  z-index: 9998;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(37, 193, 143, 0.16);
  background: rgba(255, 255, 255, 0.96);
  color: #25c18f;
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
  background: #25c18f;
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
  background: rgba(37, 193, 143, 0.22);
  transition: all 0.25s ease;
}

.dots span.active {
  width: 22px;
  border-radius: 4px;
  background: #25c18f;
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
