<!-- src/App.vue -->
<script setup>
import Frame from './frame/Frame.vue'
</script>

<template>
  <Frame>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/hello">Hello</router-link>
  </nav>
  <router-view />
  </Frame>
</template>

