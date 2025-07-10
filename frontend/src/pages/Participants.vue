<script setup>
import { ref, onMounted } from 'vue'
import { useGetParticipants } from '../network/useGetParticipants'

const clubs = ref([])

onMounted(async () => {
  const res = await useGetParticipants()
  clubs.value = res.clubs ?? []
})

const approve = (user) => {
  console.log('承認:', user)
}

const reject = (user) => {
  console.log('却下:', user)
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
      <v-col cols="2">
        <v-btn color="primary" size="small" @click="approve(user)">承認</v-btn>
      </v-col>
      <v-col cols="2">
        <v-btn color="error" size="small" @click="reject(user)">却下</v-btn>
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


