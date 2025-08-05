<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useGetRecords } from '../network/useGetRecords'

const router = useRouter()
const rawRecords = ref([])       // API全件
const clubFilter = ref('')
const statusFilter = ref('')

// ▼ ページネーション用変数
const limit = 6               // 1ページ件数
const page = ref(1)           // 現在ページ
const loading = ref(false)

const user = JSON.parse(localStorage.getItem('user'))
const userId = user?.user_id

if (!userId) {
  router.push('/login')
}

// 初回ロード
onMounted(async () => {
  await loadRecords()
})

// ▼ API呼び出し関数
async function loadRecords() {
  loading.value = true
  const res = await useGetRecords(userId)  // ★ 全件取得
  rawRecords.value = res.records ?? []
  loading.value = false
}

// ▼ フィルタ済みリスト
const filteredList = computed(() => {
  return rawRecords.value.filter(item =>
    (!clubFilter.value || item.club_name.includes(clubFilter.value)) &&
    (!statusFilter.value || item.approved_status === statusFilter.value)
  )
})

// ▼ ページ総数
const pageCount = computed(() => {
  return Math.max(1, Math.ceil(filteredList.value.length / limit))
})

// 現在ページに応じたスライス
const pagedList = computed(() => {
  const start = (page.value - 1) * limit
  return filteredList.value.slice(start, start + limit)
})

// ページ変更時
const onPageChange = (newPage) => {
  page.value = newPage
}

// ▼ フィルタ入力時はページを1にリセット
watch([clubFilter, statusFilter], () => {
  page.value = 1
})

// ▼ フィルタリング後にページが範囲外なら補正
watch([filteredList, pageCount], () => {
  if (page.value > pageCount.value) {
    page.value = pageCount.value
  }
})

// ステータス表示用
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

const headers = [
  { title: '同好会', key: 'club_name', width: '40%' },
  { title: '参加日', key: 'joined_at', width: '30%' },
  { title: '承認状況', key: 'approved_status', width: '30%' }
]
</script>

<template>
  <div>
    <h1 class="text-h5 my-4">参加記録</h1>

    <v-row class="mb-4" dense>
      <v-col cols="6">
        <v-text-field
          v-model="clubFilter"
          label="同好会名"
          clearable
        />
      </v-col>
      <v-col cols="6">
        <v-select
          v-model="statusFilter"
          :items="[
            { title: 'すべて', value: '' },
            { title: '承認済み', value: 'approved' },
            { title: '未承認', value: 'pending' },
            { title: '却下済み', value: 'rejected' },
          ]"
          label="承認状況"
          clearable
        />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="pagedList"
      class="elevation-1 fixed-table"
      hide-default-footer
      density="compact"
      :loading="loading"
    >
      <template #item.club_name="{ item }">
        <span class="text-truncate">{{ item.club_name }}</span>
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

    <!-- ページネーション -->
    <v-row justify="center" class="my-4">
      <v-col cols="auto">
        <v-pagination
          v-model="page"
          :length="pageCount"
          :total-visible="3"
          @update:model-value="onPageChange"
          variant="outlined"
        >
          <template #prev="{ onClick }">
            <v-btn
              class="d-flex align-center justify-center"
              variant="text"
              size="small"
              min-width="36"
              height="36"
              @click="onClick"
              :disabled="page <= 1"
            >
              前へ
            </v-btn>
          </template>

          <template #next="{ onClick }">
            <v-btn
              class="d-flex align-center justify-center"
              variant="text"
              size="small"
              min-width="36"
              height="36"
              @click="onClick"
              :disabled="page >= pageCount"
            >
              次へ
            </v-btn>
          </template>
        </v-pagination>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
.text-truncate {
  display: block;
  max-width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.fixed-table :deep(table) {
  table-layout: fixed;
  width: 100%;
  font-size: 12px;
}

.fixed-table :deep(th) {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.v-pagination .v-btn) {
  height: 36px;
  min-width: 36px;
  color: black !important;
  background-color: white !important;
  border-color: lightgray !important;
}
</style>
