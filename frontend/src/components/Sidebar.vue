<template>
  <aside class="fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-all duration-300 lg:translate-x-0 border-r border-gray-200 dark:border-gray-700" :class="{ '-translate-x-full': !isOpen }">
    <div class="flex flex-col h-full">
      <!-- Logo -->
      <div class="flex items-center justify-between h-16 px-6 border-b border-gray-200 dark:border-gray-700">
        <h1 class="text-xl font-bold text-primary-600 dark:text-primary-400">Social Dashboard</h1>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-primary-50 dark:hover:bg-gray-700 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
          active-class="bg-primary-100 dark:bg-gray-700 text-primary-600 dark:text-primary-400 font-medium"
        >
          <component :is="item.icon" class="w-5 h-5 mr-3" />
          <span>{{ item.name }}</span>
        </router-link>
      </nav>

      <!-- Footer -->
      <div class="p-4 border-t border-gray-200 dark:border-gray-700">
        <div class="px-4 py-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p class="text-sm text-gray-600 dark:text-gray-400">v1.0.0</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { LayoutDashboard, BarChart3, Calendar, FileText, Users } from 'lucide-vue-next'

const isOpen = ref(true)

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'Scheduler', path: '/scheduler', icon: Calendar },
  { name: 'Posts', path: '/posts', icon: FileText },
  { name: 'Accounts', path: '/accounts', icon: Users }
]
</script>
