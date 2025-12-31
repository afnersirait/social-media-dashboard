<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="card">
      <div class="flex flex-wrap items-center gap-4">
        <div class="flex-1 min-w-[200px]">
          <select v-model="filters.status" @change="loadPosts" class="select">
            <option value="">All Status</option>
            <option value="draft">Draft</option>
            <option value="scheduled">Scheduled</option>
            <option value="published">Published</option>
            <option value="failed">Failed</option>
          </select>
        </div>
        <div class="flex-1 min-w-[200px]">
          <select v-model="filters.account_id" @change="loadPosts" class="select">
            <option value="">All Accounts</option>
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.platform }} - {{ account.account_name }}
            </option>
          </select>
        </div>
        <button @click="loadPosts" class="btn btn-primary">
          <RefreshCw class="w-4 h-4 mr-2" />
          Refresh
        </button>
      </div>
    </div>

    <!-- Posts Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="post in posts"
        :key="post.id"
        class="card hover:shadow-lg transition-shadow"
      >
        <div class="flex items-start justify-between mb-3">
          <span
            :class="getStatusColor(post.status)"
            class="px-2 py-1 text-xs font-medium rounded"
          >
            {{ post.status }}
          </span>
          <div class="flex items-center space-x-1">
            <button
              v-if="post.status === 'draft'"
              @click="publishPost(post.id)"
              class="p-1 text-green-600 hover:bg-green-50 rounded"
              title="Publish"
            >
              <Send class="w-4 h-4" />
            </button>
            <button
              @click="viewPost(post)"
              class="p-1 text-gray-600 hover:bg-gray-100 rounded"
              title="View"
            >
              <Eye class="w-4 h-4" />
            </button>
          </div>
        </div>

        <p class="text-sm text-gray-800 dark:text-gray-200 mb-3 line-clamp-3">{{ post.content }}</p>

        <div class="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400 mb-3">
          <span class="flex items-center">
            <Calendar class="w-3 h-3 mr-1" />
            {{ formatDate(post.published_time || post.created_at) }}
          </span>
          <span class="px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded">
            {{ getAccountName(post.account_id) }}
          </span>
        </div>

        <div v-if="post.status === 'published' && post.engagement" class="pt-3 border-t">
          <div class="grid grid-cols-4 gap-2 text-center">
            <div>
              <Heart class="w-4 h-4 mx-auto text-pink-500 mb-1" />
              <p class="text-xs font-medium">{{ post.engagement.likes }}</p>
            </div>
            <div>
              <MessageCircle class="w-4 h-4 mx-auto text-blue-500 mb-1" />
              <p class="text-xs font-medium">{{ post.engagement.comments }}</p>
            </div>
            <div>
              <Share2 class="w-4 h-4 mx-auto text-green-500 mb-1" />
              <p class="text-xs font-medium">{{ post.engagement.shares }}</p>
            </div>
            <div>
              <Eye class="w-4 h-4 mx-auto text-purple-500 mb-1" />
              <p class="text-xs font-medium">{{ post.engagement.views }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!posts.length" class="card text-center py-12">
      <FileText class="w-12 h-12 mx-auto mb-4 text-gray-400" />
      <p class="text-gray-500">No posts found</p>
    </div>

    <!-- View Modal -->
    <div
      v-if="selectedPost"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="selectedPost = null"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100">Post Details</h3>
            <button @click="selectedPost = null" class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">
              <X class="w-6 h-6" />
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Status</label>
              <span
                :class="getStatusColor(selectedPost.status)"
                class="inline-block px-3 py-1 text-sm font-medium rounded"
              >
                {{ selectedPost.status }}
              </span>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account</label>
              <p class="text-gray-800 dark:text-gray-200">{{ getAccountName(selectedPost.account_id) }}</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Content</label>
              <p class="text-gray-800 dark:text-gray-200 whitespace-pre-wrap">{{ selectedPost.content }}</p>
            </div>

            <div v-if="selectedPost.media_url">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Media</label>
              <a :href="selectedPost.media_url" target="_blank" class="text-primary-600 dark:text-primary-400 hover:underline">
                {{ selectedPost.media_url }}
              </a>
            </div>

            <div v-if="selectedPost.engagement" class="pt-4 border-t">
              <label class="block text-sm font-medium text-gray-700 mb-3">Engagement Metrics</label>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="text-center p-3 bg-pink-50 rounded-lg">
                  <Heart class="w-6 h-6 mx-auto text-pink-500 mb-2" />
                  <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ selectedPost.engagement.likes }}</p>
                  <p class="text-xs text-gray-600 dark:text-gray-400">Likes</p>
                </div>
                <div class="text-center p-3 bg-blue-50 rounded-lg">
                  <MessageCircle class="w-6 h-6 mx-auto text-blue-500 mb-2" />
                  <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ selectedPost.engagement.comments }}</p>
                  <p class="text-xs text-gray-600 dark:text-gray-400">Comments</p>
                </div>
                <div class="text-center p-3 bg-green-50 rounded-lg">
                  <Share2 class="w-6 h-6 mx-auto text-green-500 mb-2" />
                  <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ selectedPost.engagement.shares }}</p>
                  <p class="text-xs text-gray-600 dark:text-gray-400">Shares</p>
                </div>
                <div class="text-center p-3 bg-purple-50 rounded-lg">
                  <Eye class="w-6 h-6 mx-auto text-purple-500 mb-2" />
                  <p class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ selectedPost.engagement.views }}</p>
                  <p class="text-xs text-gray-600 dark:text-gray-400">Views</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Calendar, Heart, MessageCircle, Share2, Eye, Send, FileText, X, RefreshCw } from 'lucide-vue-next'
import { usePostsStore } from '../stores/posts'
import { useAccountsStore } from '../stores/accounts'
import { format } from 'date-fns'

const postsStore = usePostsStore()
const accountsStore = useAccountsStore()

const filters = ref({
  status: '',
  account_id: ''
})

const selectedPost = ref(null)

const posts = computed(() => postsStore.posts)
const accounts = computed(() => accountsStore.accounts)

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return format(new Date(dateString), 'MMM dd, yyyy')
}

const getAccountName = (accountId) => {
  const account = accounts.value.find(a => a.id === accountId)
  return account ? account.platform : 'Unknown'
}

const getStatusColor = (status) => {
  const colors = {
    draft: 'bg-gray-200 text-gray-700',
    scheduled: 'bg-blue-100 text-blue-700',
    published: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700'
  }
  return colors[status] || 'bg-gray-200 text-gray-700'
}

const loadPosts = async () => {
  const params = {}
  if (filters.value.status) params.status = filters.value.status
  if (filters.value.account_id) params.account_id = filters.value.account_id
  await postsStore.fetchPosts(params)
}

const viewPost = (post) => {
  selectedPost.value = post
}

const publishPost = async (id) => {
  if (confirm('Are you sure you want to publish this post?')) {
    try {
      await postsStore.publishPost(id)
      await loadPosts()
    } catch (error) {
      console.error('Error publishing post:', error)
      alert('Failed to publish post. Please try again.')
    }
  }
}

onMounted(async () => {
  await Promise.all([
    loadPosts(),
    accountsStore.fetchAccounts()
  ])
})
</script>
