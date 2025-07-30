<script setup>
import { ref, onMounted } from 'vue'
import { useGetRecords } from '../network/useGetRecords'
import { useRouter } from 'vue-router'

const router = useRouter()
const records = ref([])
const limit = 20
const offset = ref(0)
const loading = ref(false)
const allLoaded = ref(false)

const user = JSON.parse(localStorage.getItem('user'))
const userId = user?.user_id

if (!userId) {
  router.push('/login')
}

const loadRecords = async () => {
  if (loading.value || allLoaded.value) return
  loading.value = true
  const res = await useGetRecords(userId, limit, offset.value)
  if (res.records.length < limit) {
    allLoaded.value = true
  }
  records.value.push(...res.records)
  offset.value += limit
  loading.value = false
}

onMounted(loadRecords)

const headers = [
  { title: '同好会', key: 'club_name', width: '40%' },
  { title: '参加日', key: 'joined_at', width: '30%' },
  { title: '承認状況', key: 'approved_status', width: '30%' }
]

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

const onScroll = (e) => {
  const el = e.target
  if (el.scrollHeight - el.scrollTop - el.clientHeight < 100) {
    loadRecords()
  }
}
</script>

<template>
  <div>
    <h1 class="text-h5 my-4">参加記録</h1>

    <div
      style="max-height: 600px; overflow-y: auto;"
      @scroll="onScroll"
    >
      <v-data-table
        :headers="headers"
        :items="records"
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

      <div v-if="loading" class="text-center my-4">読み込み中...</div>
      <div v-if="allLoaded" class="text-center my-4 text-grey">これ以上のデータはありません</div>
    </div>
  </div>
</template>
