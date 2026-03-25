<script setup>
import { ref } from 'vue'

const piOnline = ref(true)
const piPower = ref(true)

const devices = ref([
  {
    id: 'fan',
    title: '风扇',
    subtitle: '帮助降温',
    desc: '温度过高时开启，促进空气流通。',
    available: true,
    on: false,
    icon: 'fan',
  },
  {
    id: 'pump',
    title: '水泵',
    subtitle: '浇灌',
    desc: '支持定时或手动浇灌营养液。',
    available: true,
    on: false,
    icon: 'pump',
  },
  {
    id: 'light',
    title: '补光灯',
    subtitle: '补光',
    desc: '日照不足时为作物补光。',
    available: true,
    on: false,
    icon: 'light',
  },
])

const logs = ref([
  { time: '2025-03-25 14:02:18', device: '风扇', command: 'turn_off', status: 'success' },
  { time: '2025-03-25 13:41:05', device: '水泵', command: 'irrigate_5min', status: 'pending' },
  { time: '2025-03-25 12:15:44', device: 'Raspberry Pi', command: 'heartbeat', status: 'success' },
  { time: '2025-03-25 11:03:04', device: 'Raspberry Pi', command: 'turn_off', status: 'pending' },
])

function statusLabel(s) {
  const map = { success: '已执行', pending: '待执行', error: '失败' }
  return map[s] || s
}

function onDeviceChange(d) {
  if (!piOnline.value || !d.available || !piPower.value) return
  logs.value.unshift({
    time: new Date().toLocaleString('zh-CN', { hour12: false }),
    device: d.title,
    command: d.on ? 'turn_on' : 'turn_off',
    status: 'pending',
  })
}
</script>

