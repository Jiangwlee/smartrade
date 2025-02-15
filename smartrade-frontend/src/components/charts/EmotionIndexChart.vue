<template>
  <div>
    <v-chart class="chart" :option="option" autoresize />
  </div>

</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref, computed } from 'vue'

import VChart, { THEME_KEY } from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  MarkPointComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { ComposeOption } from 'echarts/core'
import type { LineSeriesOption } from 'echarts/charts'
import type {
  TitleComponentOption,
  TooltipComponentOption,
  GridComponentOption,
  LegendComponentOption,
  MarkPointComponentOption,
} from 'echarts/components'
import { getEmotionIndex } from '@/services/requests'

use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  MarkPointComponent,
  LineChart,
  LegendComponent,
  CanvasRenderer
])

type EChartsOption = ComposeOption<
  | TitleComponentOption
  | TooltipComponentOption
  | GridComponentOption
  | MarkPointComponentOption
  | LineSeriesOption
  | LegendComponentOption
>

const props = defineProps<{
  date: string
}>()

const datasource = [{}]

const option = ref<EChartsOption>({
  title: {
    text: '情绪指数趋势',
    left: 'center',
  },
  dataset: {
    source: datasource
  },
  legend: {
    // Try 'horizontal'
    // orient: 'vertical',
    top: 30,
    // selected: {
    //   '1进2': true, // 默认显示
    //   '2进3': true, // 默认显示
    //   '3进4': false, // 默认隐藏
    //   '4进5': false, // 默认隐藏
    //   '5进6': false, // 默认隐藏
    //   '6进7': false, // 默认隐藏
    //   '7进8': false, // 默认隐藏
    //   '8进9': false, // 默认隐藏
    //   '9进10': false, // 默认隐藏
    // },
  },
  tooltip: {
    trigger: 'item',
    // formatter: function (params: any) {
    //   console.log(params)
    //   const seriesName = params.seriesName; // 序列名称
    //   const value = params.value[params.componentIndex + 1]; // 当前数据点的值
    //   const date = params.value[0]; // 日期
    //   return `${date}<br/>${seriesName}: ${value !== '-' ? value + '%' : '暂无数据'}`;
    // },
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
    // max: 100,
    // axisLabel: {
    //   formatter: '{value}%',
    // },
    axisLine: {
      lineStyle: { color: '#ccc' },
    },
  },
  series: [
    {
      name: '天地板',
      type: 'line',
      encode: {
        x: 'date', // 将 x 轴关联到 "日期" 维度
        y: 'tdb_count',  // 将 y 轴关联到 "利润" 维度
        tooltip: ['tdb_count', 'tdb_stock']
      },
    },
    {
      name: '最高连板',
      type: 'line',
      encode: {
        x: 'date', // 将 x 轴关联到 "日期" 维度
        y: 'height',  // 将 y 轴关联到 "利润" 维度
        tooltip: ['height', 'height_stock']
      },
    },
    {
      name: '跌停数',
      type: 'line',
      encode: {
        x: 'date', // 将 x 轴关联到 "日期" 维度
        y: 'dt_count'  // 将 y 轴关联到 "利润" 维度
      }
    },
    {
      name: '连续跌停数',
      type: 'line',
      encode: {
        x: 'date', // 将 x 轴关联到 "日期" 维度
        y: 'dt_continue_count',  // 将 y 轴关联到 "利润" 维度
        tooltip: ['dt_continue_count', 'dt_continue_stock']
      }
    },
    {
      name: '连续涨停数',
      type: 'line',
      encode: {
        x: 'date', // 将 x 轴关联到 "日期" 维度
        y: 'zt_continue_count'  // 将 y 轴关联到 "利润" 维度
      }
    },
  ],
  grid: {
    left: '10%',
    right: '10%',
    bottom: '10%',
  },
});

const fetchData = async () => {
  getEmotionIndex(props.date).then(
    (resp) => {
      option.value.dataset = {
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
