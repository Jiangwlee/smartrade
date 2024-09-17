<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="date" label="日期" />
    <el-table-column prop="code" label="股票代码"/>
    <el-table-column prop="name" label="股票名称" />
    <el-table-column prop="pred" label="预测结果" />
    <el-table-column prop="pred_prob" label="概率" />
  </el-table>
</template>
  
<script lang="ts" setup>
  import { reactive, onMounted } from 'vue';
  import { getPrediction } from '../services/requests'
  import { type Prediction } from '@/services/types';

  const tableData = reactive<Prediction[]>([])
  
  const fetchPredictions = async () => {
    const resp = await getPrediction('20240913');
    console.log(resp.data.data)
    tableData.length = 0;
    tableData.push(...resp.data.data)
  };

  onMounted(() => {
    fetchPredictions();
  });
</script>