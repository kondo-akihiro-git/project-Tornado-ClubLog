<!-- ｆrontend/src/pages/Register.vue -->
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
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card>
          <v-card-title class="text-h6">イベント参加登録</v-card-title>

          <v-card-text>
            <div v-if="event">
              <p><strong>イベント名:</strong> {{ event.title }}</p>
              <p v-if="event.scheduled_at">
                <strong>開催日時:</strong> {{ new Date(event.scheduled_at).toLocaleString() }}
              </p>
            </div>
            <div v-else>
              <p>イベント情報を読み込み中...</p>
            </div>

            <v-text-field
              v-model="mailAddress"
              label="メールアドレス"
              type="email"
              placeholder="メールアドレスを入力"
              required
              class="mt-4"
            />

            <v-btn
              @click="register"
              :disabled="!event"
              color="primary"
              class="mt-2"
              block
            >
              登録する
            </v-btn>

            <p class="mt-4" :class="message.includes('完了') ? 'text-success' : 'text-error'">
              {{ message }}
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
