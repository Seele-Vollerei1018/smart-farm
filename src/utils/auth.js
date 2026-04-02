import { login as apiLogin, register as apiRegister } from '@/api/client'

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

export async function loginWithPassword(username, password) {
  try {
    const response = await apiLogin(username, password)
    if (response.ok) {
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(response.user))
      return response
    }
    return response
  } catch (error) {
    return {
      ok: false,
      message: '登录失败，请检查网络连接',
    }
  }
}

export async function register(username, password, displayName) {
  try {
    const response = await apiRegister(username, password, displayName)
    return response
  } catch (error) {
    return {
      ok: false,
      message: '注册失败，请检查网络连接',
    }
  }
}

export function logout() {
  localStorage.removeItem(AUTH_STORAGE_KEY)
}

export function updateUserAvatar(avatarDataUrl) {
  const user = getAuthUser()
  if (!user) return false
  
  try {
    user.avatar = avatarDataUrl
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user))
    return true
  } catch (error) {
    console.error('更新头像失败:', error)
    return false
  }
}

export function getUserAvatar() {
  const user = getAuthUser()
  return user?.avatar || null
}
