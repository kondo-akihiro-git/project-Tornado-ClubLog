<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGetUsers } from '../network/useGetUsers'

// APIから取得する生データ
const rawParticipation = ref({})

// computed で user_participation を整形（空配列フォールバック）
const participationList = computed(() => rawParticipation.value.user_participation ?? [])

// 表示用ヘッダー
const headers = [
  { text: 'ユーザー名', value: 'username' },
  { text: '同好会名', value: 'club_name' },
  { text: '参加日時', value: 'joined_at' }
]

// API呼び出し
onMounted(async () => {
  const res = await useGetUsers()
  console.log("res", res)
  rawParticipation.value = res
})
</script>

<template>
  <div>
    <h1 class="text-h5 mb-4">ユーザーの同好会参加履歴</h1>

    <v-data-table :headers="headers" :items="participationList" class="elevation-1">
      <template #item.joined_at="{ item }">
        {{ new Date(item.joined_at).toLocaleString() }}
      </template>
    </v-data-table>
  </div>
</template>
