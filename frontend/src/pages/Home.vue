<!-- src/pages/Home.vue -->
<script setup>

import { ref } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user')) || {})
</script>

<template>
  <div>
    <div class="text-h5 mb-4">ホーム</div>

    
  </div>
</template>

