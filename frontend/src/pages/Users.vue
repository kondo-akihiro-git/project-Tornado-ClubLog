<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGetUsers } from '../network/useGetUsers'

const rawParticipation = ref({})
const usernameFilter = ref('')
const clubFilter = ref('')
const monthFilter = ref('')

// 表示用ヘッダー
const headers = [
  { text: 'ユーザー名', value: 'username' },
  { text: '同好会名', value: 'club_name' },
  { text: '参加日時', value: 'joined_at' }
]

// API呼び出し
onMounted(async () => {
  const res = await useGetUsers()
  rawParticipation.value = res
})

// フィルタ済みデータ
const filteredList = computed(() => {
  const items = rawParticipation.value.user_participation ?? []
  return items.filter(item => {
    const joinedDate = new Date(item.joined_at)
    const joinedMonth = `${joinedDate.getFullYear()}-${String(joinedDate.getMonth() + 1).padStart(2, '0')}`

    return (
      (!usernameFilter.value || item.username.includes(usernameFilter.value)) &&
      (!clubFilter.value || item.club_name.includes(clubFilter.value)) &&
      (!monthFilter.value || joinedMonth === monthFilter.value)
    )
  })
})

// 選択肢用：開催年月（重複なしで抽出）
const uniqueMonths = computed(() => {
  const items = rawParticipation.value.user_participation ?? []
  const months = new Set(
    items.map(item => {
      const date = new Date(item.joined_at)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    })
  )
  return Array.from(months).sort()
})
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">ユーザーの同好会参加履歴</h1>

    <v-row class="mb-4" dense>
      <v-col cols="4">
        <v-text-field
          v-model="usernameFilter"
          label="ユーザー名でフィルタ"
          clearable
        />
      </v-col>
      <v-col cols="4">
        <v-text-field
          v-model="clubFilter"
          label="同好会名でフィルタ"
          clearable
        />
      </v-col>
      <v-col cols="4">
        <v-select
          v-model="monthFilter"
          :items="uniqueMonths"
          label="開催年月でフィルタ"
          clearable
        />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="filteredList"
      class="elevation-1"
    >
      <template #item.joined_at="{ item }">
        {{ new Date(item.joined_at).toLocaleString() }}
      </template>
    </v-data-table>
  </div>
</template>
