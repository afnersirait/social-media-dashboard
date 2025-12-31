<template>
  <div class="space-y-6">
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        title="Total Followers"
        :value="stats?.total_followers || 0"
        :change="stats?.growth_rate || 0"
        :icon="Users"
        iconColor="text-blue-600"
        iconBgColor="bg-blue-100"
      />
      <StatCard
        title="Total Posts"
        :value="stats?.total_posts || 0"
        :icon="FileText"
        iconColor="text-green-600"
        iconBgColor="bg-green-100"
      />
      <StatCard
        title="Total Engagement"
        :value="stats?.total_engagement || 0"
        :icon="Heart"
        iconColor="text-pink-600"
        iconBgColor="bg-pink-100"
      />
      <StatCard
        title="Engagement Rate"
        :value="stats?.engagement_rate || 0"
        :icon="TrendingUp"
        iconColor="text-purple-600"
        iconBgColor="bg-purple-100"
        format="percent"
      />
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Engagement Trends -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Engagement Trends</h3>
        <LineChart
          v-if="trends.length"
          :data="trends"
          :y-keys="['likes', 'comments', 'shares']"
          :colors="['#3b82f6', '#10b981', '#f59e0b']"
          :height="300"
        />
        <div v-else class="h-[300px] flex items-center justify-center text-gray-500">
          No data available
        </div>
      </div>

      <!-- Platform Stats -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Platform Distribution</h3>
        <BarChart
          v-if="platformStats.length"
          :data="platformStats"
          x-key="platform"
          y-key="followers"
          :height="300"
        />
        <div v-else class="h-[300px] flex items-center justify-center text-gray-500">
          No data available
        </div>
      </div>
    </div>

    <!-- Top Posts and Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Top Posts -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Top Performing Posts</h3>
        <div class="space-y-3">
          <div
            v-for="post in topPosts.slice(0, 5)"
            :key="post.id"
            class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <p class="text-sm text-gray-800 dark:text-gray-200 font-medium">{{ post.content }}</p>
                <div class="flex items-center mt-2 space-x-4 text-xs text-gray-600 dark:text-gray-400">
                  <span class="flex items-center">
                    <Heart class="w-3 h-3 mr-1" />
                    {{ post.likes }}
                  </span>
                  <span class="flex items-center">
                    <MessageCircle class="w-3 h-3 mr-1" />
                    {{ post.comments }}
                  </span>
                  <span class="flex items-center">
                    <Share2 class="w-3 h-3 mr-1" />
                    {{ post.shares }}
                  </span>
                </div>
              </div>
              <span class="px-2 py-1 text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-100 dark:bg-primary-900/30 rounded">
                {{ post.platform }}
              </span>
            </div>
          </div>
          <div v-if="!topPosts.length" class="text-center text-gray-500 dark:text-gray-400 py-8">
            No posts yet
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Quick Actions</h3>
        <div class="space-y-3">
          <router-link
            to="/scheduler"
            class="flex items-center p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors group"
          >
            <div class="p-3 bg-primary-600 rounded-lg mr-4">
              <Calendar class="w-6 h-6 text-white" />
            </div>
            <div>
              <h4 class="font-medium text-gray-800 dark:text-gray-200 group-hover:text-primary-600 dark:group-hover:text-primary-400">Schedule Post</h4>
              <p class="text-sm text-gray-600 dark:text-gray-400">Plan your content calendar</p>
            </div>
          </router-link>

          <router-link
            to="/analytics"
            class="flex items-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors group"
          >
            <div class="p-3 bg-green-600 rounded-lg mr-4">
              <BarChart3 class="w-6 h-6 text-white" />
            </div>
            <div>
              <h4 class="font-medium text-gray-800 dark:text-gray-200 group-hover:text-green-600 dark:group-hover:text-green-400">View Analytics</h4>
              <p class="text-sm text-gray-600 dark:text-gray-400">Deep dive into your metrics</p>
            </div>
          </router-link>

          <router-link
            to="/accounts"
            class="flex items-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors group"
          >
            <div class="p-3 bg-purple-600 rounded-lg mr-4">
              <Users class="w-6 h-6 text-white" />
            </div>
            <div>
              <h4 class="font-medium text-gray-800 dark:text-gray-200 group-hover:text-purple-600 dark:group-hover:text-purple-400">Manage Accounts</h4>
              <p class="text-sm text-gray-600 dark:text-gray-400">Connect social platforms</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { Users, FileText, Heart, TrendingUp, Calendar, BarChart3, MessageCircle, Share2 } from 'lucide-vue-next'
import StatCard from '../components/StatCard.vue'
import LineChart from '../components/charts/LineChart.vue'
import BarChart from '../components/charts/BarChart.vue'
import { useAnalyticsStore } from '../stores/analytics'

const analyticsStore = useAnalyticsStore()

const stats = computed(() => analyticsStore.dashboardStats)
const trends = computed(() => analyticsStore.engagementTrends)
const platformStats = computed(() => analyticsStore.platformStats)
const topPosts = computed(() => analyticsStore.topPosts)

onMounted(async () => {
  await Promise.all([
    analyticsStore.fetchDashboardStats(),
    analyticsStore.fetchEngagementTrends(30),
    analyticsStore.fetchPlatformStats(),
    analyticsStore.fetchTopPosts(10)
  ])
})
</script>
