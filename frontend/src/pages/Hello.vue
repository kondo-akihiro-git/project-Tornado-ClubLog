<!-- src/pages/Hello.vue -->
<script setup>
import { ref, onMounted } from 'vue'

const message = ref('Loading...')

onMounted(async () => {
    try {
        const res = await fetch('http://localhost:8000/')
        message.value = await res.text()
    } catch (e) {
        message.value = 'Error fetching from API'
    }
})
</script>

<template>
    <div class="frame">
        <h1>{{ message }}</h1>
    </div>
</template>

<style scoped>
.frame {
    padding: 2rem;
    font-family: sans-serif;
    background: #f9f9f9;
    margin: 2rem auto;
    width: fit-content;
}
</style>
