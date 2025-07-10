<!-- /src/pages/Setting.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useGetUser } from '../network/useGetUser'
import { useUpdateUser } from '../network/useUpdateUser'

const user = ref(null)
const updatedUsername = ref('')
const updatedPassword = ref('')
const message = ref('')

const userId = 1 // 将来的にはログインユーザーのIDを動的に

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
      <v-text-field label="メールアドレス" v-model="user.mail_address" readonly />
      <v-text-field label="更新日時" :model-value="new Date(user.updated_at).toLocaleString()" readonly />

      <v-btn type="submit" color="primary" class="mt-4">更新ボタン</v-btn>
    </v-form>

    <div v-if="message" class="mt-2" style="color: #333;">{{ message }}</div>
    <div v-else-if="!user">ユーザー情報を読み込み中...</div>
  </div>
</template>
