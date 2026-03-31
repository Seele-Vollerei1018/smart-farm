const AUTH_STORAGE_KEY = 'smart-farm-auth-user'

export function getAuthUser() {
  const raw = localStorage.getItem(AUTH_STORAGE_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw)
  } catch {
    localStorage.removeItem(AUTH_STORAGE_KEY)
    return null
  }
}

export function isAuthenticated() {
  return !!getAuthUser()
}

export function loginWithPassword(username, password) {
  if (username !== 'admin' || password !== 'admin123') {
    return {
      ok: false,
      message: '账号或密码错误，请使用测试账号：admin / admin123',
    }
  }

  const user = {
    username: 'admin',
    displayName: 'admin',
    loginAt: new Date().toISOString(),
  }
  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user))
  return { ok: true, user }
}

export function logout() {
  localStorage.removeItem(AUTH_STORAGE_KEY)
}
