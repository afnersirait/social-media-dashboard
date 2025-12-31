<template>
  <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
    <div class="flex items-center justify-between h-16 px-6">
      <div class="flex items-center">
        <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100">{{ pageTitle }}</h2>
      </div>

      <div class="flex items-center space-x-4">
        <!-- Theme Toggle -->
        <button
          @click="toggleTheme"
          class="p-2 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-gray-700 rounded-lg transition-colors"
          title="Toggle theme"
        >
          <Sun v-if="themeStore.isDark" class="w-5 h-5" />
          <Moon v-else class="w-5 h-5" />
        </button>

        <!-- Refresh Button -->
        <button
          @click="handleRefresh"
          class="p-2 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-gray-700 rounded-lg transition-colors"
          title="Refresh data"
        >
          <RefreshCw :class="{ 'animate-spin': isRefreshing }" class="w-5 h-5" />
        </button>

        <!-- Notifications -->
        <div class="relative">
          <button
            @click="toggleNotifications"
            class="p-2 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-gray-700 rounded-lg transition-colors relative"
            title="Notifications"
          >
            <Bell class="w-5 h-5" />
            <span v-if="unreadCount > 0" class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          <!-- Notifications Dropdown -->
          <div
            v-if="showNotifications"
            class="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 max-h-96 overflow-hidden"
          >
            <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100">Notifications</h3>
              <button
                v-if="unreadCount > 0"
                @click="markAllAsRead"
                class="text-xs text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300"
              >
                Mark all as read
              </button>
            </div>

            <div class="overflow-y-auto max-h-80">
              <div v-if="notifications.length === 0" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
                <Bell class="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p class="text-sm">No notifications yet</p>
              </div>

              <div v-else>
                <button
                  v-for="notification in notifications"
                  :key="notification.id"
                  @click="handleNotificationClick(notification)"
                  class="w-full px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-100 dark:border-gray-700 transition-colors"
                  :class="{ 'bg-blue-50 dark:bg-blue-900/30': !notification.read }"
                >
                  <div class="flex items-start space-x-3">
                    <div
                      class="p-2 rounded-lg flex-shrink-0"
                      :class="getNotificationIconBg(notification.type)"
                    >
                      <component :is="getNotificationIcon(notification.type)" class="w-4 h-4" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ notification.title }}</p>
                      <p class="text-xs text-gray-600 dark:text-gray-300 mt-1">{{ notification.message }}</p>
                      <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">{{ notification.time }}</p>
                    </div>
                    <div v-if="!notification.read" class="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0 mt-2"></div>
                  </div>
                </button>
              </div>
            </div>

            <div class="px-4 py-3 border-t border-gray-200 dark:border-gray-700 text-center">
              <button
                @click="viewAllNotifications"
                class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
              >
                View all notifications
              </button>
            </div>
          </div>
        </div>

        <!-- User Menu -->
        <div class="relative">
          <button
            @click="toggleUserMenu"
            class="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white font-medium">
              U
            </div>
            <ChevronDown class="w-4 h-4 text-gray-600 dark:text-gray-300" />
          </button>

          <!-- Dropdown Menu -->
          <div
            v-if="showUserMenu"
            class="absolute right-0 mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-2 z-50"
          >
            <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
              <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ userInfo.name }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ userInfo.email }}</p>
            </div>

            <div class="py-2">
              <button
                @click="viewProfile"
                class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
              >
                <User class="w-4 h-4 mr-3" />
                Profile Settings
              </button>
              <button
                @click="viewConnectedAccounts"
                class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
              >
                <Users class="w-4 h-4 mr-3" />
                Connected Accounts ({{ accountsCount }})
              </button>
              <button
                @click="viewNotifications"
                class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
              >
                <Bell class="w-4 h-4 mr-3" />
                Notifications
              </button>
              <button
                @click="viewSettings"
                class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
              >
                <Settings class="w-4 h-4 mr-3" />
                Settings
              </button>
            </div>

            <div class="border-t border-gray-200 dark:border-gray-700 py-2">
              <button
                @click="handleLogout"
                class="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center"
              >
                <LogOut class="w-4 h-4 mr-3" />
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { RefreshCw, Bell, ChevronDown, User, Users, Settings, LogOut, Heart, MessageCircle, TrendingUp, Calendar, Sun, Moon } from 'lucide-vue-next'
import { useAnalyticsStore } from '../stores/analytics'
import { usePostsStore } from '../stores/posts'
import { useAccountsStore } from '../stores/accounts'
import { useThemeStore } from '../stores/theme'

