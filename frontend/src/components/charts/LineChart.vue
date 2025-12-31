<template>
  <div ref="chartContainer" class="w-full h-full"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  xKey: {
    type: String,
    default: 'date'
  },
  yKeys: {
    type: Array,
    required: true
  },
  colors: {
    type: Array,
    default: () => ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
  },
  height: {
    type: Number,
    default: 300
  }
})

const chartContainer = ref(null)

const drawChart = () => {
  if (!chartContainer.value || !props.data.length) return

  // Clear previous chart
  d3.select(chartContainer.value).selectAll('*').remove()

  const margin = { top: 20, right: 120, bottom: 40, left: 60 }
  const width = chartContainer.value.clientWidth - margin.left - margin.right
  const height = props.height - margin.top - margin.bottom

  // Create SVG
  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Parse dates
  const parseDate = d3.timeParse('%Y-%m-%d')
  const data = props.data.map(d => ({
    ...d,
    [props.xKey]: parseDate(d[props.xKey])
  }))

  // Create scales
  const x = d3.scaleTime()
    .domain(d3.extent(data, d => d[props.xKey]))
    .range([0, width])

  const maxY = d3.max(data, d => 
    d3.max(props.yKeys, key => d[key])
  )

  const y = d3.scaleLinear()
    .domain([0, maxY * 1.1])
    .range([height, 0])

  // Create line generator
  const line = d3.line()
    .x(d => x(d[props.xKey]))
    .y((d, i, key) => y(d[key]))
    .curve(d3.curveMonotoneX)

  // Add X axis
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(6))
    .selectAll('text')
    .style('font-size', '12px')
    .style('fill', '#6b7280')

  // Add Y axis
  svg.append('g')
    .call(d3.axisLeft(y).ticks(5))
    .selectAll('text')
    .style('font-size', '12px')
    .style('fill', '#6b7280')

  // Add grid lines
  svg.append('g')
    .attr('class', 'grid')
    .attr('opacity', 0.1)
    .call(d3.axisLeft(y)
      .ticks(5)
      .tickSize(-width)
      .tickFormat('')
    )

  // Draw lines
  props.yKeys.forEach((key, index) => {
    const lineData = data.map(d => ({ ...d, value: d[key] }))
    
    svg.append('path')
      .datum(lineData)
      .attr('fill', 'none')
      .attr('stroke', props.colors[index])
      .attr('stroke-width', 2)
      .attr('d', d3.line()
        .x(d => x(d[props.xKey]))
        .y(d => y(d.value))
        .curve(d3.curveMonotoneX)
      )

    // Add dots
    svg.selectAll(`.dot-${key}`)
      .data(lineData)
      .enter()
      .append('circle')
      .attr('class', `dot-${key}`)
      .attr('cx', d => x(d[props.xKey]))
      .attr('cy', d => y(d.value))
      .attr('r', 4)
      .attr('fill', props.colors[index])
      .attr('stroke', 'white')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('mouseover', function(event, d) {
        d3.select(this).attr('r', 6)
        
        // Show tooltip
        const tooltip = d3.select(chartContainer.value)
          .append('div')
          .attr('class', 'tooltip')
          .style('position', 'absolute')
          .style('background', 'rgba(0, 0, 0, 0.8)')
          .style('color', 'white')
          .style('padding', '8px 12px')
          .style('border-radius', '4px')
          .style('font-size', '12px')
          .style('pointer-events', 'none')
          .style('z-index', '1000')
          .html(`
            <strong>${key}</strong><br/>
            ${d.value.toLocaleString()}<br/>
            ${d[props.xKey].toLocaleDateString()}
          `)
          .style('left', `${event.pageX - chartContainer.value.getBoundingClientRect().left + 10}px`)
          .style('top', `${event.pageY - chartContainer.value.getBoundingClientRect().top - 10}px`)
      })
      .on('mouseout', function() {
        d3.select(this).attr('r', 4)
        d3.select(chartContainer.value).selectAll('.tooltip').remove()
      })
  })

  // Add legend
  const legend = svg.append('g')
    .attr('transform', `translate(${width + 10}, 0)`)

  props.yKeys.forEach((key, index) => {
    const legendRow = legend.append('g')
      .attr('transform', `translate(0, ${index * 25})`)

    legendRow.append('rect')
      .attr('width', 12)
      .attr('height', 12)
      .attr('fill', props.colors[index])
      .attr('rx', 2)

    legendRow.append('text')
      .attr('x', 18)
      .attr('y', 10)
      .style('font-size', '12px')
      .style('fill', '#374151')
      .text(key.charAt(0).toUpperCase() + key.slice(1))
  })
}

onMounted(() => {
  drawChart()
  window.addEventListener('resize', drawChart)
})

watch(() => props.data, () => {
  drawChart()
}, { deep: true })
</script>

<style scoped>
.grid line {
  stroke: #e5e7eb;
}
</style>
