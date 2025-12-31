<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <Sidebar />
    <div class="lg:pl-64">
      <Header />
      <main class="p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import { useAnalyticsStore } from './stores/analytics'
import { useThemeStore } from './stores/theme'

const analyticsStore = useAnalyticsStore()
const themeStore = useThemeStore()

onMounted(() => {
  // Initialize theme
  themeStore.initTheme()
  
  // Load initial data
  analyticsStore.fetchDashboardStats()
})
</script>
