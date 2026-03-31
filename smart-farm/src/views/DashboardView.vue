<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { fetchDeviceStatus, fetchHistory, fetchRuleLogs } from '../api/client'

/** 状态管理 */
const cityQuery = ref('Beijing')
const weather = ref({
  city: 'Beijing',
  temp: 18,
  feels: 16,
  desc: '多云',
  humidity: 62,
  wind: '东北 3 级',
  updated: '2025-03-25 14:32',
})

const sensorLatest = ref({
  temperature: 0,
  humidity: 0,
  ph: 6.4,
  light: 0,
  soil: 0,
  updated: '',
})

const alerts = ref([])
const historyRows = ref([])
const trendTemp = ref([])
const trendHum = ref([])
const trendLabels = ref([])
const loading = ref(true) // 初始加载时显示加载中
const error = ref('')
const initialLoaded = ref(false) // 标记是否已经完成初始加载
const lastHistoryUpdateHour = ref(null) // 记录上次更新历史记录的小时

/** 计算属性 */
const chartPaths = computed(() => {
  const w = 560
  const h = 160
  const pad = 8
  const series = (arr, min, max) => {
    const n = arr.length
    if (n < 2) return ''
    const pts = arr.map((v, i) => {
      const x = pad + (i / (n - 1)) * (w - pad * 2)
      const t = (v - min) / (max - min || 1)
      const y = h - pad - t * (h - pad * 2)
      return `${x},${y}`
    })
    return pts.join(' ')
  }
  const tMin = trendTemp.value.length > 0 ? Math.min(...trendTemp.value) - 0.5 : 20
  const tMax = trendTemp.value.length > 0 ? Math.max(...trendTemp.value) + 0.5 : 25
  const hMin = trendHum.value.length > 0 ? Math.min(...trendHum.value) - 2 : 60
  const hMax = trendHum.value.length > 0 ? Math.max(...trendHum.value) + 2 : 75
  return {
    temp: series(trendTemp.value, tMin, tMax),
    hum: series(trendHum.value, hMin, hMax),
    w,
    h,
  }
})

/** 方法 */
async function fetchData() {
  // 只有在初始加载时才显示加载中
  if (!initialLoaded.value) {
    loading.value = true
  }
  error.value = ''
  try {
    // 获取设备状态
    const deviceStatus = await fetchDeviceStatus()
    if (deviceStatus) {
      sensorLatest.value.updated = deviceStatus.last_active || ''
    }

    // 获取温度历史数据
    const tempHistory = await fetchHistory('temperature', '24h', '1h')
    if (tempHistory) {
      trendTemp.value = tempHistory.y_axis
      trendLabels.value = tempHistory.x_axis
    }

    // 获取湿度历史数据
    const humHistory = await fetchHistory('humidity', '24h', '1h')
    if (humHistory) {
      trendHum.value = humHistory.y_axis
    }

    // 获取光照数据
    const lightHistory = await fetchHistory('light', '24h', '1h')
    if (lightHistory && lightHistory.y_axis.length > 0) {
      sensorLatest.value.light = lightHistory.y_axis[lightHistory.y_axis.length - 1]
    }

    // 获取土壤湿度数据
    const soilHistory = await fetchHistory('soil_moisture', '24h', '1h')
    if (soilHistory && soilHistory.y_axis.length > 0) {
      sensorLatest.value.soil = soilHistory.y_axis[soilHistory.y_axis.length - 1]
    }

    // 获取规则日志（警告）
    const logs = await fetchRuleLogs()
    if (logs) {
      alerts.value = logs.map(log => ({
        time: log.timestamp,
        type: '系统',
        info: log.rule_name,
        detail: log.result
      }))
    }

    // 获取当前小时
    const currentHour = new Date().getHours()
    
    // 只有在新的小时或者是第一次加载时，才更新历史记录
    if ((tempHistory && humHistory && tempHistory.y_axis.length === humHistory.y_axis.length) && 
        (lastHistoryUpdateHour.value !== currentHour || lastHistoryUpdateHour.value === null)) {
      historyRows.value = tempHistory.y_axis.map((temp, index) => ({
        time: tempHistory.x_axis[index] || '',
        temp: typeof temp === 'number' ? temp.toFixed(2) : '0.00',
        humidity: typeof humHistory.y_axis[index] === 'number' ? humHistory.y_axis[index].toFixed(2) : '0.00',
        ph: 6.4 // 模拟pH值
      })).slice(-25).reverse()
      
      // 记录上次更新历史记录的小时
      lastHistoryUpdateHour.value = currentHour
    }

    // 更新最新传感器数据
    if (tempHistory && tempHistory.y_axis.length > 0) {
      sensorLatest.value.temperature = tempHistory.y_axis[tempHistory.y_axis.length - 1]
    }
    if (humHistory && humHistory.y_axis.length > 0) {
      sensorLatest.value.humidity = humHistory.y_axis[humHistory.y_axis.length - 1]
    }

    // 标记初始加载完成
    initialLoaded.value = true

  } catch (err) {
    error.value = '数据获取失败，请稍后重试'
    console.error('API调用错误:', err)
  } finally {
    // 只有在初始加载时才关闭加载中
    if (!initialLoaded.value) {
      loading.value = false
    }
  }
}

