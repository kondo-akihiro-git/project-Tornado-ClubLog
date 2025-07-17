<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGetRecords } from '../network/useGetRecords'
import { useRouter } from 'vue-router'

const router = useRouter()
const rawRecords = ref({})

// ✅ ログインユーザー取得
const user = JSON.parse(localStorage.getItem('user'))
const userId = user?.user_id

if (!userId) {
  router.push('/login')
}

// APIから取得する参加記録データ
onMounted(async () => {
  const res = await useGetRecords(userId)
  console.log("参加記録:", res)
  rawRecords.value = res
})

// computed: records を整形（空配列フォールバック）
const recordsList = computed(() => rawRecords.value.records ?? [])

// 表示用ヘッダー
const headers = [
  { text: '同好会名', value: 'club_name' },
  { text: '参加日時', value: 'joined_at' },
  { text: 'ステータス', value: 'approved_status' }
]

// ステータスラベルと色
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
