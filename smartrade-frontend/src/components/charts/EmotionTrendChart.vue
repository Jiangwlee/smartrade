<template>
  <div>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'
import VChart, { THEME_KEY } from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  MarkPointComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { ComposeOption } from 'echarts/core'
import type { LineSeriesOption } from 'echarts/charts'
import type {
  TitleComponentOption,
  TooltipComponentOption,
  GridComponentOption,
  MarkPointComponentOption
} from 'echarts/components'
import { getEmotionTrend } from '@/services/requests'

use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  MarkPointComponent,
  LineChart,
  CanvasRenderer
])

type EChartsOption = ComposeOption<
  | TitleComponentOption
  | TooltipComponentOption
  | GridComponentOption
  | MarkPointComponentOption
  | LineSeriesOption
>

const props = defineProps<{
  date: string
}>()

const datasource = [
    ['日期', '1进2', '2进3', '3进4', '4进5', '5进6', '6进7', '7进8', '8进9', '9进10'],
    ['2024-12-01', 90, 80, 70, 60, 50, 40, 30, 20, 10],
    ['2024-12-02', 90, 80, 70, 60, 50, 40, 30, 20, 10],
    ['2024-12-03', '-', 80, 70, 60, 50, 40, 30, 20, 10],
    ['2024-12-04', 90, 80, 70, 60, 50, 40, 30, 20, 10],
    ['2024-12-05', 90, 80, 70, 60, 50, 40, 30, 20, 10],
    ['2024-12-06', 90, 80, 70, 60, 50, 40, 30, 20, 10],
]
const option = ref<EChartsOption>({
  title: {
    text: '晋级率趋势',
    left: 'center',
  },
  dataset: {
    source: datasource
  },
  legend: {
    // Try 'horizontal'
    orient: 'horizontal',
    top: 30,
    selected: {
      '1进2': true, // 默认显示
      '2进3': true, // 默认显示
      '3进4': false, // 默认隐藏
      '4进5': false, // 默认隐藏
      '5进6': false, // 默认隐藏
      '6进7': false, // 默认隐藏
      '7进8': false, // 默认隐藏
      '8进9': false, // 默认隐藏
      '9进10': false, // 默认隐藏
    },
  },
  tooltip: {
    trigger: 'item',
    formatter: function (params: any) {
      const seriesName = params.seriesName; // 序列名称
      const value = params.value[params.componentIndex + 1]; // 当前数据点的值
      const date = params.value[0]; // 日期
      return `${date}<br/>${seriesName}: ${value !== '-' ? value + '%' : '暂无数据'}`;
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
    max: 100,
    axisLabel: {
      formatter: '{value}%',
    },
    axisLine: {
      lineStyle: { color: '#ccc' },
    },
  },
  series: [
    {
      name: '1进2',
      type: 'line',
      connectNulls: false,
      symbolSize: (value) => { return value[1] > 40 ? 10 : 4;}
    },
    {
      name: '2进3',
      type: 'line',
      connectNulls: false,
      symbolSize: (value) => { return value[2] > 40 ? 10 : 4;}
    },
    {
      name: '3进4',
      type: 'line',
      connectNulls: false,
    },
    {
      name: '4进5',
      type: 'line',
      connectNulls: false,
    },
    {
      name: '5进6',
      type: 'line',
      connectNulls: false,
    },
    {
      name: '6进7',
      type: 'line',
      connectNulls: false,
    },
    {
      name: '7进8',
      type: 'line',
      connectNulls: false,
    },
    {
      name: '8进9',
      type: 'line',
      connectNulls: false,
    },
    {
      name: '9进10',
      type: 'line',
      connectNulls: false,
    },
  ],
  grid: {
    left: '10%',
    right: '10%',
    bottom: '10%',
  },
});

const fetchData = async () => {
  getEmotionTrend(props.date).then(
    (resp) => {
      option.value.dataset = {
        dimensions: ['日期', '1进2', '2进3', '3进4', '4进5', '5进6', '6进7', '7进8', '8进9', '9进10'],
        source: resp.data.data
      }
      console.log(option.value.dataset)
    }
  )
}

onMounted(() => {
  console.log("EmotionTrendChart is mounted")
  fetchData()
})

onUpdated(() => {
  console.log("EmotionTrendChart is updated")
  fetchData()
})

</script>

<style scoped>
.chart {
  height: 50vh;
}
</style>
