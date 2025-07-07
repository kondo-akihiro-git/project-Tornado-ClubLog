<script setup>
import { ref, onMounted } from 'vue'
import { useGetParticipants } from '../network/useGetParticipants'

const clubs = ref([])

onMounted(async () => {
  const res = await useGetParticipants()
  clubs.value = res.clubs ?? []
})
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">同好会別イベント参加者一覧</h1>
    <div v-for="club in clubs" :key="club.club_name" class="mb-6">
      <h2 class="text-h6">{{ club.club_name }}</h2>
      <div v-for="event in club.events" :key="event.event_id" class="ml-4">
        <p class="font-medium">イベント: {{ event.title }}</p>
        <ul>
          <li v-for="user in event.participants" :key="user.mail_address">
            {{ user.username }}（{{ user.mail_address }}）
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

