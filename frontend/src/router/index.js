// src/router/index.js
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
  { path: '/', component: Home }, // 全員アクセス可（ログイン済み）
  {
    path: '/participants',
    component: Participants,
    meta: { roles: ['owner'] }
  },
  {
    path: '/linkcreater',
    component: LinkCreater,
    meta: { roles: ['owner'] }
  },
  {
    path: '/setting',
    component: Setting,
    meta: { roles: ['member', 'owner', 'admin'] }
  },
  {
    path: '/users',
    component: Users,
    meta: { roles: ['admin'] }
  },
  {
    path: '/records',
    component: Records,
    meta: { roles: ['member'] }
  },
  {
    path: '/register/:token',
    component: Register,
    meta: { public: true }
  },
  {
    path: '/login',
    component: Login,
    meta: { public: true }
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'))
  const isPublic = to.meta?.public === true

  if (!user && !isPublic) {
    return next('/login')
  }

  if (user) {
    try {
      const authUser = await useAuth(user.user_id)

      // アクセス制限がある場合、ロールを確認
      const allowedRoles = to.meta?.roles
      if (allowedRoles && !allowedRoles.includes(authUser.user_role)) {
        return next('/')  // ホームにリダイレクト（権限なし）
      }

      return next()
    } catch {
      localStorage.removeItem('user')
      return next('/login')
    }
  }

  return next()
})


export default router
