<script setup>
import { ref } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import { useCreateEvent } from '../network/useCreateEvent'
import { useCreateLink } from '../network/useCreateLink'

const eventTitle = ref('')
const generatedUrl = ref('')
const message = ref('')

async function createLink() {
  if (!eventTitle.value) {
    message.value = 'イベント名は必須です'
    return
  }

  // 1. イベントを作成（club_id は仮に 1 で固定）
  const club_id = 1
  const eventRes = await useCreateEvent(eventTitle.value, club_id)
  if (!eventRes.success) {
    message.value = `イベント作成エラー: ${eventRes.error}`
    return
  }

  // 2. リンクを作成
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

    <!-- イベント開催日を追加 -->

    <button @click="createLink">リンク作成</button>

    <div v-if="generatedUrl" style="margin-top: 1em">
      <p>{{ message }}</p>
      <a :href="generatedUrl" target="_blank">{{ generatedUrl }}</a>
    </div>

    <p v-else-if="message" style="margin-top: 1em; color: #333;">{{ message }}</p>
  </div>
</template>
