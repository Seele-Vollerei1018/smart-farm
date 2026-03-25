<script setup>
import { ref, computed } from 'vue'

/** 以下为原型数据，后续可替换为 fetch('/api/...') 结果 */
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
  temperature: 24.6,
  humidity: 71.2,
  ph: 6.4,
  light: 8420,
  soil: 58,
  updated: '2025-03-25 14:31:08',
})

const alerts = ref([
  { time: '2025-03-25 13:45', type: '湿度', info: '湿度偏高', detail: '大棚 A 区 78%，超过阈值 75%' },
  { time: '2025-03-25 11:20', type: '温度', info: '温度正常', detail: '当前 24.2°C，在设定范围内' },
  { time: '2025-03-25 09:05', type: 'pH', info: '轻微偏低', detail: '营养液 pH 6.1，建议微调' },
])

const historyRows = ref([
  { time: '2025-03-25 14:28', temp: 24.6, humidity: 71.2, ph: 6.4 },
  { time: '2025-03-25 14:18', temp: 24.1, humidity: 70.5, ph: 6.4 },
  { time: '2025-03-25 14:08', temp: 23.8, humidity: 69.9, ph: 6.3 },
  { time: '2025-03-25 13:58', temp: 23.5, humidity: 69.1, ph: 6.3 },
  { time: '2025-03-25 13:48', temp: 23.2, humidity: 68.4, ph: 6.2 },
])

const trendTemp = ref([22.1, 22.8, 23.2, 23.5, 23.8, 24.1, 24.6])
const trendHum = ref([66, 67, 68, 68.5, 69.2, 70.5, 71.2])
const trendLabels = ref(['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'])

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
  const tMin = Math.min(...trendTemp.value) - 0.5
  const tMax = Math.max(...trendTemp.value) + 0.5
  const hMin = Math.min(...trendHum.value) - 2
  const hMax = Math.max(...trendHum.value) + 2
  return {
    temp: series(trendTemp.value, tMin, tMax),
    hum: series(trendHum.value, hMin, hMax),
    w,
    h,
  }
})

function mockSearchWeather() {
  weather.value = {
    ...weather.value,
    city: cityQuery.value.trim() || weather.value.city,
    updated: new Date().toLocaleString('zh-CN', { hour12: false }),
  }
}

function mockRefresh() {
  sensorLatest.value = {
    ...sensorLatest.value,
    temperature: +(sensorLatest.value.temperature + (Math.random() * 0.4 - 0.2)).toFixed(1),
    humidity: +(sensorLatest.value.humidity + (Math.random() * 1 - 0.5)).toFixed(1),
    updated: new Date().toLocaleString('zh-CN', { hour12: false }),
  }
}
</script>

