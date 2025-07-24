<!-- src/components/Header.vue -->
<template>
  <header class="header">
     <router-link to="/" class="header-title">
      <img :src="titleIcon" alt="リンク" class="title-icon" />
     </router-link>
  </header>
</template>

<script setup>
import './css/Header.css';
import titleIcon from '../assets/pics/title.png'
</script>
