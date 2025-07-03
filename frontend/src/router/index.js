// src/router/router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Participant from '../pages/Participant.vue'
import Setting from '../pages/Setting.vue'
import LinkCreater from '../pages/LinkCreater.vue'
import Login from '../pages/Login.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/participant', component: Participant },
  { path: '/linkcreater', component: LinkCreater },
  { path: '/setting', component: Setting },
  { path: '/login', component: Login },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
