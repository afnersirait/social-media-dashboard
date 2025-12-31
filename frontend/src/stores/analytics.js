import { defineStore } from 'pinia'
import { ref } from 'vue'
import { analyticsAPI } from '../utils/api'

export const useAnalyticsStore = defineStore('analytics', () => {
  const dashboardStats = ref(null)
  const engagementTrends = ref([])
  const platformStats = ref([])
  const topPosts = ref([])
  const demographics = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchDashboardStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await analyticsAPI.getDashboardStats()
      dashboardStats.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching dashboard stats:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchEngagementTrends = async (days = 30) => {
    loading.value = true
    error.value = null
    try {
      const response = await analyticsAPI.getEngagementTrends(days)
      engagementTrends.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching engagement trends:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPlatformStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await analyticsAPI.getPlatformStats()
      platformStats.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching platform stats:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchTopPosts = async (limit = 10) => {
    loading.value = true
    error.value = null
    try {
      const response = await analyticsAPI.getTopPosts(limit)
      topPosts.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching top posts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchDemographics = async (accountId = null) => {
    loading.value = true
    error.value = null
    try {
      const response = await analyticsAPI.getDemographics(accountId)
      demographics.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching demographics:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    dashboardStats,
    engagementTrends,
    platformStats,
    topPosts,
    demographics,
    loading,
    error,
    fetchDashboardStats,
    fetchEngagementTrends,
    fetchPlatformStats,
    fetchTopPosts,
    fetchDemographics
  }
})
