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
import { useAuth } from '../network/useAuth'

const routes = [
  { path: '/', component: Home },
  { path: '/participants', component: Participants },
  { path: '/linkcreater', component: LinkCreater },
  { path: '/setting', component: Setting },
  { path: '/login', component: Login },
  { path: '/users', component: Users },
  { path: '/records', component: Records },
  { path: '/register/:token', component: Register },
  { path: '/login', component: Login },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const publicPages = ['/login', '/register/:token']
  const isPublic = publicPages.some(p => to.path.startsWith(p))
  const user = JSON.parse(localStorage.getItem('user'))

  if (!user && !isPublic) {
    return next('/login')
  }

  if (!isPublic && user) {
    try {
      await useAuth(user.user_id)
      return next()
    } catch {
      localStorage.removeItem('user')
      return next('/login')
    }
  }

  return next()
})

export default router
