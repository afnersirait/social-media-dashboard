<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100">Social Media Accounts</h2>
      <button @click="showAddModal = true" class="btn btn-primary">
        <Plus class="w-5 h-5 mr-2" />
        Add Account
      </button>
    </div>

    <!-- Accounts Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="account in accounts"
        :key="account.id"
        class="card hover:shadow-lg transition-shadow"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div :class="getPlatformColor(account.platform)" class="p-3 rounded-lg">
              <component :is="getPlatformIcon(account.platform)" class="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-800 dark:text-gray-100">{{ account.account_name }}</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">{{ account.platform }}</p>
            </div>
          </div>
          <button
            @click="deleteAccount(account.id)"
            class="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
          >
            <Trash2 class="w-4 h-4" />
          </button>
        </div>

        <div class="space-y-2">
          <div class="flex items-center justify-between text-sm dark:text-gray-300">
            <span class="text-gray-600 dark:text-gray-400">Account ID</span>
            <span class="font-medium text-gray-800 dark:text-gray-200">{{ account.account_id }}</span>
          </div>
          <div class="flex items-center justify-between text-sm dark:text-gray-300">
            <span class="text-gray-600 dark:text-gray-400">Status</span>
            <span
              :class="account.is_active ? 'text-green-600 bg-green-100' : 'text-gray-600 bg-gray-100'"
              class="px-2 py-1 rounded text-xs font-medium"
            >
              {{ account.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <div class="flex items-center justify-between text-sm dark:text-gray-300">
            <span class="text-gray-600 dark:text-gray-400">Added</span>
            <span class="text-gray-800 dark:text-gray-200">{{ formatDate(account.created_at) }}</span>
          </div>
        </div>

        <button
          @click="viewAnalytics(account.id)"
          class="mt-4 w-full btn btn-secondary text-sm"
        >
          <BarChart3 class="w-4 h-4 mr-2" />
          View Analytics
        </button>
      </div>
    </div>

    <div v-if="!accounts.length" class="card text-center py-12">
      <Users class="w-12 h-12 mx-auto mb-4 text-gray-400" />
      <p class="text-gray-500 dark:text-gray-400 mb-4">No accounts connected yet</p>
      <button @click="showAddModal = true" class="btn btn-primary">
        Connect Your First Account
      </button>
    </div>

    <!-- Add Account Modal -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100">Add Social Account</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">
              <X class="w-6 h-6" />
            </button>
          </div>

          <form @submit.prevent="submitAccount" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Platform</label>
              <select v-model="formData.platform" required class="select">
                <option value="">Select platform</option>
                <option value="twitter">Twitter</option>
                <option value="facebook">Facebook</option>
                <option value="instagram">Instagram</option>
                <option value="linkedin">LinkedIn</option>
                <option value="youtube">YouTube</option>
                <option value="tiktok">TikTok</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Account Name</label>
              <input
                v-model="formData.account_name"
                type="text"
                required
                class="input"
                placeholder="e.g., @mycompany"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Account ID</label>
              <input
                v-model="formData.account_id"
                type="text"
                required
                class="input"
                placeholder="Unique identifier"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Access Token (optional)</label>
              <input
                v-model="formData.access_token"
                type="password"
                class="input"
                placeholder="OAuth access token"
              />
            </div>

            <div class="flex items-center justify-end space-x-3 pt-4">
              <button type="button" @click="closeModal" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">
                Add Account
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Analytics Modal -->
    <div
      v-if="showAnalyticsModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="showAnalyticsModal = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100">Account Analytics</h3>
            <button @click="showAnalyticsModal = false" class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">
              <X class="w-6 h-6" />
            </button>
          </div>

          <div v-if="accountAnalytics.length" class="space-y-4">
            <LineChart
              :data="accountAnalytics.map(a => ({ date: a.date.split('T')[0], followers: a.followers, engagement: a.total_engagement }))"
              :y-keys="['followers', 'engagement']"
              :colors="['#3b82f6', '#10b981']"
              :height="300"
            />

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
              <div class="text-center p-4 bg-blue-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ latestAnalytics?.followers || 0 }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Followers</p>
              </div>
              <div class="text-center p-4 bg-green-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ latestAnalytics?.total_posts || 0 }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Posts</p>
              </div>
              <div class="text-center p-4 bg-purple-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ latestAnalytics?.reach || 0 }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Reach</p>
              </div>
              <div class="text-center p-4 bg-pink-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ latestAnalytics?.total_engagement || 0 }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Engagement</p>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12 text-gray-500">
            No analytics data available
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Trash2, X, BarChart3, Users, Twitter, Facebook, Instagram, Linkedin } from 'lucide-vue-next'
import { useAccountsStore } from '../stores/accounts'
import LineChart from '../components/charts/LineChart.vue'
import { format } from 'date-fns'

const accountsStore = useAccountsStore()

const showAddModal = ref(false)
const showAnalyticsModal = ref(false)
const formData = ref({
  platform: '',
  account_name: '',
  account_id: '',
  access_token: ''
})

const accounts = computed(() => accountsStore.accounts)
const accountAnalytics = computed(() => accountsStore.accountAnalytics)
const latestAnalytics = computed(() => accountAnalytics.value[0])

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return format(new Date(dateString), 'MMM dd, yyyy')
}

const getPlatformIcon = (platform) => {
  const icons = {
    twitter: Twitter,
    facebook: Facebook,
    instagram: Instagram,
    linkedin: Linkedin
  }
  return icons[platform.toLowerCase()] || Users
}

const getPlatformColor = (platform) => {
  const colors = {
    twitter: 'bg-blue-500',
    facebook: 'bg-blue-600',
    instagram: 'bg-pink-500',
    linkedin: 'bg-blue-700',
    youtube: 'bg-red-600',
    tiktok: 'bg-black'
  }
  return colors[platform.toLowerCase()] || 'bg-gray-500'
}

const closeModal = () => {
  showAddModal.value = false
  formData.value = {
    platform: '',
    account_name: '',
    account_id: '',
    access_token: ''
  }
}

const submitAccount = async () => {
  try {
    await accountsStore.createAccount(formData.value)
    closeModal()
    await accountsStore.fetchAccounts()
  } catch (error) {
    console.error('Error adding account:', error)
    alert('Failed to add account. Please check if the account ID already exists.')
  }
}

const deleteAccount = async (id) => {
  if (confirm('Are you sure you want to remove this account?')) {
    try {
      await accountsStore.deleteAccount(id)
      await accountsStore.fetchAccounts()
    } catch (error) {
      console.error('Error deleting account:', error)
      alert('Failed to delete account. Please try again.')
    }
  }
}

const viewAnalytics = async (id) => {
  await accountsStore.fetchAccountAnalytics(id, 30)
  showAnalyticsModal.value = true
}

onMounted(() => {
  accountsStore.fetchAccounts()
})
</script>
