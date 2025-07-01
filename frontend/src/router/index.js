// src/router/router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Hello from '../pages/Hello.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/hello', component: Hello },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
