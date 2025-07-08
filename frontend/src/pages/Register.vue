<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useRegisterParticipation } from '../network/useRegisterParticipation'

const route = useRoute()
const eventId = route.params.eventId

const username = ref('')
const mailAddress = ref('')
const message = ref('')

async function register() {
  if (!username.value || !mailAddress.value) {
    message.value = '名前とメールアドレスを入力してください'
    return
  }

  const res = await useRegisterParticipation({
    username: username.value,
    mail_address: mailAddress.value,
    event_id: Number(eventId)
  })

  if (res.success) {
    message.value = '登録が完了しました！'
    username.value = ''
    mailAddress.value = ''
  } else {
    message.value = `エラー: ${res.error}`
  }
}
</script>

<template>
  <div>
    <h1>イベント参加登録</h1>
    <p>イベントID: {{ eventId }}</p>

    <div>
      <label>名前:</label>
      <input v-model="username" type="text" placeholder="名前を入力" />
    </div>

    <div>
      <label>メールアドレス:</label>
      <input v-model="mailAddress" type="email" placeholder="メールアドレスを入力" />
    </div>

    <button @click="register">登録する</button>

    <p style="margin-top: 1em; color: #333;">{{ message }}</p>
  </div>
</template>
