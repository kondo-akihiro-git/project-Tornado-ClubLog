<!-- src/components/Footer.vue -->
<script setup>
import './css/Footer.css';
import { ref, computed } from 'vue'

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
          <div class="icon-placeholder">🔗</div>
          <div class="footer-label">リンク</div>
        </router-link>
      </v-col>

      <v-col cols="true" v-if="userRole === 'owner'" class="text-center">
        <router-link to="/participants" class="footer-icon-link">
          <div class="icon-placeholder">👥</div>
          <div class="footer-label">参加者</div>
        </router-link>
      </v-col>

      <!-- member向け -->
      <v-col cols="true" v-if="userRole === 'member'" class="text-center">
        <router-link to="/records" class="footer-icon-link">
          <div class="icon-placeholder">✏️</div>
          <div class="footer-label">記録</div>
        </router-link>
      </v-col>

      <!-- admin向け -->
      <v-col cols="true" v-if="userRole === 'admin'" class="text-center">
        <router-link to="/users" class="footer-icon-link">
          <div class="icon-placeholder">👤</div>
          <div class="footer-label">全ユーザー</div>
        </router-link>
      </v-col>

      <!-- ホーム -->
      <v-col cols="true" v-if="isLoggedIn" class="text-center">
        <router-link to="/" class="footer-icon-link">
          <div class="icon-placeholder">🏠</div>
          <div class="footer-label">ホーム</div>
        </router-link>
      </v-col>

      <!-- 設定 -->
      <v-col cols="true" v-if="isLoggedIn" class="text-center">
        <router-link to="/setting" class="footer-icon-link">
          <div class="icon-placeholder">⚙️</div>
          <div class="footer-label">設定</div>
        </router-link>
      </v-col>
    </v-row>
  </footer>
</template>
