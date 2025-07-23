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
    <!-- カード1 -->
    <div class="scroll-card">
      <v-img :src="troublePicture" height="100%" contain />
    </div>

    <!-- カード2 -->
    <div class="scroll-card">
      <v-img :src="aboutPicture" height="100%" contain />
    </div>

    <!-- カード3 -->
    <div class="scroll-card">
      <v-img :src="stepsPicture" height="100%" contain />
    </div>
  </div>
</template>

<style scoped>
.scroll-container {
  height: calc(100vh - 120px); /* Frame.vue の header/footer 高さを除いた表示域 */
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  -webkit-overflow-scrolling: touch;
  border-radius: 12px;
  padding: 0;
  margin: 0;
}

.scroll-card {
  height: 100%;
  scroll-snap-align: start;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  box-sizing: border-box;
}
</style>
