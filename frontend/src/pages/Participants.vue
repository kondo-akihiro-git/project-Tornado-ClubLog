<!-- frontend/src/pages/Participants.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useGetParticipants } from '../network/useGetParticipants'
import { useApproveStatus } from '../network/useApproveStatus'
import { useGetStatus } from '../network/useGetStatus'

const FIXED_USER_ID = 1
const clubs = ref([])
const statusMap = ref({})  // { [event_id_user_id]: 'approved' | 'rejected' | 'pending' }

onMounted(async () => {
  const res = await useGetParticipants()
  clubs.value = res.clubs ?? []

  // 各ユーザー・イベントごとにステータス取得
  for (const club of clubs.value) {
    for (const event of club.events) {
      for (const user of event.participants) {
        const key = `${event.event_id}_${user.user_id}`
        try {
          const result = await useGetStatus({ user_id: user.user_id, event_id: event.event_id })
          statusMap.value[key] = result.approved_status
        } catch {
          statusMap.value[key] = 'pending'
        }
      }
    }
  }
})

const approve = async (user, event_id) => {
  try {
    await useApproveStatus({ user_id: user.user_id, event_id, status: 'approved' })
    statusMap.value[`${event_id}_${user.user_id}`] = 'approved'
  } catch (e) {
    alert(`承認に失敗しました: ${e.message}`)
  }
}

const reject = async (user, event_id) => {
  try {
    await useApproveStatus({ user_id: user.user_id, event_id, status: 'rejected' })
    statusMap.value[`${event_id}_${user.user_id}`] = 'rejected'
  } catch (e) {
    alert(`却下に失敗しました: ${e.message}`)
  }
}
</script>


<template>
  <div>
    <h1 class="text-h5 mb-4">同好会別イベント参加者一覧</h1>

    <v-expansion-panels multiple>
      <v-expansion-panel v-for="club in clubs" :key="club.club_name">
        <v-expansion-panel-title>
          {{ club.club_name }}
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <v-expansion-panels multiple>
            <v-expansion-panel v-for="event in club.events" :key="event.event_id">
              <v-expansion-panel-title>
                イベント: {{ event.title }}
              </v-expansion-panel-title>

              <v-expansion-panel-text>
                <ul>
<li
  v-for="user in event.participants"
  :key="user.mail_address"
  class="mb-2"
>
  <v-row align="center" no-gutters>
    <v-col cols="8">
      {{ user.username }}（{{ user.mail_address }}）
    </v-col>
    <v-col cols="4" class="d-flex align-center">
      <v-btn
        :color="statusMap[`${event.event_id}_${user.user_id}`] === 'approved' ? 'primary' : 'grey'"
        size="small"
        class="me-2"
        @click="approve(user, event.event_id)"
      >
        承認
      </v-btn>

      <v-btn
        :color="statusMap[`${event.event_id}_${user.user_id}`] === 'rejected' ? 'error' : 'grey'"
        size="small"
        @click="reject(user, event.event_id)"
      >
        却下
      </v-btn>
    </v-col>
  </v-row>
</li>

                </ul>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>
