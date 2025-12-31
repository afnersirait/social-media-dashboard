<template>
  <div class="space-y-6">
    <!-- Time Range Selector -->
    <div class="card">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">Analytics Overview</h3>
        <select
          v-model="selectedDays"
          @change="loadData"
          class="select"
        >
          <option :value="7">Last 7 days</option>
          <option :value="30">Last 30 days</option>
          <option :value="90">Last 90 days</option>
        </select>
      </div>
    </div>

    <!-- Engagement Trends -->
    <div class="card">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Engagement Over Time</h3>
      <LineChart
        v-if="trends.length"
        :data="trends"
        :y-keys="['likes', 'comments', 'shares', 'views']"
        :colors="['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']"
        :height="400"
      />
      <div v-else class="h-[400px] flex items-center justify-center text-gray-500 dark:text-gray-400">
        Loading data...
      </div>
    </div>

    <!-- Platform Comparison -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Platform Followers</h3>
        <BarChart
          v-if="platformStats.length"
          :data="platformStats"
          x-key="platform"
          y-key="followers"
          color="#3b82f6"
          :height="300"
        />
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Platform Engagement</h3>
        <BarChart
          v-if="platformStats.length"
          :data="platformStats"
          x-key="platform"
          y-key="engagement"
          color="#10b981"
          :height="300"
        />
      </div>
    </div>

    <!-- Demographics -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Age Distribution</h3>
        <PieChart
          v-if="demographics?.age_groups"
          :data="demographics.age_groups"
          label-key="range"
          value-key="percentage"
          :height="300"
        />
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Gender Distribution</h3>
        <PieChart
          v-if="demographics?.gender"
          :data="demographics.gender"
          label-key="type"
          value-key="percentage"
          :colors="['#3b82f6', '#ec4899', '#8b5cf6']"
          :height="300"
        />
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Top Locations</h3>
        <div v-if="demographics?.locations" class="space-y-3">
          <div
            v-for="location in demographics.locations"
            :key="location.country"
            class="flex items-center justify-between"
          >
            <span class="text-sm text-gray-700 dark:text-gray-200">{{ location.country }}</span>
            <div class="flex items-center space-x-2">
              <div class="w-32 h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                <div
                  class="h-full bg-primary-600 rounded-full"
                  :style="{ width: `${location.percentage}%` }"
                ></div>
              </div>
              <span class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ location.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Top Posts Table -->
    <div class="card">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Top Performing Posts</h3>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b dark:border-gray-700">
              <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-200">Content</th>
              <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-200">Platform</th>
              <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-200">Likes</th>
              <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-200">Comments</th>
              <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-200">Shares</th>
              <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-200">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="post in topPosts"
              :key="post.id"
              class="border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <td class="py-3 px-4 text-sm text-gray-800 dark:text-gray-200">{{ post.content }}</td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 text-xs font-medium text-primary-600 dark:text-primary-400 bg-primary-100 dark:bg-primary-900/30 rounded">
                  {{ post.platform }}
                </span>
              </td>
              <td class="py-3 px-4 text-center text-sm text-gray-600 dark:text-gray-300">{{ post.likes.toLocaleString() }}</td>
              <td class="py-3 px-4 text-center text-sm text-gray-600 dark:text-gray-300">{{ post.comments.toLocaleString() }}</td>
              <td class="py-3 px-4 text-center text-sm text-gray-600 dark:text-gray-300">{{ post.shares.toLocaleString() }}</td>
              <td class="py-3 px-4 text-center text-sm font-medium text-gray-800 dark:text-gray-100">
                {{ post.total_engagement.toLocaleString() }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import LineChart from '../components/charts/LineChart.vue'
import BarChart from '../components/charts/BarChart.vue'
import PieChart from '../components/charts/PieChart.vue'
import { useAnalyticsStore } from '../stores/analytics'

const analyticsStore = useAnalyticsStore()
const selectedDays = ref(30)

const trends = computed(() => analyticsStore.engagementTrends)
const platformStats = computed(() => analyticsStore.platformStats)
const demographics = computed(() => analyticsStore.demographics)
const topPosts = computed(() => analyticsStore.topPosts)

const loadData = async () => {
  await Promise.all([
    analyticsStore.fetchEngagementTrends(selectedDays.value),
    analyticsStore.fetchPlatformStats(),
    analyticsStore.fetchDemographics(),
    analyticsStore.fetchTopPosts(10)
  ])
}

onMounted(() => {
  loadData()
})
</script>
