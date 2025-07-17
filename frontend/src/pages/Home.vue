<!-- src/pages/Home.vue -->
<script setup>
import { useLogout } from '../network/useLogout'
import { ref } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user')) || {})
</script>

<template>
  <div>
    <div class="text-h5 mb-4">同好会管理画面</div>

    <nav>
      <!-- オーナー向け -->
      <div v-if="user.user_role === 'owner'">
        <router-link to="/participants">参加者の管理</router-link><br>
        <router-link to="/linkcreater">リンク作成</router-link><br>
      </div>

      <!-- 一般ユーザー向け -->
      <div v-if="user.user_role === 'member'">
        <router-link to="/records">記録</router-link><br>
      </div>

      <!-- 管理者向け -->
      <div v-if="user.user_role === 'admin'">
        <router-link to="/users">全ユーザー情報</router-link><br>
      </div>

      <!-- 共通 -->
      <router-link to="/setting">ユーザー設定</router-link><br>
    </nav>

    <v-btn class="mt-4" color="error" @click="useLogout()">ログアウト</v-btn>
  </div>
</template>

