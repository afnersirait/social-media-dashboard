import { defineStore } from 'pinia'
import { ref } from 'vue'
import { postsAPI } from '../utils/api'

export const usePostsStore = defineStore('posts', () => {
  const posts = ref([])
  const scheduledPosts = ref([])
  const currentPost = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchPosts = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await postsAPI.getPosts(params)
      posts.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching posts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchScheduledPosts = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await postsAPI.getScheduledPosts()
      scheduledPosts.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching scheduled posts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPost = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await postsAPI.getPost(id)
      currentPost.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching post:', err)
    } finally {
      loading.value = false
    }
  }

  const createPost = async (data) => {
    loading.value = true
    error.value = null
    try {
      const response = await postsAPI.createPost(data)
      posts.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error creating post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updatePost = async (id, data) => {
    loading.value = true
    error.value = null
    try {
      const response = await postsAPI.updatePost(id, data)
      const index = posts.value.findIndex(p => p.id === id)
      if (index !== -1) {
        posts.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error updating post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deletePost = async (id) => {
    loading.value = true
    error.value = null
    try {
      await postsAPI.deletePost(id)
      posts.value = posts.value.filter(p => p.id !== id)
      scheduledPosts.value = scheduledPosts.value.filter(p => p.id !== id)
    } catch (err) {
      error.value = err.message
      console.error('Error deleting post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const publishPost = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await postsAPI.publishPost(id)
      const index = posts.value.findIndex(p => p.id === id)
      if (index !== -1) {
        posts.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error publishing post:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    posts,
    scheduledPosts,
    currentPost,
    loading,
    error,
    fetchPosts,
    fetchScheduledPosts,
    fetchPost,
    createPost,
    updatePost,
    deletePost,
    publishPost
  }
})
