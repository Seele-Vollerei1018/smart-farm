<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loginWithPassword } from '../utils/auth'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

function onSubmit() {
  errorMessage.value = ''
  const result = loginWithPassword(username.value.trim(), password.value)
  if (!result.ok) {
    errorMessage.value = result.message
    return
  }

  const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
  router.replace(redirect)
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

      <p class="hint">测试账号：姓名 admin，密码 admin123</p>
    </section>
  </main>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1rem;
  background: linear-gradient(140deg, #e8f8ef 0%, #f6fbf8 55%, #dff5e8 100%);
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
  font-weight: 800;
  color: #0f5132;
}

.sub {
  margin: 0.35rem 0 1.2rem;
  color: rgba(20, 61, 46, 0.7);
  font-size: 0.9rem;
}

.form {
  display: grid;
  gap: 0.65rem;
}

.label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #143d2e;
}

.input {
  width: 100%;
  padding: 0.58rem 0.72rem;
  border-radius: 10px;
  border: 1px solid rgba(15, 81, 50, 0.2);
  font-size: 0.92rem;
}

.input:focus {
  outline: 2px solid rgba(25, 135, 84, 0.32);
  border-color: rgba(25, 135, 84, 0.5);
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
  background: linear-gradient(180deg, #2d9d5f 0%, #198754 100%);
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
</style>
