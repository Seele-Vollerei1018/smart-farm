const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001'

function buildUrl(path) {
  const base = API_BASE_URL.replace(/\/+$/, '')
  const p = path.startsWith('/') ? path : `/${path}`
  return `${base}${p}`
}

async function getJson(path) {
  const res = await fetch(buildUrl(path), {
    method: 'GET',
    headers: { Accept: 'application/json' },
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`GET ${path} failed: ${res.status} ${text}`)
  }
  return res.json()
}

export async function fetchDeviceStatus(deviceId = '1001') {
  const res = await getJson(`/api/v1/devices/${deviceId}/status`)
  return res?.data || null
}

export async function fetchHistory(sensorType, range = '24h', interval = '1h') {
  const params = new URLSearchParams({
    sensor_type: sensorType,
    range,
    interval,
  })
  const res = await getJson(`/api/v1/analytics/history?${params.toString()}`)
  return res?.data || { x_axis: [], y_axis: [], min_val: null, max_val: null }
}

export async function fetchRuleLogs() {
  const res = await getJson('/api/v1/rules/logs')
  return Array.isArray(res?.data) ? res.data : []
}

export async function downloadReportXlsx() {
  const url = buildUrl(
    `/api/v1/analytics/report/export?${new URLSearchParams({ format: 'xlsx' })}`,
  )
  const res = await fetch(url, { method: 'GET' })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`export failed: ${res.status} ${text}`)
  }

  const blob = await res.blob()
  const filename = 'smart_farm_report.xlsx'
  const objectUrl = URL.createObjectURL(blob)

  const a = document.createElement('a')
  a.href = objectUrl
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()

  URL.revokeObjectURL(objectUrl)
}

