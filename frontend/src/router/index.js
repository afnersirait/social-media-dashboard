import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Analytics from '../views/Analytics.vue'
import Scheduler from '../views/Scheduler.vue'
import Posts from '../views/Posts.vue'
import Accounts from '../views/Accounts.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: Analytics
    },
    {
      path: '/scheduler',
      name: 'scheduler',
      component: Scheduler
    },
    {
      path: '/posts',
      name: 'posts',
      component: Posts
    },
    {
      path: '/accounts',
      name: 'accounts',
      component: Accounts
    }
  ]
})

export default router
