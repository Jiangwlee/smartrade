<template>
  <div class="block">
    <span class="demonstration">选择日期: </span>
    <el-date-picker
      v-model="pickedDate"
      type="date"
      format="YYYY-MM-DD"
      placeholder="Pick a day"
      :disabled-date="disabledDate"
      :shortcuts="shortcuts"
      size="small"
    />

    <el-button type="primary" size="small" :onclick="fetchPredictions">连板预测</el-button>
  </div>

  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="date" label="日期" />
    <el-table-column prop="code" label="股票代码"/>
    <el-table-column prop="name" label="股票名称" />
    <el-table-column prop="pred" label="预测结果" />
    <el-table-column prop="pred_prob" label="概率" />
  </el-table>
</template>
  
<script lang="ts" setup>
  import { ref, reactive, onMounted } from 'vue';
  import { getPrediction } from '@/services/requests'
  import { type Prediction } from '@/services/types';
  import 'dayjs/locale/zh-cn'

  const pickedDate = ref('')
  const tableData = reactive<Prediction[]>([])
  
  const fetchPredictions = async () => {
    const resp = await getPrediction(formatDate(pickedDate.value));
    console.log(resp.data.data)
    tableData.length = 0;
    tableData.push(...resp.data.data)
  };

  const disabledDate = (time: Date) => {
    return time.getTime() > Date.now()
  }

  const shortcuts = [
    {
      text: '今天',
      value: new Date(),
    },
    {
      text: '昨天',
      value: () => {
        const date = new Date()
        date.setTime(date.getTime() - 3600 * 1000 * 24)
        return date
      },
    },
    {
      text: '一周前',
      value: () => {
        const date = new Date()
        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
        return date
      },
    },
  ]

  const formatDate = (value: string) => {
    console.log("Date: " + value)
    if (value) {
        const date = new Date(value);
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        return `${year}${month}${day}`;
      } else {
        return '';
      }
  }

  onMounted(() => {
    // fetchPredictions();
  });
</script>