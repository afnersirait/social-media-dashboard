<template>
  <div class="stat-card">
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ title }}</p>
        <p class="mt-2 text-3xl font-bold text-gray-900 dark:text-gray-100">{{ formattedValue }}</p>
        <div v-if="change !== undefined" class="mt-2 flex items-center">
          <component
            :is="changeIcon"
            :class="changeColor"
            class="w-4 h-4 mr-1"
          />
          <span :class="changeColor" class="text-sm font-medium">
            {{ Math.abs(change) }}%
          </span>
          <span class="text-sm text-gray-600 dark:text-gray-400 ml-1">vs last period</span>
        </div>
      </div>
      <div :class="iconBgColor" class="p-3 rounded-lg">
        <component :is="icon" :class="iconColor" class="w-6 h-6" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'

const props = defineProps({
  title: String,
  value: [Number, String],
  change: Number,
  icon: Object,
  iconColor: {
    type: String,
    default: 'text-primary-600'
  },
  iconBgColor: {
    type: String,
    default: 'bg-primary-100'
  },
  format: {
    type: String,
    default: 'number'
  }
})

const formattedValue = computed(() => {
  if (props.format === 'number') {
    return new Intl.NumberFormat().format(props.value)
  } else if (props.format === 'percent') {
    return `${props.value}%`
  }
  return props.value
})

const changeIcon = computed(() => {
  return props.change >= 0 ? TrendingUp : TrendingDown
})

const changeColor = computed(() => {
  return props.change >= 0 ? 'text-green-600' : 'text-red-600'
})
</script>
