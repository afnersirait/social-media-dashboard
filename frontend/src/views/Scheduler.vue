<template>
  <div class="space-y-6">
    <!-- Header with Create Button -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100">Content Scheduler</h2>
      <button @click="showCreateModal = true" class="btn btn-primary">
        <Plus class="w-5 h-5 mr-2" />
        Schedule Post
      </button>
    </div>

    <!-- Scheduled Posts -->
    <div class="card">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Upcoming Posts</h3>
      <div v-if="scheduledPosts.length" class="space-y-4">
        <div
          v-for="post in scheduledPosts"
          :key="post.id"
          class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary-300 dark:hover:border-primary-600 transition-colors"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-2">
                <span class="px-2 py-1 text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-100 dark:bg-primary-900/30 rounded">
                  {{ getAccountName(post.account_id) }}
                </span>
                <span class="text-xs text-gray-500 dark:text-gray-400">
                  <Calendar class="w-3 h-3 inline mr-1" />
                  {{ formatDate(post.scheduled_time) }}
                </span>
              </div>
              <p class="text-sm text-gray-800 dark:text-gray-200">{{ post.content }}</p>
              <div v-if="post.media_url" class="mt-2">
                <span class="text-xs text-gray-500 dark:text-gray-400">📎 Media attached</span>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="editPost(post)"
                class="p-2 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <Edit2 class="w-4 h-4" />
              </button>
              <button
                @click="deletePost(post.id)"
                class="p-2 text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-12 text-gray-500 dark:text-gray-400">
        <Calendar class="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No scheduled posts yet</p>
        <button @click="showCreateModal = true" class="mt-4 btn btn-primary">
          Create Your First Post
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100">
              {{ editingPost ? 'Edit Post' : 'Schedule New Post' }}
            </h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300">
              <X class="w-6 h-6" />
            </button>
          </div>

          <form @submit.prevent="submitPost" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Account</label>
              <select v-model="formData.account_id" required class="select">
                <option value="">Select an account</option>
                <option v-for="account in accounts" :key="account.id" :value="account.id">
                  {{ account.platform }} - {{ account.account_name }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Content</label>
              <textarea
                v-model="formData.content"
                required
                rows="6"
                class="textarea"
                placeholder="What's on your mind?"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Media URL (optional)</label>
              <input
                v-model="formData.media_url"
                type="url"
                class="input"
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Post Type</label>
              <select v-model="formData.post_type" class="select">
                <option value="text">Text</option>
                <option value="image">Image</option>
                <option value="video">Video</option>
                <option value="link">Link</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Schedule Time</label>
              <input
                v-model="formData.scheduled_time"
                type="datetime-local"
                class="input"
              />
            </div>

            <div class="flex items-center justify-end space-x-3 pt-4">
              <button type="button" @click="closeModal" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary">
                {{ editingPost ? 'Update' : 'Schedule' }} Post
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Calendar, Edit2, Trash2, X } from 'lucide-vue-next'
import { usePostsStore } from '../stores/posts'
import { useAccountsStore } from '../stores/accounts'
import { format } from 'date-fns'

const postsStore = usePostsStore()
const accountsStore = useAccountsStore()

const showCreateModal = ref(false)
const editingPost = ref(null)
const formData = ref({
  account_id: '',
  content: '',
  media_url: '',
  post_type: 'text',
  scheduled_time: ''
})

const scheduledPosts = computed(() => postsStore.scheduledPosts)
const accounts = computed(() => accountsStore.accounts)

const formatDate = (dateString) => {
  if (!dateString) return ''
  return format(new Date(dateString), 'MMM dd, yyyy HH:mm')
}

const getAccountName = (accountId) => {
  const account = accounts.value.find(a => a.id === accountId)
  return account ? `${account.platform} - ${account.account_name}` : 'Unknown'
}

const closeModal = () => {
  showCreateModal.value = false
  editingPost.value = null
  formData.value = {
    account_id: '',
    content: '',
    media_url: '',
    post_type: 'text',
    scheduled_time: ''
  }
}

const editPost = (post) => {
  editingPost.value = post
  formData.value = {
    account_id: post.account_id,
    content: post.content,
    media_url: post.media_url || '',
    post_type: post.post_type,
    scheduled_time: post.scheduled_time ? new Date(post.scheduled_time).toISOString().slice(0, 16) : ''
  }
  showCreateModal.value = true
}

const submitPost = async () => {
  try {
    const data = {
      ...formData.value,
      scheduled_time: formData.value.scheduled_time ? new Date(formData.value.scheduled_time).toISOString() : null
    }

    if (editingPost.value) {
      await postsStore.updatePost(editingPost.value.id, data)
    } else {
      await postsStore.createPost(data)
    }

    closeModal()
    await postsStore.fetchScheduledPosts()
  } catch (error) {
    console.error('Error saving post:', error)
    alert('Failed to save post. Please try again.')
  }
}

const deletePost = async (id) => {
  if (confirm('Are you sure you want to delete this post?')) {
    try {
      await postsStore.deletePost(id)
      await postsStore.fetchScheduledPosts()
    } catch (error) {
      console.error('Error deleting post:', error)
      alert('Failed to delete post. Please try again.')
    }
  }
}

onMounted(async () => {
  await Promise.all([
    postsStore.fetchScheduledPosts(),
    accountsStore.fetchAccounts()
  ])
})
</script>
