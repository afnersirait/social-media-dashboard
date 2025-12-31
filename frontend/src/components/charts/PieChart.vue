<template>
  <div ref="chartContainer" class="w-full h-full flex items-center justify-center"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  labelKey: {
    type: String,
    required: true
  },
  valueKey: {
    type: String,
    required: true
  },
  colors: {
    type: Array,
    default: () => ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
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

  const width = Math.min(chartContainer.value.clientWidth, props.height)
  const height = props.height
  const radius = Math.min(width, height) / 2 - 40

  // Create SVG
  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', `translate(${width / 2},${height / 2})`)

  // Create color scale
  const color = d3.scaleOrdinal()
    .domain(props.data.map(d => d[props.labelKey]))
    .range(props.colors)

  // Create pie layout
  const pie = d3.pie()
    .value(d => d[props.valueKey])
    .sort(null)

  // Create arc generator
  const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

  const arcHover = d3.arc()
    .innerRadius(0)
    .outerRadius(radius + 10)

  // Draw pie slices
  const arcs = svg.selectAll('.arc')
    .data(pie(props.data))
    .enter()
    .append('g')
    .attr('class', 'arc')

  arcs.append('path')
    .attr('d', arc)
    .attr('fill', d => color(d.data[props.labelKey]))
    .attr('stroke', 'white')
    .attr('stroke-width', 2)
    .style('cursor', 'pointer')
    .on('mouseover', function(event, d) {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('d', arcHover)
      
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
          <strong>${d.data[props.labelKey]}</strong><br/>
          ${d.data[props.valueKey].toLocaleString()}<br/>
          ${((d.data[props.valueKey] / d3.sum(props.data, d => d[props.valueKey])) * 100).toFixed(1)}%
        `)
        .style('left', `${event.pageX - chartContainer.value.getBoundingClientRect().left + 10}px`)
        .style('top', `${event.pageY - chartContainer.value.getBoundingClientRect().top - 10}px`)
    })
    .on('mouseout', function() {
      d3.select(this)
        .transition()
        .duration(200)
        .attr('d', arc)
      
      d3.select(chartContainer.value).selectAll('.tooltip').remove()
    })
    .transition()
    .duration(800)
    .attrTween('d', function(d) {
      const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d)
      return function(t) {
        return arc(interpolate(t))
      }
    })

  // Add labels
  arcs.append('text')
    .attr('transform', d => `translate(${arc.centroid(d)})`)
    .attr('text-anchor', 'middle')
    .style('font-size', '12px')
    .style('font-weight', '600')
    .style('fill', 'white')
    .text(d => {
      const percentage = (d.data[props.valueKey] / d3.sum(props.data, d => d[props.valueKey])) * 100
      return percentage > 5 ? `${percentage.toFixed(0)}%` : ''
    })
    .style('opacity', 0)
    .transition()
    .delay(800)
    .duration(400)
    .style('opacity', 1)

  // Add legend
  const legend = svg.append('g')
    .attr('transform', `translate(${radius + 20}, ${-radius})`)

  const legendItems = legend.selectAll('.legend-item')
    .data(props.data)
    .enter()
    .append('g')
    .attr('class', 'legend-item')
    .attr('transform', (d, i) => `translate(0, ${i * 25})`)

  legendItems.append('rect')
    .attr('width', 12)
    .attr('height', 12)
    .attr('fill', d => color(d[props.labelKey]))
    .attr('rx', 2)

  legendItems.append('text')
    .attr('x', 18)
    .attr('y', 10)
    .style('font-size', '12px')
    .style('fill', '#374151')
    .text(d => d[props.labelKey])
}

onMounted(() => {
  drawChart()
  window.addEventListener('resize', drawChart)
})

watch(() => props.data, () => {
  drawChart()
}, { deep: true })
</script>
