<!-- src/frame/Frame.vue -->
<template>
    <div class="frame-root">
        <div class="frame-center">
                <Header />
            <slot />
        </div>
    </div>
</template>

<script setup>
import './css/Frame.css';
import Header from '../components/Header.vue';
</script>
