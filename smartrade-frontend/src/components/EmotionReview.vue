<template>
  <div class="emotion-board">
    <div class="header">
        市场情绪
    </div>
    <div class="body">
      <el-tooltip v-for="item in dtbStocks" :content="item" placement="top">
        <el-button :key="item" class="good">地<br/>天</el-button>
      </el-tooltip>
      <el-tooltip v-for="item in tdbStocks" :content="item" placement="top">
        <el-button :key="item" class="danger">天<br/>地</el-button>
      </el-tooltip>
      <el-button v-for="n in Math.ceil(dailyInfo['dt_count'] / 5)" :key="n" :icon="Download" circle class="warning" />
    </div>
    <el-divider />
    <div class="chart-wrapper">
        <TrendChart :date="props.date" />
    </div>
    <div class="chart-wrapper">
        <LineChart :date="props.date" />
    </div>
    <div class="chart-wrapper">
        <EmotionIndexChart :date="props.date" />
    </div>
    <div class="chart-wrapper">
        <ZdtTrendChart :date="props.date" />
    </div>
    <div class="chart-wrapper">
        <EmotionTrendChart :date="props.date" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, computed, onMounted, onUpdated } from 'vue';
import EmotionIndexChart from './charts/EmotionIndexChart.vue';
import TrendChart from './charts/TrendChart.vue';
import ZdtTrendChart from './charts/ZdtTrendChart.vue';
import EmotionTrendChart from './charts/EmotionTrendChart.vue';
import LineChart from './charts/LineChart.vue';
import { type EmotionInfo } from '@/services/types';
import { getEmotionOverview } from '@/services/requests';
import {
  Download,
  WarningFilled,
  Bell,
  Bottom
} from '@element-plus/icons-vue'

const props = defineProps<{
  date: string
}>()

const dailyInfo = ref<EmotionInfo>({
  "date": "",
  "tdb_count": 0,
  "tdb_stock": "",
  "height": 0,
  "height_stock": "",
  "dt_count": 0,
  "dt_continue_count": 0,
  "dt_continue_stock": "",
  "zt_continue_count": 0,
  "dtb_count": 0,
  "dtb_stock": "",
})

const dtbStocks = computed(() => {
  if (dailyInfo.value['dtb_count'] == 0) {
    return []
  }
  return dailyInfo.value['dtb_stock'].split(",");
})

const tdbStocks = computed(() => {
  if (dailyInfo.value['tdb_count'] == 0) {
    return []
  }
  return dailyInfo.value['tdb_stock'].split(",");
})

const fetchData = async () => {
  getEmotionOverview(props.date).then(
    (resp) => {
      dailyInfo.value = resp.data.data
    }
  )
}

onMounted(() => {
  console.log("EmotionTrendChart is mounted")
  fetchData()
})

// onUpdated(() => {
//   console.log("EmotionTrendChart is updated")
//   fetchData()
// })

</script>

<style scoped>
.emotion-board {
    background-color: white;
    padding-top: 20px;

    .header {
        font-weight: bold;
        font-size: large;
    }

    .body {
        margin: 20px
    }

    .chart-wrapper {
        margin: 10px;
    }
}

.good {
    background-color:  #ff4d00;
    color: white;
    font-weight: bold;
}

.danger {
    background-color:  #0ef082;
    color: gray;
    font-weight: bold;
}

.warning {
    background-color: gold;
}

</style>