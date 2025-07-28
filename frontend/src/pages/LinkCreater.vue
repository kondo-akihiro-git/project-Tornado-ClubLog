<!-- src/pages/LinkCreater.vue -->
<script setup>
import { ref } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import { useCreateEvent } from '../network/useCreateEvent'
import { useCreateLink } from '../network/useCreateLink'

const eventTitle = ref('')
const scheduledAt = ref('')
const generatedUrl = ref('')
const message = ref('')

async function createLink() {
  if (!eventTitle.value || !scheduledAt.value) {
    message.value = 'イベント名と開催日は必須です'
    return
  }

  const club_id = 1
  const eventRes = await useCreateEvent(eventTitle.value, club_id, scheduledAt.value)
  if (!eventRes.success) {
    message.value = `イベント作成エラー: ${eventRes.error}`
    return
  }

  const eventId = eventRes.data.id
  const token = uuidv4()
  const linkRes = await useCreateLink(token, eventId)
  const fullUrl = `${window.location.origin}/register/${token}`

  if (linkRes.success) {
    generatedUrl.value = fullUrl
    message.value = 'リンクを作成しました！以下から登録できます:'
  } else {
    message.value = `リンク作成エラー: ${linkRes.error}`
  }
}
</script>

<template>
  <div>
    <h1 class="text-h5 my-4">参加登録用リンクの作成</h1>

    <v-form @submit.prevent="createLink">
      <v-text-field
        v-model="eventTitle"
        label="イベント名"
        placeholder="イベント名を入力"
        required
      />

      <v-text-field
        v-model="scheduledAt"
        label="開催日"
        type="date"
        required
      />

      <v-btn type="submit" color="primary" class="mt-4">リンク作成</v-btn>
    </v-form>

    <div v-if="generatedUrl" class="mt-4">
      <p class="text-subtitle-2 mb-1" style="color: #333;">{{ message }}</p>
      <a :href="generatedUrl" target="_blank" class="text-decoration-underline">{{ generatedUrl }}</a>
    </div>

    <div v-else-if="message" class="mt-4" style="color: #333;">{{ message }}</div>
  </div>
</template>
