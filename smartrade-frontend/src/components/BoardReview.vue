<template>
  <el-card v-for="(card, index) in blockData" :key="card.name" :class=cardClass(index)>
    <template #header>
      <div class="card-title">
        <span>{{ card.name }}</span>
      </div>
    </template>
    <ul class="card-list">
        <li>涨停家数: {{ card.limit_up_num }}</li>
        <li>板块涨幅: {{ card.change_rate }}%</li>
        <li>入选天数: {{ card.continuous_plate_num }}</li>
        <li>最高连板: {{ card.high }}</li>
    </ul>
    <template #footer>
        <div class="card-footer">
            <span class="card-title">板块领涨</span>
            <ul class="card-list">
                <li><span class="stock-title">{{ card.top0.split(':')[0] }}</span>: <span>{{ card.top0.split(':')[1] }}</span></li>
                <li><span class="stock-title">{{ card.top1?.split(':')[0] }}</span>: <span>{{ card.top1?.split(':')[1] }}</span></li>
                <li><span class="stock-title">{{ card.top2?.split(':')[0] }}</span>: <span>{{ card.top2?.split(':')[1] }}</span></li>
            </ul>
        </div>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import type { BoardDetails } from '@/services/types';
import { getLeadingBlocks } from '@/services/requests'
import {ref, defineProps, watch, onMounted} from 'vue';

const props = defineProps<{
    date: string
}>()
const blockData = ref<BoardDetails[]>([])

const fetchData = async () => {
    getLeadingBlocks(props.date).then(
        (resp) => blockData.value = resp.data.data
    )
}

const cardClass = (index: number) => "board-card card-" + index

watch(props, (newVal, oldValue) => {
    fetchData()
})

onMounted(() => {
    fetchData()
})
</script>

<style scoped lang="scss">
.board-card {
    width: 15.5%;
    margin: 0.5%;
    color: gray
}

.card-title {
    font-weight: bold;
}

.card-list {
    text-align: left;
}

.stock-title {
    display: inline-block;
    width: 65px;
}

.card-0 {
    background-color: #ec7063;
    color: white;
}

.card-1 {
    background-color: #f5b041;
    color: white;
}

.card-2 {
    background-color: #c39bd3;
    color: white;
}
</style>