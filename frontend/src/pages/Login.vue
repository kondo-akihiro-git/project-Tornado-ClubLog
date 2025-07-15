<!-- src/pages/Login.vue -->
<script setup>
import { ref } from 'vue'
import { useLogin } from '../network/useLogin'

const mailAddress = ref('')
const password = ref('')
const loginError = ref('')
const userInfo = ref(null)

const handleLogin = async () => {
  loginError.value = ''
  try {
    const res = await useLogin({ mail_address: mailAddress.value, password: password.value })
    userInfo.value = res
    localStorage.setItem('user', JSON.stringify(res))  // ← 追加
    window.location.href = '/'                         // ← トップページなどへ遷移
  } catch (err) {
    loginError.value = err.message || 'ログインに失敗しました'
  }
}

</script>

<template>
  <div class="ma-4">
    <h1 class="text-h5 mb-4">ログイン</h1>

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

    <div v-if="userInfo" class="mt-4">
      <p><strong>ユーザー名:</strong> {{ userInfo.username }}</p>
      <p><strong>ユーザーID:</strong> {{ userInfo.user_id }}</p>
      <p><strong>ロール:</strong> {{ userInfo.user_role }}</p>
    </div>
  </div>
</template>
