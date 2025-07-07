<!-- src/pages/LinkCreater.vue -->
<script setup>
import { ref } from 'vue'
import { useCreateLink } from '../network/useCreateLink'

const url = ref('')
const eventId = ref('')
const message = ref('')

async function createLink() {
  if (!url.value || !eventId.value) {
    message.value = 'URLとイベントIDは必須です'
    return
  }
  
  const res = await useCreateLink(url.value, Number(eventId.value))
  if (res.success) {
    message.value = `リンクを作成しました！ID: ${res.data.id}`
    url.value = ''
    eventId.value = ''
  } else {
    message.value = `エラー: ${res.error}`
  }
}
</script>

<template>
  <div>
    <h1>参加記録用のリンク作成</h1>

    <div>
      <label for="url">URL:</label>
      <input id="url" v-model="url" type="text" placeholder="https://example.com/event" />
    </div>

    <div>
      <label for="eventId">イベントID:</label>
      <input id="eventId" v-model="eventId" type="number" min="1" placeholder="イベントIDを入力" />
    </div>

    <button @click="createLink">リンク作成</button>

    <p v-if="message" style="margin-top: 1em; color: #333;">{{ message }}</p>
  </div>
</template>
