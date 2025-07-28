<!-- src/pages/Home.vue -->
<script setup>
import { ref } from 'vue'
import troublePicture from '../assets/pics/trouble.png'
import aboutPicture from '../assets/pics/about.png'
import stepsPicture from '../assets/pics/steps.png'

const user = ref(JSON.parse(localStorage.getItem('user')) || {})
</script>

<template>
  <!-- スクロールコンテナ（カード縦スナップ） -->
<div class="scroll-container">
  <div class="scroll-card first-card">
    <v-img :src="troublePicture" height="100%" contain />
  </div>
  <div class="scroll-card">
    <v-img :src="aboutPicture" height="100%" contain />
  </div>
  <div class="scroll-card last-card">
    <v-img :src="stepsPicture" height="100%" contain />
  </div>
</div>
</template>

<style scoped>
.scroll-container {
  height: auto;
  overflow: visible;
  scroll-snap-type: none;
  margin: 0;
  padding: 0;
}

.scroll-card {
  scroll-snap-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 10vh - 50px - 24px * 2);
  margin: 24px 0;
  border: 1px solid black;
}

.first-card {
  margin-top: 24px;
}

.last-card {
  margin-bottom: 24px;
}


</style>
