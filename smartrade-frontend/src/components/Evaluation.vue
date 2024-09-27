<template>
  <div class="prediction">
    <el-row>
      <el-col :span="4">
        <el-space style="width: 100%">
          <el-date-picker v-model="pickedDate" type="date" format="YYYY-MM-DD" placeholder="Pick a day"
            :disabled-date="disabledDate" :shortcuts="shortcuts" size="small" />
          <el-button type="primary" size="small" :onclick="fetchEvaluations">连板预测</el-button>
          <el-button type="primary" size="small" :onclick="download">下载行情</el-button>
        </el-space>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12" justify="space-between">
        <el-table :data="evaluationData.tableData" style="width: 100%" v-loading="isLoading"
          element-loading-text="数据加载中..." :element-loading-spinner="svg" element-loading-svg-view-box="-10, -10, 50, 50"
          :row-class-name="tableRowClassName" @row-click="showDetail">
          <el-table-column prop="date" label="涨停日期" width="90" />
          <el-table-column prop="rank" label="人气" sortable width="80" />
          <el-table-column prop="code" label="股票代码" >
            <template #default="scope">
              <div style="display: flex; align-items: center">
                <a :href="getEastmoneyLink(scope.row.code)" target="_blank">{{ scope.row.code }}</a>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="股票名称" />
          <el-table-column prop="limit_up_type" label="涨停类型" />
          <el-table-column prop="high_days" label="涨停天数" />
          <el-table-column prop="pred" label="预测结果" />
          <el-table-column prop="real" label="实际结果" />
          <el-table-column prop="pred_prob" label="概率" />
        </el-table>
      </el-col>
      <el-col :span="12">
        <StockInfo :details="evaluationData.details" />
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { ElNotification } from 'element-plus';
import { getEvaluation, getLimitUpDetail, getEastmoneyRank, downloadOneDay } from '@/services/requests'
import StockInfo from '@/components/StockInfo.vue'
import type { Evaluation, StockRankInfo } from '@/services/types';
import { useEvaluationStore } from '@/stores/evaluation';
import 'dayjs/locale/zh-cn'


const isLoading = ref(false)
const pickedDate = ref(new Date().toISOString())
const prevDate = computed(() => {
  const date = new Date()
  date.setDate(new Date(pickedDate.value).getDate() - 1)
  return date.toISOString()
})
const evaluationData = useEvaluationStore()

const svg = `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
        `

const fetchEvaluations = async () => {
  isLoading.value = true;
  await getLimitUpDetail(formatDate(prevDate.value)).then((resp) => {
    resp.data.data.map((item) => {
      evaluationData.limitUpDetailMap[item.code] = item;
    });
  });

  const rankMap: Record<string, StockRankInfo> = {}
  await getEastmoneyRank().then((resp) => {
    resp.data.data.forEach((value) => rankMap[value.sc.substring(2)] = value)
  });

  getEvaluation(formatDate(pickedDate.value)).then((resp) => {
    const result = resp.data.data.map((value) => ({
      date: value.date,
      code: value.code,
      name: value.name,
      pred: value.pred,
      real: value.real,
      pred_prob: value.pred_prob,
      high_days: "",
      limit_up_type: "",
      rank: 999
    }));

    result.forEach(r => {
      r.high_days = evaluationData.limitUpDetailMap[r.code].high_days;
      r.limit_up_type = evaluationData.limitUpDetailMap[r.code].limit_up_type;
      r.rank = r.code in rankMap ? rankMap[r.code].rk : 999;
    })

    evaluationData.tableData.length = 0
    evaluationData.tableData.push(...result)
    isLoading.value = false;
  })
};

const download = async () => {
  downloadOneDay(formatDate(pickedDate.value)).then((resp) => {
    ElNotification({
      title: '行情下载成功!',
      message: resp.data.msg,
      type: 'success'
    })
  }).catch((ex) => {
    ElNotification({
      title: '行情下载失败!',
      message: ex,
      type: 'error'
    })
  })
}

const showDetail = (row: Evaluation, column: any, event: Event) => {
  console.log(row.code);
  if (row.code != '') {
    evaluationData.details = evaluationData.limitUpDetailMap[row.code];
  }
}

const disabledDate = (time: Date) => {
  return time.getTime() > Date.now()
}

const tableRowClassName = ({ row, rowIndex }: { row: Evaluation, rowIndex: number }) => {
  if (row.pred == '连板') {
    return 'success-row'
  } else {
    return ''
  }
}

const getEastmoneyLink = (code: string) => {
  if (code.startsWith('6')) {
    return `https://quote.eastmoney.com/sh${code}.html`
  } else {
    return `https://quote.eastmoney.com/sz${code}.html`
  }
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
</script>

<style lang="scss" scoped>
.prediction {
  width: 100%;

  :deep(.success-row) {
    --el-table-tr-bg-color: var(--el-color-danger-light-5);
  }

  .el-row {
    margin-bottom: 20px;
  }

  .el-row:last-child {
    margin-bottom: 0;
  }

  .el-col {
    border-radius: 4px;
  }

  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }

  :deep(.description) {
    background-color: white;
    --el-text-color-primary: #606266;
  }

  :deep(.my-label) {
    font-weight: bold;
  }

  :deep(.block-label) {
    color: lightcoral;
    font-weight: bold;
  }
}
</style>