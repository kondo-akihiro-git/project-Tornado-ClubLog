<!-- src/components/Footer.vue -->
<script setup>
import './css/Footer.css'
import { ref, computed } from 'vue'

// 画像のインポート
import homeIcon from '../assets/icons/home.png'
import settingsIcon from '../assets/icons/setting.png'
import linkIcon from '../assets/icons/link.png'
import participantsIcon from '../assets/icons/participants.png'
import recordsIcon from '../assets/icons/records.png'
import usersIcon from '../assets/icons/users.png'

const user = JSON.parse(localStorage.getItem('user') || '{}')
const userRole = ref(user?.user_role || '')
const isLoggedIn = computed(() => !!user?.user_id)
</script>

<template>
  <footer class="footer-bar">
    <v-row justify="center" align="center" class="h-full w-full">
      <!-- owner向け -->
      <v-col cols="true" v-if="userRole === 'owner'" class="text-center">
        <router-link to="/linkcreater" class="footer-icon-link">
          <img :src="linkIcon" alt="リンク" class="footer-icon-img" />
          <div class="footer-label">リンク</div>
        </router-link>
      </v-col>

      <v-col cols="true" v-if="userRole === 'owner'" class="text-center">
        <router-link to="/participants" class="footer-icon-link">
          <img :src="participantsIcon" alt="参加者" class="footer-icon-img" />
          <div class="footer-label">参加者</div>
        </router-link>
      </v-col>

      <!-- member向け -->
      <v-col cols="true" v-if="userRole === 'member'" class="text-center">
        <router-link to="/records" class="footer-icon-link">
          <img :src="recordsIcon" alt="記録" class="footer-icon-img" />
          <div class="footer-label">記録</div>
        </router-link>
      </v-col>

      <!-- admin向け -->
      <v-col cols="true" v-if="userRole === 'admin'" class="text-center">
        <router-link to="/users" class="footer-icon-link">
          <img :src="usersIcon" alt="全ユーザー" class="footer-icon-img" />
          <div class="footer-label">全ユーザー</div>
        </router-link>
      </v-col>

      <!-- ホーム -->
      <v-col cols="true" v-if="isLoggedIn" class="text-center">
        <router-link to="/" class="footer-icon-link">
          <img :src="homeIcon" alt="ホーム" class="footer-icon-img" />
          <div class="footer-label">ホーム</div>
        </router-link>
      </v-col>

      <!-- 設定 -->
      <v-col cols="true" v-if="isLoggedIn" class="text-center">
        <router-link to="/setting" class="footer-icon-link">
          <img :src="settingsIcon" alt="設定" class="footer-icon-img" />
          <div class="footer-label">設定</div>
        </router-link>
      </v-col>
    </v-row>
  </footer>
</template>
