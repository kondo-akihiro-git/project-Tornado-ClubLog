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
  { text: '参加日時', value: 'joined_at' }
]

// API呼び出し
onMounted(async () => {
  const res = await useGetRecords(userId)
  console.log("参加記録:", res)
  rawRecords.value = res
})
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">参加記録</h1>

    <v-data-table :headers="headers" :items="recordsList" class="elevation-1">
      <template #item.joined_at="{ item }">
        {{ new Date(item.joined_at).toLocaleString() }}
      </template>
    </v-data-table>
  </div>
</template>