const route = useRoute()
const router = useRouter()
const analyticsStore = useAnalyticsStore()
const postsStore = usePostsStore()
const accountsStore = useAccountsStore()
const themeStore = useThemeStore()

const isRefreshing = ref(false)
const showUserMenu = ref(false)
const showNotifications = ref(false)

const userInfo = ref({
  name: 'Demo User',
  email: 'demo@socialdashboard.com'
})

// Sample notifications
const notifications = ref([
  {
    id: 1,
    type: 'engagement',
    title: 'New engagement on your post',
    message: 'Your post "Excited to announce..." received 50 new likes',
    time: '5 minutes ago',
    read: false
  },
  {
    id: 2,
    type: 'comment',
    title: 'New comment',
    message: 'Someone commented on your Instagram post',
    time: '1 hour ago',
    read: false
  },
  {
    id: 3,
    type: 'milestone',
    title: 'Milestone reached!',
    message: 'You reached 10,000 followers on Twitter',
    time: '3 hours ago',
    read: false
  },
  {
    id: 4,
    type: 'scheduled',
    title: 'Post published',
    message: 'Your scheduled post was successfully published',
    time: '5 hours ago',
    read: true
  },
  {
    id: 5,
    type: 'engagement',
    title: 'High engagement alert',
    message: 'Your latest post is performing 200% better than average',
    time: '1 day ago',
    read: true
  }
])

const accountsCount = computed(() => accountsStore.accounts.length)
const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)

const pageTitle = computed(() => {
  const titles = {
    '/': 'Dashboard',
    '/analytics': 'Analytics',
    '/scheduler': 'Scheduler',
    '/posts': 'Posts',
    '/accounts': 'Accounts'
  }
  return titles[route.path] || 'Dashboard'
})

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  showNotifications.value = false
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  showUserMenu.value = false
}

const closeNotifications = () => {
  showNotifications.value = false
}

const getNotificationIcon = (type) => {
  const icons = {
    engagement: Heart,
    comment: MessageCircle,
    milestone: TrendingUp,
    scheduled: Calendar
  }
  return icons[type] || Bell
}

const getNotificationIconBg = (type) => {
  const colors = {
    engagement: 'bg-pink-100 text-pink-600',
    comment: 'bg-blue-100 text-blue-600',
    milestone: 'bg-green-100 text-green-600',
    scheduled: 'bg-purple-100 text-purple-600'
  }
  return colors[type] || 'bg-gray-100 text-gray-600'
}

const handleNotificationClick = (notification) => {
  notification.read = true
  closeNotifications()
  // In a real app, this would navigate to the relevant content
  console.log('Notification clicked:', notification)
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
}

const viewAllNotifications = () => {
  closeNotifications()
  alert('All Notifications\n\nThis would show a full notifications page in a production app.')
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const viewProfile = () => {
  closeUserMenu()
  alert('Profile Settings\n\nName: ' + userInfo.value.name + '\nEmail: ' + userInfo.value.email + '\n\nThis is a demo. In a production app, this would open your profile settings.')
}

const viewConnectedAccounts = () => {
  closeUserMenu()
  router.push('/accounts')
}

const viewNotifications = () => {
  closeUserMenu()
  alert('Notifications\n\nYou have no new notifications.\n\nThis is a demo feature.')
}

const viewSettings = () => {
  closeUserMenu()
  alert('Settings\n\nApplication settings would be available here in a production app.')
}

const handleLogout = () => {
  closeUserMenu()
  if (confirm('Are you sure you want to sign out?')) {
    alert('Signed out successfully!\n\nThis is a demo. In a production app, you would be redirected to the login page.')
  }
}

const handleRefresh = async () => {
  isRefreshing.value = true
  try {
    await Promise.all([
      analyticsStore.fetchDashboardStats(),
      analyticsStore.fetchPlatformStats(),
      postsStore.fetchPosts(),
      accountsStore.fetchAccounts()
    ])
  } catch (error) {
    console.error('Error refreshing data:', error)
  } finally {
    setTimeout(() => {
      isRefreshing.value = false
    }, 500)
  }
}

// Close menus when clicking outside
const handleClickOutside = (event) => {
  const clickedElement = event.target.closest('.relative')
  if (!clickedElement) {
    if (showUserMenu.value) {
      closeUserMenu()
    }
    if (showNotifications.value) {
      closeNotifications()
    }
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  accountsStore.fetchAccounts()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
