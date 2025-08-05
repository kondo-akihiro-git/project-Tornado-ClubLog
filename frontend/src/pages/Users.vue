<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useGetUsers } from '../network/useGetUsers'

const rawParticipation = ref([])       // API全件
const usernameFilter = ref('')
const clubFilter = ref('')

// ▼ ページネーション用変数
const limit = 6               // 1ページ件数
const page = ref(1)           // 現在ページ
const loading = ref(false)

// 初回ロード
onMounted(async () => {
  await loadUsers()
})

// ▼ API呼び出し関数
async function loadUsers() {
  loading.value = true
  const res = await useGetUsers()  // ★ limit/offsetなし
  rawParticipation.value = res.user_participation ?? []
  loading.value = false
}

// ▼ フィルタ済みリスト
const filteredList = computed(() => {
  return rawParticipation.value.filter(item =>
    (!usernameFilter.value || item.username.includes(usernameFilter.value)) &&
    (!clubFilter.value || item.club_name.includes(clubFilter.value))
  )
})

// ▼ ページネーション計算
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
watch([usernameFilter, clubFilter], () => {
  page.value = 1
})

// ▼ フィルタリング後にページが範囲外なら補正
watch([filteredList, pageCount], () => {
  if (page.value > pageCount.value) {
    page.value = pageCount.value
  }
})
</script>

<template>
  <div>
    <h1 class="text-h5 my-4">ユーザーの同好会参加履歴</h1>

    <v-row class="mb-4" dense>
      <v-col cols="6">
        <v-text-field
          v-model="usernameFilter"
          label="ユーザー名"
          clearable
        />
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="clubFilter"
          label="同好会名"
          clearable
        />
      </v-col>
    </v-row>

    <v-data-table
      :headers="[
        { title: 'ユーザー', key: 'username', width: '25%' },
        { title: '同好会', key: 'club_name', width: '40%' },
        { title: '参加日', key: 'joined_at', width: '30%' }
      ]"
      :items="pagedList"
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
