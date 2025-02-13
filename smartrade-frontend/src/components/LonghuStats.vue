<template>
  <div class="cards-container">
    <el-card
      v-for="(item, index) in longhuInfo.items"
      :key="index"
      class="user-card"
      shadow="hover"
    >
      <div slot="header" class="card-header">
        {{ item.name }}
      </div>
      <div class="card-content">
        <ul>
            <li style="font-weight: bold; color: orange;">净买入金额: {{ item.netvalue.toFixed(2) }}万</li>
            <li v-for="stock in item.stocks">
                <p style="font-weight: bold; color: orange;">{{ stock.stockName }}</p>
                <ul>
                    <li><span>买入: </span>{{ formatAmount(stock.bvalue) }}万</li>
                    <li><span>卖出: </span>{{ formatAmount(stock.svalue) }}万</li>
                    <li><span>净买: </span>{{ formatAmount(stock.netvalue) }}万</li>
                </ul>
            </li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import type { LonghuInfo } from '@/services/types';
import { getLonghuStats } from '@/services/requests'
import {ref, defineProps, watch, onMounted} from 'vue';

const props = defineProps<{
    date: string
}>()

const longhuInfo = ref<LonghuInfo>({
    'date': '',
    'items': []
})

const fetchData = async () => {
    getLonghuStats(props.date).then(
        (resp) => {
            console.log(resp.data.data)
            longhuInfo.value = resp.data.data
            console.log(longhuInfo.value)
        }
    )
}

const formatPercent = (value: number) => {
      return (value * 100).toFixed(2) + "%";
    }

const formatAmount = (value: number) => {
    return value.toFixed(2);
}

watch(props, (newVal, oldValue) => {
    fetchData()
})

onMounted(() => {
    fetchData()
})
</script>

<style scoped>
.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: flex-start;
}

.user-card {
  width: 240px; /* 卡片宽度 */
}

.card-header {
  font-size: 16px;
  font-weight: bold;
  text-align: center; /* 标题左对齐 */
  margin: 10px;
}

.card-content {
  text-align: left; /* 卡片内容左对齐 */
  font-size: 14px;
}

.card-content ul {
  padding-left: 20px; /* 为列表添加左缩进 */
  margin: 0;
}

.card-content ul li {
  margin-bottom: 8px; /* 列表项之间添加间距 */
  color: gray;
}

.card-content ul li ul {
  padding-left: 20px; /* 嵌套列表添加额外缩进 */
  margin-top: 5px; /* 嵌套列表与上方间距 */
}
</style>