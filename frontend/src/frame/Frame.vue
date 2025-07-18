<!-- src/frame/Frame.vue -->
<template>
  <div class="frame-root">
    <div class="frame-center">
      <Header />

      <div class="frame-content">
        <slot />
      </div>

      <Footer />
    </div>
  </div>
</template>

<script setup>
import './css/Frame.css';
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';
</script>
