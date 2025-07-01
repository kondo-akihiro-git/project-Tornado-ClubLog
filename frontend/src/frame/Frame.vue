<!-- src/frame/Frame.vue -->
<template>
    <div class="frame">
        <slot></slot>
    </div>
</template>

<style scoped>
.frame {
    padding: 2rem;
    font-family: sans-serif;
    background: #f9f9f9;
    margin: 2rem auto;
    width: 100%;
}
</style>
