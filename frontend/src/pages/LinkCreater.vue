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
    <h1>参加記録用のリンク作成</h1>

    <div>
      <label for="eventTitle">イベント名:</label>
      <input id="eventTitle" v-model="eventTitle" type="text" placeholder="イベント名を入力" />
    </div>

    <div>
      <label for="scheduledAt">開催日:</label>
      <input id="scheduledAt" v-model="scheduledAt" type="datetime-local" />
    </div>

    <button @click="createLink">リンク作成</button>

    <div v-if="generatedUrl" style="margin-top: 1em">
      <p>{{ message }}</p>
      <a :href="generatedUrl" target="_blank">{{ generatedUrl }}</a>
    </div>

    <p v-else-if="message" style="margin-top: 1em; color: #333;">{{ message }}</p>
  </div>
</template>
