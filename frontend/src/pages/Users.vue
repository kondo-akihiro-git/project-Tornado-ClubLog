<!-- frontend/src/pages/Users.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGetUsers } from '../network/useGetUsers'

const rawParticipation = ref([])
const usernameFilter = ref('')
const clubFilter = ref('')
const displayCount = ref(20) // 初期表示件数
const loadMoreThreshold = 100 // 下端から何pxで追加読み込みするか

onMounted(async () => {
  const res = await useGetUsers()
  rawParticipation.value = res.user_participation ?? []
})

// ヘッダー（カラム幅指定あり）
const headers = ref([
  { title: 'ユーザー', key: 'username', width: '35%' },
  { title: '同好会', key: 'club_name', width: '35%' },
  { title: '参加日', key: 'joined_at', width: '30%' }
])

// フィルタ + 表示制御
const filteredList = computed(() => {
  return rawParticipation.value
    .filter(item =>
      (!usernameFilter.value || item.username.includes(usernameFilter.value)) &&
      (!clubFilter.value || item.club_name.includes(clubFilter.value))
    )
    .slice(0, displayCount.value)
})

// スクロールイベント処理
const onScroll = (e) => {
  const el = e.target
  if (el.scrollHeight - el.scrollTop - el.clientHeight < loadMoreThreshold) {
    displayCount.value += 20 // 20件ずつ追加表示
  }
}
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">ユーザーの同好会参加履歴</h1>

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

    <!-- スクロール可能な枠で包む -->
    <div
      style="max-height: 600px; overflow-y: auto;"
      @scroll="onScroll"
    >
      <v-data-table
        :headers="headers"
        :items="filteredList"
        class="elevation-1"
        hide-default-footer
        density="compact"
      >
        <template #item.username="{ item }">
          <span class="text-truncate" style="max-width: 100%; white-space: nowrap; display: block;">
            {{ item.username }}
          </span>
        </template>

        <template #item.club_name="{ item }">
          <span class="text-truncate" style="max-width: 100%; white-space: nowrap; display: block;">
            {{ item.club_name }}
          </span>
        </template>

        <template #item.joined_at="{ item }">
          {{ new Date(item.joined_at).toLocaleDateString() }}
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