function mockSearchWeather() {
  weather.value = {
    ...weather.value,
    city: cityQuery.value.trim() || weather.value.city,
    updated: new Date().toLocaleString('zh-CN', { hour12: false }),
  }
}

function handleRefresh() {
  fetchData()
}

/** 生命周期 */
let refreshTimer = null

onMounted(() => {
  fetchData()
  // 每2秒自动刷新一次数据
  refreshTimer = setInterval(fetchData, 2000)
})

onUnmounted(() => {
  // 组件卸载时清除定时器
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<template>
  <div class="dashboard">

    <!-- 第一行：天气（通栏） -->
    <div class="card weather">
      <div class="weather-left">
        <h3>外部天气</h3>
        <p>晴 · 26°C · 微风</p>
      </div>
      <div class="weather-icon">☀️</div>
    </div>

    <!-- 第二行：2x2 核心数据 -->
    <div class="grid-2x2">

      <div class="card data">
        <div class="icon temp">🌡️</div>
        <div>
          <p class="value">26°C</p>
          <p class="label">环境温度</p>
        </div>
      </div>

      <div class="card data">
        <div class="icon hum">💧</div>
        <div>
          <p class="value">60%</p>
          <p class="label">空气湿度</p>
        </div>
      </div>

      <div class="card data">
        <div class="icon light">☀️</div>
        <div>
          <p class="value">800 lx</p>
          <p class="label">光照强度</p>
        </div>
      </div>

      <div class="card data">
        <div class="icon water">🌊</div>
        <div>
          <p class="value">75%</p>
          <p class="label">水位</p>
        </div>
      </div>

    </div>

    <!-- 第三行：趋势图（通栏） -->
    <div class="card chart">
      <h3>历史趋势</h3>
      <div class="chart-box">
        图表区域（后续接 ECharts）
      </div>
    </div>

    <!-- 第四行：左右 -->
    <div class="bottom">

      <div class="card list">
        <h3>历史警告</h3>
        <div class="item" v-for="i in 4" :key="i">
          <span class="dot warn"></span>
          温度异常警告 {{ i }}
        </div>
      </div>

      <div class="card list">
        <h3>历史记录</h3>
        <div class="item" v-for="i in 4" :key="i">
          <span class="dot normal"></span>
          正常运行记录 {{ i }}
        </div>
      </div>

    </div>

  </div>
</template>



<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 24px;
}

/* 卡片统一规范 */
.card {
  background: #FFFFFF;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 10px 40px rgba(29, 52, 54, 0.04);
  border: none;
}

/* ===== 天气 ===== */
.weather {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.weather h3 {
  font-size: 18px;
  font-weight: bold;
  color: #1E293B;
}

.weather p {
  color: #94A3B8;
}

.weather-icon {
  font-size: 36px;
}

/* ===== 2x2 网格 ===== */
.grid-2x2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.data {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 图标 */
.icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

/* 不同颜色 */
.temp {
  background: rgba(248, 113, 113, 0.1);
  color: #F87171;
}

.hum {
  background: rgba(96, 165, 250, 0.1);
  color: #60A5FA;
}

.light {
  background: rgba(251, 191, 36, 0.1);
  color: #FBBF24;
}

.water {
  background: rgba(37, 193, 143, 0.1);
  color: #25C18F;
}

/* 数据 */
.value {
  font-size: 28px;
  font-weight: bold;
  color: #1E293B;
}

.label {
  font-size: 14px;
  color: #94A3B8;
}

/* ===== 图表 ===== */
.chart-box {
  height: 240px;
  margin-top: 16px;
  background: #F8FAF9;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94A3B8;
}

/* ===== 底部 ===== */
.bottom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.list h3 {
  font-size: 18px;
  margin-bottom: 12px;
}

.item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  color: #1E293B;
}

/* 状态点 */
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.warn {
  background: #F59E0B;
}

.normal {
  background: #25C18F;
}
</style>