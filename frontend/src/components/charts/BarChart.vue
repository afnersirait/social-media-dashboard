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
    required: true
  },
  yKey: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: '#3b82f6'
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

  const margin = { top: 20, right: 20, bottom: 60, left: 60 }
  const width = chartContainer.value.clientWidth - margin.left - margin.right
  const height = props.height - margin.top - margin.bottom

  // Create SVG
  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Create scales
  const x = d3.scaleBand()
    .domain(props.data.map(d => d[props.xKey]))
    .range([0, width])
    .padding(0.3)

  const y = d3.scaleLinear()
    .domain([0, d3.max(props.data, d => d[props.yKey]) * 1.1])
    .range([height, 0])

  // Add X axis
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .style('font-size', '12px')
    .style('fill', '#6b7280')
    .attr('transform', 'rotate(-45)')
    .style('text-anchor', 'end')

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

  // Add bars
  svg.selectAll('.bar')
    .data(props.data)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d[props.xKey]))
    .attr('y', height)
    .attr('width', x.bandwidth())
    .attr('height', 0)
    .attr('fill', props.color)
    .attr('rx', 4)
    .style('cursor', 'pointer')
    .on('mouseover', function(event, d) {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('opacity', 0.7)
      
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
          <strong>${d[props.xKey]}</strong><br/>
          ${d[props.yKey].toLocaleString()}
        `)
        .style('left', `${event.pageX - chartContainer.value.getBoundingClientRect().left + 10}px`)
        .style('top', `${event.pageY - chartContainer.value.getBoundingClientRect().top - 10}px`)
    })
    .on('mouseout', function() {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('opacity', 1)
      
      d3.select(chartContainer.value).selectAll('.tooltip').remove()
    })
    .transition()
    .duration(800)
    .attr('y', d => y(d[props.yKey]))
    .attr('height', d => height - y(d[props.yKey]))
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
