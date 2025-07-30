<!-- frontend/src/pages/Users.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGetUsers } from '../network/useGetUsers'

const rawParticipation = ref([])
const usernameFilter = ref('')
const clubFilter = ref('')

// ▼ ページネーション用変数
const limit = 6               // 1ページ件数
const page = ref(1)           // 現在ページ
const totalCount = ref(0)     // 総件数（APIから取得する想定）
const pageCount = computed(() => {
  return Math.max(1, Math.ceil(totalCount.value / limit)) // 0件でも1にするならMath.max
})
const totalVisible = computed(() => {
  return pageCount.value <= 2 ? pageCount.value : 2
})


const loading = ref(false)

// 初回ロード
onMounted(async () => {
  await loadUsers()
})

// ▼ API呼び出し関数
async function loadUsers() {
  loading.value = true
  const offset = (page.value - 1) * limit
  const res = await useGetUsers(limit, offset) // limit/offset指定
  rawParticipation.value = res.user_participation ?? []
  totalCount.value = res.total_count ?? rawParticipation.value.length // 総件数がAPIで返るなら利用
  loading.value = false
console.log('totalCount:', totalCount.value)
console.log('ページ数(ceil):', Math.ceil(totalCount.value / limit))
console.log('ページ数(computed):', pageCount.value)

}

// ▼ ページ変更時
const onPageChange = async (newPage) => {
  page.value = newPage
  await loadUsers()
}

// ヘッダー
const headers = ref([
  { title: 'ユーザー', key: 'username', width: '25%' },
  { title: '同好会', key: 'club_name', width: '40%' },
  { title: '参加日', key: 'joined_at', width: '30%' }
])

// フィルタ済みリスト
const filteredList = computed(() => {
  return rawParticipation.value
    .filter(item =>
      (!usernameFilter.value || item.username.includes(usernameFilter.value)) &&
      (!clubFilter.value || item.club_name.includes(clubFilter.value))
    )
})
</script>

<template>
  <div>
    <h1 class="text-h5 my-4">ユーザーの同好会参加履歴</h1>

    <v-row class="mb-4" dense>
      <v-col cols="6">
        <v-text-field
          v-model="usernameFilter"
          label="ユーザー名でフィルタ"
          clearable
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="clubFilter"
          label="同好会名でフィルタ"
          clearable
        />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="filteredList"
      class="elevation-1 fixed-table"
      hide-default-footer
      density="compact"
      :loading="loading"
    >
      <template #item.username="{ item }">
        <span class="text-truncate">{{ item.username }}</span>
      </template>

      <template #item.club_name="{ item }">
        <span class="text-truncate">{{ item.club_name }}</span>
      </template>

      <template #item.joined_at="{ item }">
        {{ new Date(item.joined_at).toLocaleDateString() }}
      </template>
    </v-data-table>

    <!-- ページネーション追加 -->
<!-- ページネーション部分のみ修正版 -->
<v-row justify="center" class="my-4">
  <v-col cols="auto">
    <!-- 横幅固定ラッパ -->
<div class="pagination-wrapper d-flex align-center justify-center">
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
        variant="plain"
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
        variant="plain"
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
</div>

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

.pagination-wrapper {
  min-width: 100px; /* ここを小さめに設定 */
  max-width: 100px;
  margin: 0 auto;
}

:deep(.v-pagination .v-btn) {
  height: 36px;
  max-width: 20px;
  color: black !important;
  background-color: white !important;
  border-color: lightgray !important;
}


</style>
