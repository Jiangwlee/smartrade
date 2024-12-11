<template>
  <v-chart class="chart" :option="option" autoresize />
</template>

<script lang="ts" setup>
import { ref, provide, onMounted, onUpdated } from 'vue'
import VChart, { THEME_KEY } from 'vue-echarts'
import { getLeadingStocks } from '@/services/requests'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { DatasetComponent, GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { ComposeOption } from 'echarts/core'
import type { LineSeriesOption } from 'echarts/charts'
import type {
  DatasetComponentOption,
  GridComponentOption
} from 'echarts/components'
import type { TooltipComponentOption } from 'echarts'

use([DatasetComponent, GridComponent, TooltipComponent, LineChart, CanvasRenderer])

type EChartsOption = ComposeOption<
  | DatasetComponentOption
  | GridComponentOption
  | LineSeriesOption
  | TooltipComponentOption
>


provide(THEME_KEY, 'dark')

const props = defineProps<{
  date: string
}>()

const option = ref<EChartsOption>({
  dataset: {
    dimensions: ['date', 'continuous_num', 'stocks'],
    source: [
      {'date': '', 'continuous_num': '0', 'stocks': ''},
    ]
  },
  tooltip: {
    trigger: 'axis',
    formatter: (params: any) => {
      const data = params[0]?.data;
      const date = data?.date;
      const continuousNum = data?.continuous_num;
      const stocks = data?.stocks;

      return `${date}<br/>-------------<br/>
              连板高度: ${continuousNum}<br/>
              涨停股: ${stocks}`;
    }
  },
  xAxis: {
    type: 'category',
    name: '日期',
    nameLocation: 'end',
  },
  yAxis: {
    type: 'value',
    name: '连板高度'
  },
  series: [
    { type: 'line' },  // 第一个数据列绘制为折线
  ]
})

const fetchData = async () => {
  getLeadingStocks(props.date).then(
    (resp) => {
      option.value.dataset = {
        dimensions: ['date', 'continuous_num', 'stocks'],
        source: resp.data.data
      }
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
