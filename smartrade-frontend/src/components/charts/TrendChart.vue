<template>
  <v-chart class="chart" :option="option" autoresize />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import {
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { ComposeOption } from 'echarts/core'
import type { BarSeriesOption } from 'echarts/charts'
import type {
  TooltipComponentOption,
  LegendComponentOption,
  GridComponentOption,
} from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'

use([
  TooltipComponent,
  LegendComponent,
  GridComponent,
  BarChart,
  CanvasRenderer,
])

type EChartsOption = ComposeOption<
  | TooltipComponentOption
  | LegendComponentOption
  | GridComponentOption
  | BarSeriesOption
>

const props = defineProps<{
  source: Array<Array<string | number>>
}>()

const option = computed<EChartsOption>(() => ({
  dataset: {
    source: props.source,
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
    valueFormatter: (value) => {
      const num = Math.abs(Number(value))
      return '' + num
    },
  },
  legend: {
    data: ['涨停', '跌停'],
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: [
    {
      type: 'category',
      axisTick: {
        show: false,
      },
    },
  ],
  yAxis: [
    {
      type: 'value',
    },
  ],
  series: [
    {
      name: '涨停',
      type: 'bar',
      stack: 'Total',
      label: {
        show: true,
        position: 'top',
      },
      emphasis: {
        focus: 'series',
      },
      seriesLayoutBy: 'row',
      xAxisIndex: 0,
      yAxisIndex: 0,
      itemStyle: {
        color: '#ec7063', // 给系列指定颜色
      },
    },
    {
      name: '跌停',
      type: 'bar',
      stack: 'Total',
      label: {
        show: true,
        position: 'bottom',
        formatter: (params: any) => {
          if (Number(params.data[2]) == 0) {
            return ''
          } else {
            return '' + (0 - Number(params.data[2]))
          }
        },
      },
      emphasis: {
        focus: 'series',
      },
      seriesLayoutBy: 'row',
      xAxisIndex: 0,
      yAxisIndex: 0,
      itemStyle: {
        color: '#82e0aa', // 给系列指定颜色
      },
    },
  ],
}))
</script>

<style scoped>
.chart {
  height: 50vh;
}
</style>
