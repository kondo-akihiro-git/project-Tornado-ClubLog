<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRegisterParticipation } from '../network/useRegisterParticipation'
import { useGetEvent } from '../network/useGetEvent'
import { useVerifyUser } from '../network/useVerifyUser'

const route = useRoute()
const token = route.params.token

const event = ref(null)
const mailAddress = ref('')
const message = ref('')

onMounted(async () => {
  const res = await useGetEvent(token)
  if (res.success) {
    event.value = res.data
  } else {
    message.value = `イベント情報の取得に失敗しました: ${res.error}`
  }
})

async function register() {
  if (!mailAddress.value) {
    message.value = 'メールアドレスを入力してください'
    return
  }

  // 先にユーザー名確認
  const verifyRes = await useVerifyUser(mailAddress.value)
  if (verifyRes.success && verifyRes.data.exists) {
    const username = verifyRes.data.username
    const ok = window.confirm(`${username} さんで間違いありませんか？`)
    if (!ok) {
      message.value = 'メールアドレスが誤っている可能性があります'
      return
    }
  }

  const res = await useRegisterParticipation({
    mail_address: mailAddress.value,
    event_id: Number(event.value?.event_id)
  })

  if (res.success) {
    message.value = '登録が完了しました！'
    mailAddress.value = ''
  } else {
    message.value = `エラー: ${res.error}`
  }
}
</script>

<template>
  <div>
    <h1>イベント参加登録</h1>

    <div v-if="event">
      <p><strong>イベント名:</strong> {{ event.title }}</p>
      <p v-if="event.scheduled_at"><strong>開催日時:</strong> {{ new Date(event.scheduled_at).toLocaleString() }}</p>
    </div>
    <div v-else>
      <p>イベント情報を読み込み中...</p>
    </div>

    <div>
      <label>メールアドレス:</label>
      <input v-model="mailAddress" type="email" placeholder="メールアドレスを入力" />
    </div>

    <button @click="register" :disabled="!event">登録する</button>

    <p style="margin-top: 1em; color: #333;">{{ message }}</p>
  </div>
</template>
