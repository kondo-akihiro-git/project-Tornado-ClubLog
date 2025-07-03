<!-- src/pages/Login.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useLogin } from '../network/useLogin'

const message = ref('Loading...')
onMounted(async () => { message.value = await useLogin() })
</script>

<template>
    <div>
        <div>ログイン</div>
        <div>{{ message }}</div>
    </div>
</template>
