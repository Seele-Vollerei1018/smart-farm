import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'
import ControlView from '../views/ControlView.vue'
import LearningView from '../views/LearningView.vue'
import LoginView from '../views/LoginView.vue'

import { isAuthenticated } from '../utils/auth'
import Layout from '../layouts/Layout.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
     // ✅ 登录页（独立）
    {
      path: '/login',
      component: LoginView,
      meta: { guestOnly: true }
    },

    
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '',
          component: HomeView
        },
        {
          path: 'dashboard',
          component: DashboardView,
          meta: { requiresAuth: true }
        },
        {
          path: 'control',
          component: ControlView,
          meta: { requiresAuth: true }
        },
        {
          path: 'learning',
          component: LearningView,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})




router.beforeEach((to) => {
  const authed = isAuthenticated()

  if (to.meta.requiresAuth && !authed) {
    return {
      path: '/login',
      query: { redirect: to.fullPath }
    }
  }

  if (to.meta.guestOnly && authed) {
    return '/'
  }

  return true
})

export default router