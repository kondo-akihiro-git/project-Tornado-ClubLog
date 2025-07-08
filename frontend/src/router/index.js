// src/router/router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Participants from '../pages/Participants.vue'
import Setting from '../pages/Setting.vue'
import LinkCreater from '../pages/LinkCreater.vue'
import Login from '../pages/Login.vue'
import Users from '../pages/Users.vue'
import Records from '../pages/Records.vue'
import Register from '../pages/Register.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/participants', component: Participants },
  { path: '/linkcreater', component: LinkCreater },
  { path: '/setting', component: Setting },
  { path: '/login', component: Login },
  { path: '/users', component: Users },
  { path: '/records', component: Records },
  { path: '/register/:token', component: Register } 
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
