<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loginWithPassword, register } from '../utils/auth'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const showRegisterConfirm = ref(false)

async function onSubmit() {
  errorMessage.value = ''
  const result = await loginWithPassword(username.value.trim(), password.value)

  if (result.ok) {
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    router.replace(redirect)
    return
  }

  // 用户不存在，询问是否注册
  if (result.code === 'USER_NOT_FOUND') {
    showRegisterConfirm.value = true
    return
  }

  // 其他错误（如密码错误）
  errorMessage.value = result.message
}

async function confirmRegister() {
  showRegisterConfirm.value = false
  errorMessage.value = ''

  try {
    // 注册新用户
    const registerResult = await register(username.value.trim(), password.value, username.value.trim())

    if (!registerResult.ok) {
      errorMessage.value = registerResult.message || '注册失败，请重试'
      return
    }

    // 注册成功后自动登录
    const loginResult = await loginWithPassword(username.value.trim(), password.value)

    if (loginResult.ok) {
      const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
      router.replace(redirect)
    } else {
      errorMessage.value = '注册成功，但自动登录失败，请手动登录'
    }
  } catch (error) {
    errorMessage.value = '注册失败，请重试'
  }
}

function cancelRegister() {
  showRegisterConfirm.value = false
  errorMessage.value = '用户不存在，请先注册'
}
</script>

<template>
  <main class="login-page">
    <section class="login-card">
      <h1 class="title">智慧农业监测系统</h1>
      <p class="sub">请登录后使用系统功能</p>

      <form class="form" @submit.prevent="onSubmit">
        <label class="label" for="username">姓名</label>
        <input id="username" v-model="username" class="input" type="text" placeholder="请输入姓名" autocomplete="username" />

        <label class="label" for="password">密码</label>
        <input
          id="password"
          v-model="password"
          class="input"
          type="password"
          placeholder="请输入密码"
          autocomplete="current-password"
        />

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button type="submit" class="submit-btn">登录</button>
      </form>

      <p class="hint">未注册的账号将自动注册</p>
    </section>

    <!-- 注册确认对话框 -->
    <div v-if="showRegisterConfirm" class="modal-overlay" @click.self="cancelRegister">
      <div class="modal-dialog">
        <h3 class="modal-title">用户不存在</h3>
        <p class="modal-message">该用户名未注册，是否立即注册？</p>
        <div class="modal-actions">
          <button class="modal-btn cancel" @click="cancelRegister">取消</button>
          <button class="modal-btn confirm" @click="confirmRegister">注册并登录</button>
        </div>
      </div>
    </div>
  </main>
</template>

<style >
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1rem;
  background: #f2f5f4;
}

.login-card {
  width: min(420px, 100%);
  padding: 1.5rem 1.5rem 1.25rem;
  background: #fff;
  border-radius: 16px;
  border: 1px solid rgba(15, 81, 50, 0.12);
  box-shadow:
    0 12px 30px rgba(15, 81, 50, 0.12),
    0 2px 8px rgba(15, 81, 50, 0.08);
}

.title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 700;
  color: #000000;
}

.sub {
  margin: 0.35rem 0 1.2rem;
  color: rgba(0, 0, 0, 0.65);
  font-size: 0.9rem;
}

.form {
  display: grid;
  gap: 0.65rem;
}

.label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #000000;
}

.input {
  width: 100%;
  padding: 0.58rem 0.72rem;
  border-radius: 10px;
  border: 1px solid rgba(15, 81, 50, 0.2);
  font-size: 0.92rem;
}

.input:focus {
  outline: 2px solid rgba(37, 193, 143, 0.32);
  border-color: rgba(37, 193, 143, 0.5);
}

.error {
  margin: 0.2rem 0 0;
  color: #b02a37;
  font-size: 0.82rem;
}

.submit-btn {
  margin-top: 0.3rem;
  border: none;
  border-radius: 10px;
  padding: 0.62rem 0.9rem;
  background: linear-gradient(180deg, #25c18f 0%, #1db882 100%);
  color: #fff;
  font-size: 0.92rem;
  font-weight: 700;
  cursor: pointer;
}

.submit-btn:hover {
  filter: brightness(1.05);
}

.hint {
  margin: 0.9rem 0 0;
  font-size: 0.78rem;
  color: rgba(20, 61, 46, 0.58);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #000;
}

.modal-message {
  margin: 0 0 1.5rem 0;
  font-size: 0.9rem;
  color: #666;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.modal-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn.cancel {
  background: #f0f0f0;
  color: #666;
}

.modal-btn.cancel:hover {
  background: #e0e0e0;
}

.modal-btn.confirm {
  background: linear-gradient(180deg, #25c18f 0%, #1db882 100%);
  color: white;
}

.modal-btn.confirm:hover {
  filter: brightness(1.05);
}
</style>
