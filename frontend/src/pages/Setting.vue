<script setup>
import { ref, onMounted } from 'vue'
import { useGetUser } from '../network/useGetUser'

const user = ref(null)

onMounted(async () => {
  const res = await useGetUser(1)
  console.log("res", res)
  user.value = res
})
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">ユーザー設定</h1>

    <v-form v-if="user">
      <v-text-field
        label="ユーザー名"
        v-model="user.username"
        readonly
      />
      <v-text-field
        label="メールアドレス"
        v-model="user.mail_address"
        readonly
      />
      <v-text-field
        label="更新日時"
        :model-value="new Date(user.updated_at).toLocaleString()"
        readonly
      />
    </v-form>

    <div v-else>
      ユーザー情報を読み込み中...
    </div>
  </div>
</template>
