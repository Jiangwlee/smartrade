<template>
  <div>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'
import VChart, { THEME_KEY } from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  MarkPointComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { ComposeOption } from 'echarts/core'
import type { BarSeriesOption } from 'echarts/charts'
import type {
  TitleComponentOption,
  TooltipComponentOption,
  GridComponentOption,
  MarkPointComponentOption
} from 'echarts/components'
import { getZdtTrend } from '@/services/requests'

use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  MarkPointComponent,
  BarChart,
  CanvasRenderer
])

type EChartsOption = ComposeOption<
  | TitleComponentOption
  | TooltipComponentOption
  | GridComponentOption
  | MarkPointComponentOption
  | BarSeriesOption
>

const props = defineProps<{
  date: string
}>()

const option = ref<EChartsOption>({
  title: {
    text: '涨跌停分类趋势',
    left: 'center',
  },
  dataset: {
    source: []
  },
  legend: {
    // Try 'horizontal'
    orient: 'horizontal',
    top: 30,
  },
  tooltip: {
    trigger: 'item',
    formatter: function (params: any) {
      const seriesName = params.seriesName; // 序列名称
      const value = params.value; // 当前数据点的值
      const date = value['date']; // 日期
      return `${date}<br/>${seriesName}: ${value[seriesName]}`;
    },
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    axisLine: {
      lineStyle: { color: '#ccc' },
    },
  },
  yAxis: {
    type: 'value',
    min: 0,
    axisLine: {
      lineStyle: { color: '#ccc' },
    },
  },
  color: [
    '#3380ff',
    '#DAF7A6',
    '#af7ac5',
    '#1a814f',
    '#FF0000'
  ],
  emphasis: {
    focus: 'series',
    blurScope: 'coordinateSystem'
  },
  series: [
    {
      name: '涨停',
      type: 'bar',
      stack: 'total',
      label: {
        show: true
      },
    },
    {
      name: '一字板',
      type: 'bar',
      stack: 'total',
      label: {
        show: true
      }
    },
    {
      name: 'T字板',
      type: 'bar',
      stack: 'total'
    },
    {
      name: '天地板',
      type: 'bar',
      stack: 'total',
    },
    {
      name: '地天板',
      type: 'bar',
      stack: 'total'
    }
  ],
  grid: {
    left: '10%',
    right: '10%',
    bottom: '10%',
  },
});

const fetchData = async () => {
  getZdtTrend(props.date).then(
    (resp) => {
      option.value.dataset = {
        dimensions: ['date', '涨停', '一字板', 'T字板', '天地板', '地天板', '天地板股票', '地天板股票'],
        source: resp.data.data
      }
    }
  )
}

onMounted(() => {
  console.log("ZdtTrendChart is mounted")
  fetchData()
})

onUpdated(() => {
  console.log("ZdtTrendChart is updated")
  fetchData()
})

</script>

<style scoped>
.chart {
  height: 50vh;
}
</style>