<template>
  <div class="ctrl">
    <header class="ctrl-head">
      <div>
        <h2 class="ctrl-title">设备控制</h2>
        <p class="ctrl-sub">
          请确保树莓派在线后再操作末端设备。
          <span class="legend"><span class="dot on"></span> 在线</span>
          <span class="legend"><span class="dot off"></span> 离线</span>
        </p>
      </div>
    </header>

    <!-- 主控 -->
    <article class="proto-card pi-card">
      <div class="pi-row">
        <div class="pi-icon-wrap" aria-hidden="true">
          <svg viewBox="0 0 64 64" width="56" height="56" class="pi-svg">
            <rect x="8" y="12" width="48" height="40" rx="6" fill="#ede7f6" stroke="#7e57c2" stroke-width="2" />
            <rect x="16" y="22" width="14" height="10" rx="1" fill="#fff" stroke="#9575cd" />
            <rect x="34" y="22" width="14" height="10" rx="1" fill="#fff" stroke="#9575cd" />
            <circle cx="22" cy="40" r="3" fill="#7e57c2" />
            <circle cx="32" cy="40" r="3" fill="#7e57c2" />
            <circle cx="42" cy="40" r="3" fill="#7e57c2" />
          </svg>
        </div>
        <div class="pi-info">
          <div class="pi-title-row">
            <h3>Raspberry Pi（温室主控）</h3>
            <span :class="['badge', piOnline ? 'badge-ok' : 'badge-bad']">
              {{ piOnline ? '在线' : '离线' }}
            </span>
          </div>
          <p class="pi-desc">网关状态与末端设备联动；后续对接 <code>/api/device/pi</code>。</p>
        </div>
        <label class="switch large">
          <input v-model="piPower" type="checkbox" :disabled="!piOnline" />
          <span class="slider" />
        </label>
      </div>
    </article>

    <!-- 末端设备 -->
    <section class="device-section" aria-label="末端设备">
      <h3 class="section-title">末端设备</h3>
      <div class="device-grid">
        <article v-for="d in devices" :key="d.id" class="proto-card device-card">
          <div class="device-top">
            <div class="device-titles">
              <h4>{{ d.title }}</h4>
              <span class="device-sub">{{ d.subtitle }}</span>
            </div>
            <span class="tag-avail">可用</span>
          </div>
          <div class="device-icon-row">
            <div v-if="d.icon === 'fan'" class="ico ico-fan" aria-hidden="true">
              <svg viewBox="0 0 48 48" width="40" height="40">
                <circle cx="24" cy="24" r="18" fill="#e3f2fd" stroke="#0d6efd" stroke-width="2" />
                <path
                  fill="#0d6efd"
                  d="M24 10c2 4 2 8 0 14-4-2-7-5-8-10 3-2 6-3 8-4zm0 28c-2-4-2-8 0-14 4 2 7 5 8 10-3 2-6 3-8 4zm14-14c-4 2-8 2-14 0 2-4 5-7 10-8 2 3 3 6 4 8zm-28 0c4-2 8-2 14 0-2 4-5 7-10 8-2-3-3-6-4-8z"
                />
              </svg>
            </div>
            <div v-else-if="d.icon === 'pump'" class="ico ico-pump" aria-hidden="true">
              <svg viewBox="0 0 48 48" width="40" height="40">
                <path
                  fill="#198754"
                  d="M24 8c-4 6-12 10-12 20a12 12 0 1024 0c0-10-8-14-12-20z"
                />
                <ellipse cx="24" cy="34" rx="10" ry="4" fill="#52b788" opacity="0.5" />
              </svg>
            </div>
            <div v-else class="ico ico-light" aria-hidden="true">
              <svg viewBox="0 0 48 48" width="40" height="40">
                <circle cx="24" cy="22" r="12" fill="#fff9c4" stroke="#f9a825" stroke-width="2" />
                <path stroke="#f9a825" stroke-width="2" stroke-linecap="round" d="M24 6v4M24 34v4M38 22h-4M14 22h-4" />
              </svg>
            </div>
            <label class="switch">
              <input
                v-model="d.on"
                type="checkbox"
                :disabled="!piOnline || !d.available || !piPower"
                @change="onDeviceChange(d)"
              />
              <span class="slider" />
            </label>
          </div>
          <p class="device-desc">{{ d.desc }}</p>
        </article>
      </div>
    </section>

    <!-- 日志 -->
    <article class="proto-card log-card">
      <div class="log-head">
        <h3>控制日志</h3>
        <span class="muted">演示数据 · 对接 <code>GET /api/control/logs</code></span>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>设备</th>
              <th>命令</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in logs" :key="i">
              <td>{{ row.time }}</td>
              <td>{{ row.device }}</td>
              <td><code class="cmd">{{ row.command }}</code></td>
              <td>
                <span
                  :class="[
                    'pill-status',
                    row.status === 'success' && 'pill-ok',
                    row.status === 'pending' && 'pill-warn',
                    row.status === 'error' && 'pill-err',
                  ]"
                >
                  {{ statusLabel(row.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </div>
</template>

<style scoped>
.ctrl {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.ctrl-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f5132;
  margin: 0 0 0.35rem;
}

.ctrl-sub {
  margin: 0;
  font-size: 0.88rem;
  color: rgba(26, 46, 36, 0.7);
}

.legend {
  margin-left: 0.75rem;
  font-size: 0.82rem;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 4px;
  vertical-align: middle;
}

.dot.on {
  background: #198754;
}

.dot.off {
  background: #dc3545;
}

.pi-card {
  padding: 1.25rem 1.35rem;
}

.pi-row {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.pi-icon-wrap {
  flex-shrink: 0;
}

.pi-svg {
  filter: drop-shadow(0 6px 12px rgba(126, 87, 194, 0.25));
}

.pi-info {
  flex: 1;
  min-width: 200px;
}

.pi-title-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-wrap: wrap;
  margin-bottom: 0.35rem;
}

.pi-title-row h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #143d2e;
}

.badge {
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.25rem 0.55rem;
  border-radius: 999px;
  letter-spacing: 0.02em;
}

.badge-ok {
  background: rgba(25, 135, 84, 0.15);
  color: #146c43;
}

.badge-bad {
  background: rgba(220, 53, 69, 0.12);
  color: #b02a37;
}

.pi-desc {
  margin: 0;
  font-size: 0.84rem;
  color: rgba(26, 46, 36, 0.65);
}

.pi-desc code {
  font-size: 0.85em;
  background: rgba(25, 135, 84, 0.08);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
}

.section-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #143d2e;
  margin: 0 0 0.65rem;
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.device-card {
  padding: 1.1rem 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.device-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
}

.device-titles h4 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f5132;
}

.device-sub {
  font-size: 0.78rem;
  color: rgba(26, 46, 36, 0.55);
}

.tag-avail {
  font-size: 0.68rem;
  font-weight: 800;
  color: #146c43;
  background: rgba(25, 135, 84, 0.12);
  padding: 0.2rem 0.45rem;
  border-radius: 6px;
  white-space: nowrap;
}

.device-icon-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.ico {
  display: flex;
  align-items: center;
  justify-content: center;
}

.device-desc {
  margin: 0;
  font-size: 0.82rem;
  line-height: 1.45;
  color: rgba(26, 46, 36, 0.72);
}

/* toggle */
.switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 26px;
  flex-shrink: 0;
}

.switch.large {
  width: 52px;
  height: 30px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: #ced4da;
  border-radius: 999px;
  transition: background 0.25s ease;
}

.slider::before {
  position: absolute;
  content: '';
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background: #fff;
  border-radius: 50%;
  transition: transform 0.25s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.switch.large .slider::before {
  height: 24px;
  width: 24px;
}

.switch input:checked + .slider {
  background: linear-gradient(180deg, #4dabf7 0%, #0d6efd 100%);
}

.switch input:checked + .slider::before {
  transform: translateX(20px);
}

.switch.large input:checked + .slider::before {
  transform: translateX(22px);
}

.switch input:disabled + .slider {
  opacity: 0.45;
  cursor: not-allowed;
}

.log-card {
  padding: 1.1rem 1.2rem 1.2rem;
}

.log-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.85rem;
}

.log-head h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: #143d2e;
}

.muted {
  font-size: 0.78rem;
  color: rgba(26, 46, 36, 0.55);
}

.muted code {
  font-size: 0.85em;
  background: rgba(25, 135, 84, 0.08);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
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

.cmd {
  font-size: 0.8em;
  background: #f1f3f5;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
}

.pill-status {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
}

.pill-ok {
  background: rgba(25, 135, 84, 0.15);
  color: #146c43;
}

.pill-warn {
  background: rgba(255, 193, 7, 0.2);
  color: #946200;
}

.pill-err {
  background: rgba(220, 53, 69, 0.12);
  color: #b02a37;
}

@media (max-width: 900px) {
  .device-grid {
    grid-template-columns: 1fr;
  }
}
</style>
