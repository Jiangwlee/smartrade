<template>
  <v-chart class="chart" :option="option" autoresize />
</template>

<script lang="ts" setup>
import { ref, provide, onMounted, onUpdated } from 'vue'
import { type LimitUpLeadingStock } from '@/services/types'
import VChart, { THEME_KEY } from 'vue-echarts'
import { getLeadingStocks } from '@/services/requests'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([GridComponent, LineChart, CanvasRenderer])

provide(THEME_KEY, 'dark')

const props = defineProps<{
  date: string
}>()

const data = ref<LimitUpLeadingStock[]>([])

const option = ref({
  xAxis: {
    type: 'category',
    data: ['']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [0],
      type: 'line'
    }
  ]
})

const fetchData = async () => {
  getLeadingStocks(props.date).then(
    (resp) => {
      const category = resp.data.data.map((value) => value.date)
      const height = resp.data.data.map((value) => value.continuous_num)
      option.value.xAxis.data = category
      option.value.series[0].data = height
    }
  )
}

onMounted(() => {
  console.log("LineChart is mounted")
  fetchData()
})

onUpdated(() => {
  console.log("LineChart is updated")
  fetchData()
})
</script>

<style scoped>
.chart {
  height: 50vh;
}
</style>
