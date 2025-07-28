<!-- frontend/src/pages/Records.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGetRecords } from '../network/useGetRecords'
import { useRouter } from 'vue-router'

const router = useRouter()
const rawRecords = ref([])
const displayCount = ref(20)
const loadMoreThreshold = 100

const user = JSON.parse(localStorage.getItem('user'))
const userId = user?.user_id

if (!userId) {
  router.push('/login')
}

onMounted(async () => {
  const res = await useGetRecords(userId)
  rawRecords.value = res.records ?? []
})

// ヘッダー（クラブ名広め＋改行防止）
const headers = [
  { title: '同好会', key: 'club_name', width: '40%' },
  { title: '参加日', key: 'joined_at', width: '30%' },
  { title: '承認状況', key: 'approved_status', width: '30%' }
]

// 表示制御付きレコード
const visibleRecords = computed(() => rawRecords.value.slice(0, displayCount.value))

// ステータス表示
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

// スクロール検知で表示件数追加
const onScroll = (e) => {
  const el = e.target
  if (el.scrollHeight - el.scrollTop - el.clientHeight < loadMoreThreshold) {
    displayCount.value += 20
  }
}
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">参加記録</h1>

    <div
      style="max-height: 600px; overflow-y: auto;"
      @scroll="onScroll"
    >
      <v-data-table
        :headers="headers"
        :items="visibleRecords"
        class="elevation-1"
        hide-default-footer
        density="compact"
      >
        <template #item.club_name="{ item }">
          <span class="text-truncate" style="max-width: 100%; white-space: nowrap; display: block;">
            {{ item.club_name }}
          </span>
        </template>

        <template #item.joined_at="{ item }">
          {{ new Date(item.joined_at).toLocaleDateString() }}
        </template>

        <template #item.approved_status="{ item }">
          <v-chip
          
            :color="statusColor(item.approved_status)"
            text-color="white"
            size="small"
            label
          >
            {{ statusLabel(item.approved_status) }}
          </v-chip>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<style scoped>
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