<template>
  <div class="dash">
    <header class="dash-head">
      <div>
        <h2 class="dash-title">智慧农业监测 — 仪表盘</h2>
        <p class="dash-sub">实时概览 · 以下为演示数据，可对接传感器与云端接口</p>
      </div>
      <div class="dash-actions">
        <span class="pill">模式：演示</span>
        <button type="button" class="btn btn-ghost" @click="mockRefresh">刷新</button>
        <button type="button" class="btn btn-primary">同步云端</button>
        <button type="button" class="btn btn-ghost">导出告警 CSV</button>
      </div>
    </header>

    <!-- 第一行：核心指标 -->
    <section class="grid metrics" aria-label="最新传感器指标">
      <article class="proto-card metric proto-card--accent">
        <span class="metric-label">温度</span>
        <span class="metric-value">{{ sensorLatest.temperature }}<small>°C</small></span>
        <span class="metric-hint">适宜生长</span>
      </article>
      <article class="proto-card metric">
        <span class="metric-label">空气湿度</span>
        <span class="metric-value">{{ sensorLatest.humidity }}<small>%</small></span>
        <span class="metric-hint">略偏高</span>
      </article>
      <article class="proto-card metric">
        <span class="metric-label">pH</span>
        <span class="metric-value">{{ sensorLatest.ph }}</span>
        <span class="metric-hint">营养液</span>
      </article>
      <article class="proto-card metric">
        <span class="metric-label">光照</span>
        <span class="metric-value">{{ sensorLatest.light }}<small> lux</small></span>
        <span class="metric-hint">充足</span>
      </article>
    </section>

    <!-- 第二行：天气 + 土壤 -->
    <section class="grid row-2" aria-label="环境与土壤">
      <article class="proto-card panel weather">
        <div class="panel-head">
          <h3>外部天气（OpenWeather）</h3>
          <span class="muted">演示 · 接入 API 后展示真实数据</span>
        </div>
        <div class="weather-search">
          <label class="sr-only" for="city">城市</label>
          <input id="city" v-model="cityQuery" type="text" class="input" placeholder="城市英文名，如 Beijing" />
          <button type="button" class="btn btn-primary btn-sm" @click="mockSearchWeather">查询</button>
        </div>
        <div class="weather-body">
          <div class="weather-main">
            <span class="weather-temp">{{ weather.temp }}°</span>
            <div>
              <div class="weather-city">{{ weather.city }}</div>
              <div class="muted">{{ weather.desc }} · 体感 {{ weather.feels }}°C</div>
            </div>
          </div>
          <ul class="weather-meta">
            <li><span>湿度</span><strong>{{ weather.humidity }}%</strong></li>
            <li><span>风</span><strong>{{ weather.wind }}</strong></li>
            <li><span>更新</span><strong>{{ weather.updated }}</strong></li>
          </ul>
        </div>
      </article>

      <article class="proto-card panel soil">
        <div class="panel-head">
          <h3>土壤 / 基质</h3>
          <span class="tag tag-ok">正常</span>
        </div>
        <div class="soil-grid">
          <div>
            <span class="soil-label">含水率</span>
            <span class="soil-val">{{ sensorLatest.soil }}%</span>
          </div>
          <div>
            <span class="soil-label">电导率</span>
            <span class="soil-val">1.12 <small>mS/cm</small></span>
          </div>
          <div>
            <span class="soil-label">采集时间</span>
            <span class="soil-val small">{{ sensorLatest.updated }}</span>
          </div>
        </div>
        <p class="panel-note">接口就绪后映射字段：<code>soil_moisture</code>、<code>ec</code> 等。</p>
      </article>
    </section>

    <!-- 第三行：告警 + 历史表 -->
    <section class="grid row-3">
      <article class="proto-card panel table-panel">
        <div class="panel-head">
          <h3>告警记录</h3>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>时间</th>
                <th>类型</th>
                <th>摘要</th>
                <th>详情</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(a, i) in alerts" :key="i">
                <td>{{ a.time }}</td>
                <td><span class="tag tag-soft">{{ a.type }}</span></td>
                <td>{{ a.info }}</td>
                <td class="cell-detail">{{ a.detail }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>

      <article class="proto-card panel table-panel">
        <div class="panel-head">
          <h3>历史记录（最近）</h3>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>时间</th>
                <th>温度 (°C)</th>
                <th>湿度 (%)</th>
                <th>pH</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in historyRows" :key="i">
                <td>{{ r.time }}</td>
                <td>{{ r.temp }}</td>
                <td>{{ r.humidity }}</td>
                <td>{{ r.ph }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>
    </section>

    <!-- 第四行：趋势图 -->
    <article class="proto-card panel chart-panel" aria-label="温湿度趋势">
      <div class="panel-head">
        <h3>历史趋势（24h 采样示意）</h3>
        <div class="legend">
          <span class="dot dot-temp"></span> 温度 °C
          <span class="dot dot-hum"></span> 湿度 %
        </div>
      </div>
      <div class="chart-box">
        <svg
          class="chart-svg"
          :viewBox="`0 0 ${chartPaths.w} ${chartPaths.h}`"
          preserveAspectRatio="xMidYMid meet"
          role="img"
          aria-label="温湿度折线图"
        >
          <defs>
            <linearGradient id="g-temp" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#198754" stop-opacity="0.35" />
              <stop offset="100%" stop-color="#198754" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polyline
            :points="chartPaths.temp"
            fill="none"
            stroke="#157347"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <polyline
            :points="chartPaths.hum"
            fill="none"
            stroke="#0d6efd"
            stroke-width="2"
            stroke-dasharray="6 4"
            opacity="0.85"
          />
        </svg>
        <div class="chart-labels">
          <span v-for="(lb, i) in trendLabels" :key="i">{{ lb }}</span>
        </div>
      </div>
    </article>
  </div>
</template>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.dash {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.dash-head {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}

.dash-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f5132;
  margin: 0 0 0.25rem;
  letter-spacing: 0.02em;
}

.dash-sub {
  margin: 0;
  font-size: 0.88rem;
  color: rgba(26, 46, 36, 0.65);
}

.dash-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
}


.pill {
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
  background: rgba(25, 135, 84, 0.12);
  color: #146c43;
}

.btn {
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.45rem 0.9rem;
  border-radius: 10px;
  border: 1px solid transparent;
  cursor: pointer;
  transition:
    background 0.2s,
    border-color 0.2s,
    color 0.2s;
}

.btn-sm {
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
}

.btn-primary {
  background: linear-gradient(180deg, #2d9d5f 0%, #198754 100%);
  color: #fff;
  border-color: rgba(0, 0, 0, 0.06);
  box-shadow: 0 2px 8px rgba(25, 135, 84, 0.35);
}

.btn-primary:hover {
  filter: brightness(1.05);
}


.btn-ghost {
  background: #fff;
  border-color: rgba(15, 81, 50, 0.15);
  color: #1b4332;
}

.btn-ghost:hover {
  background: #f8fffa;
  border-color: rgba(25, 135, 84, 0.35);
}

.grid {
  display: grid;
  gap: 1rem;
}

.metrics {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.metric {
  padding: 1.1rem 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  position: relative;
  overflow: hidden;
}

.metric::after {
  content: '';
  position: absolute;
  right: -20px;
  top: -20px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(25, 135, 84, 0.12) 0%, transparent 70%);
  pointer-events: none;
}

.proto-card--accent {
  background: linear-gradient(135deg, #ffffff 0%, #f0fff6 100%);
}

.metric-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(26, 46, 36, 0.55);
}

.metric-value {
  font-size: 1.65rem;
  font-weight: 800;
  color: #0f5132;
  line-height: 1.1;
}

.metric-value small {
  font-size: 0.55em;
  font-weight: 700;
  margin-left: 2px;
  color: rgba(15, 81, 50, 0.65);
}

.metric-hint {
  font-size: 0.82rem;
  color: #198754;
  font-weight: 600;
}

.row-2 {
  grid-template-columns: 1.35fr 1fr;
}

.row-3 {
  grid-template-columns: 1fr 1fr;
}

.panel {
  padding: 1.1rem 1.2rem;
}

.panel-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.panel-head h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: #143d2e;
}

.muted {
  font-size: 0.78rem;
  color: rgba(26, 46, 36, 0.55);
}

.weather-search {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.input {
  flex: 1;
  min-width: 0;
  padding: 0.5rem 0.75rem;
  border-radius: 10px;
  border: 1px solid rgba(15, 81, 50, 0.15);
  font-size: 0.9rem;
  background: #fbfcfb;
}

.input:focus {
  outline: 2px solid rgba(25, 135, 84, 0.35);
  outline-offset: 0;
}

.weather-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.weather-main {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.weather-temp {
  font-size: 2.5rem;
  font-weight: 800;
  color: #157347;
  line-height: 1;
}

.weather-city {
  font-weight: 800;
  font-size: 1.05rem;
  color: #1b4332;
}

.weather-meta {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.5rem;
}

.weather-meta li {
  background: rgba(25, 135, 84, 0.06);
  border-radius: 10px;
  padding: 0.5rem 0.65rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 0.72rem;
  color: rgba(26, 46, 36, 0.6);
}

.weather-meta strong {
  font-size: 0.85rem;
  color: #143d2e;
}

.soil-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
}

.soil-label {
  display: block;
  font-size: 0.75rem;
  color: rgba(26, 46, 36, 0.55);
  margin-bottom: 0.25rem;
}

.soil-val {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f5132;
}

.soil-val.small {
  font-size: 0.85rem;
  font-weight: 600;
}

.soil-val small {
  font-size: 0.65em;
  font-weight: 700;
  color: rgba(15, 81, 50, 0.6);
}

.panel-note {
  margin: 0.85rem 0 0;
  font-size: 0.75rem;
  color: rgba(26, 46, 36, 0.5);
}

.panel-note code {
  font-size: 0.85em;
  background: rgba(25, 135, 84, 0.08);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
}

.tag {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
}

.tag-ok {
  background: rgba(25, 135, 84, 0.15);
  color: #146c43;
}

.tag-soft {
  background: rgba(13, 110, 253, 0.1);
  color: #0a58ca;
}

.table-wrap {
  overflow: auto;
  border-radius: 10px;
  border: 1px solid rgba(15, 81, 50, 0.08);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.data-table th,
.data-table td {
  padding: 0.55rem 0.65rem;
  text-align: left;
  border-bottom: 1px solid rgba(15, 81, 50, 0.06);
}

.data-table th {
  background: rgba(25, 135, 84, 0.08);
  font-weight: 700;
  color: #143d2e;
  white-space: nowrap;
}

.data-table tbody tr:hover {
  background: rgba(25, 135, 84, 0.04);
}

.cell-detail {
  color: rgba(26, 46, 36, 0.75);
  max-width: 220px;
}

.chart-panel {
  padding: 1.1rem 1.2rem 1.25rem;
}

.legend {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.8rem;
  color: rgba(26, 46, 36, 0.7);
}

.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 4px;
  vertical-align: middle;
}

.dot-temp {
  background: #157347;
}

.dot-hum {
  background: #0d6efd;
}

.chart-box {
  margin-top: 0.5rem;
}

.chart-svg {
  width: 100%;
  height: auto;
  display: block;
  background: linear-gradient(180deg, rgba(25, 135, 84, 0.04) 0%, transparent 55%);
  border-radius: 12px;
}

.chart-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.35rem;
  padding: 0 0.25rem;
  font-size: 0.72rem;
  color: rgba(26, 46, 36, 0.5);
}

@media (max-width: 1100px) {
  .metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .row-2 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .row-3 {
    grid-template-columns: 1fr;
  }

  .weather-meta {
    grid-template-columns: 1fr;
  }

  .soil-grid {
    grid-template-columns: 1fr;
  }
}
</style>
