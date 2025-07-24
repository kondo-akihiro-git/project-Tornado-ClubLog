<!-- src/pages/Login.vue -->
<script setup>
import { ref } from 'vue'
import { useLogin } from '../network/useLogin'

const mailAddress = ref('')
const password = ref('')
const loginError = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  loginError.value = ''
  isLoading.value = true
  try {
    const res = await useLogin({ mail_address: mailAddress.value, password: password.value })
    localStorage.setItem('user', JSON.stringify(res))
    window.location.href = '/' // トップページへ
  } catch (err) {
    loginError.value = err.message || 'ログインに失敗しました'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-wrapper">
    <div v-if="isLoading" class="loading-message">
      ログイン中...
    </div>

    <div v-else class="login-form">
      <v-text-field
        label="メールアドレス"
        v-model="mailAddress"
        type="email"
        required
      />

      <v-text-field
        label="パスワード"
        v-model="password"
        type="password"
        required
      />

      <v-btn @click="handleLogin" color="primary" class="mt-2">ログイン</v-btn>

      <div v-if="loginError" class="mt-2 text-error">
        {{ loginError }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 70vh; /* 画面全体に中央配置 */
  text-align: center;
}

.loading-message {
  font-size: 1rem;
}

.login-form {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}
</style>
