<!-- /src/pages/Setting.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useGetUser } from '../network/useGetUser'
import { useUpdateUser } from '../network/useUpdateUser'
import { useLogout } from '../network/useLogout'

const user = ref(null)
const updatedUsername = ref('')
const updatedPassword = ref('')
const message = ref('')

const user_data = JSON.parse(localStorage.getItem('user'))
const userId = user_data?.user_id

if (!userId) {
  router.push('/login')
}

onMounted(async () => {
  const res = await useGetUser(userId)
  if (res.id) {
    user.value = res
    updatedUsername.value = res.username // 初期値に現在の名前をセット
  }
})

async function updateUser() {
  if (!updatedUsername.value && !updatedPassword.value) {
    message.value = 'ユーザー名またはパスワードのいずれかを入力してください'
    return
  }

  const updateData = {}
  if (updatedUsername.value) updateData.username = updatedUsername.value
  if (updatedPassword.value) updateData.password = updatedPassword.value

  const res = await useUpdateUser(userId, updateData)

  if (res.success) {
    message.value = res.data.message
    const refreshed = await useGetUser(userId)
    user.value = refreshed
    updatedPassword.value = '' // パスワードは更新後にクリア
  } else {
    message.value = `更新エラー: ${res.error}`
  }
}
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">ユーザー設定</h1>

    <v-form v-if="user" @submit.prevent="updateUser">
      <v-text-field label="ユーザー名" v-model="updatedUsername" />
      <v-text-field label="新しいパスワード" v-model="updatedPassword" type="password" />
      <v-text-field label="メールアドレス" v-model="user.mail_address" readonly class="readonly-field" />

      <v-text-field label="更新日時" :model-value="new Date(user.updated_at).toLocaleString()" readonly
        class="readonly-field" />


      <div class="d-flex justify-space-between mt-4">
        <v-btn type="submit" color="primary">更新</v-btn>
        <v-btn color="error" @click="useLogout()">ログアウト</v-btn>
      </div>
    </v-form>

    <div v-if="message" class="mt-2" style="color: #333;">{{ message }}</div>
    <div v-else-if="!user">ユーザー情報を読み込み中...</div>
  </div>
</template>

<style>
.readonly-field {
  color: #777;
  cursor: not-allowed;
}
</style>