<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGetRecords } from '../network/useGetRecords'

// 特定ユーザー（仮ログイン状態）のID
const userId = 1

// APIから取得する参加記録データ
const rawRecords = ref({})

// computed: records を整形（空配列フォールバック）
const recordsList = computed(() => rawRecords.value.records ?? [])

// 表示用ヘッダー
const headers = [
  { text: '同好会名', value: 'club_name' },
  { text: '参加日時', value: 'joined_at' },
  { text: 'ステータス', value: 'approved_status' }
]

// API呼び出し
onMounted(async () => {
  const res = await useGetRecords(userId)
  console.log("参加記録:", res)
  rawRecords.value = res
})
const statusLabel = (status) => {
  switch (status) {
    case 'approved': return '承認済み'
    case 'pending': return '未承認'
    case 'rejected': return '却下済み'
    default: return '不明'
  }
}

const statusColor = (status) => {
  switch (status) {
    case 'approved': return 'green'
    case 'pending': return 'grey'
    case 'rejected': return 'red'
    default: return 'black'
  }
}

</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">参加記録</h1>

    <v-data-table :headers="headers" :items="recordsList" class="elevation-1">
      <template #item.joined_at="{ item }">
        {{ new Date(item.joined_at).toLocaleString() }}
      </template>

      <template #item.approved_status="{ item }">
        <v-chip
          :color="statusColor(item.approved_status)"
          text-color="white"
          small
        >
          {{ statusLabel(item.approved_status) }}
        </v-chip>
      </template>
    </v-data-table>
  </div>
</template>

