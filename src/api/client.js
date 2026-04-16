const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || (import.meta.env.PROD ? '' : 'http://localhost:8001')

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

async function postJson(path, data) {
  const res = await fetch(buildUrl(path), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`POST ${path} failed: ${res.status} ${text}`)
  }
  return res.json()
}

async function putJson(path, data) {
  const res = await fetch(buildUrl(path), {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`PUT ${path} failed: ${res.status} ${text}`)
  }
  return res.json()
}

async function deleteJson(path) {
  const res = await fetch(buildUrl(path), {
    method: 'DELETE',
    headers: { Accept: 'application/json' },
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`DELETE ${path} failed: ${res.status} ${text}`)
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

// 认证相关 API
export async function login(username, password) {
  const res = await postJson('/api/v1/auth/login', { username, password })
  return res
}

export async function register(username, password, displayName) {
  const res = await postJson('/api/v1/auth/register', { username, password, displayName })
  return res
}

// 日记相关 API
export async function getDiaries(username) {
  const res = await getJson(`/api/v1/diaries?username=${encodeURIComponent(username)}`)
  return res?.data || []
}

export async function createDiary(username, title, content) {
  const res = await postJson(`/api/v1/diaries?username=${encodeURIComponent(username)}`, { title, content })
  return res
}

export async function updateDiary(username, diaryId, title, content) {
  const res = await putJson(`/api/v1/diaries/${diaryId}?username=${encodeURIComponent(username)}`, { title, content })
  return res
}

export async function deleteDiary(username, diaryId) {
  const res = await deleteJson(`/api/v1/diaries/${diaryId}?username=${encodeURIComponent(username)}`)
  return res
}

// 待办任务相关 API
export async function getTasks(username) {
  const res = await getJson(`/api/v1/tasks?username=${encodeURIComponent(username)}`)
  return res?.data || []
}

export async function createTask(username, title, description = '') {
  const res = await postJson(`/api/v1/tasks?username=${encodeURIComponent(username)}`, { title, description })
  return res
}

export async function updateTask(username, taskId, title, description, completed) {
  const res = await putJson(`/api/v1/tasks/${taskId}?username=${encodeURIComponent(username)}`, { title, description, completed })
  return res
}

export async function deleteTask(username, taskId) {
  const res = await deleteJson(`/api/v1/tasks/${taskId}?username=${encodeURIComponent(username)}`)
  return res
}

