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
  const user = JSON.parse(localStorage.getItem('user'))
  const userId = user?.user_id
  if (!userId) return

  const res = await useGetParticipants(userId)  // ← POST対応に変更
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

  <v-row no-gutters class="mb-2">
  <!-- 名前とボタン（同じ行、縦位置も揃える） -->
  <v-col cols="12" class="d-flex justify-space-between align-center">
    <div>{{ user.username }}</div>
    <div>
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
    </div>
  </v-col>

  <!-- メールアドレス（下段・小さく・被らない） -->
  <v-col cols="12">
    <small class="text-grey-darken-1">メール : {{ user.mail_address }}</small>
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
