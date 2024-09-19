<template>
  <div class="prediction">
    <el-row>
      <el-col :span="4">
        <el-space style="width: 100%">
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
          <el-button type="primary" size="small" :onclick="download">下载行情</el-button>
        </el-space>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12" justify="space-between">
        <el-table :data="tableData" style="width: 100%" :row-class-name="tableRowClassName" @row-click="showDetail">
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="code" label="股票代码">
            <template #default="scope">
              <div style="display: flex; align-items: center">
                <a :href="getEastmoneyLink(scope.row.code)" target="_blank">{{ scope.row.code }}</a>
              </div>
          </template>
          </el-table-column>
          <el-table-column prop="name" label="股票名称" />
          <el-table-column prop="pred" label="预测结果" />
          <el-table-column prop="pred_prob" label="概率" />
        </el-table>
      </el-col>
      <el-col :span="12">
        <el-descriptions :title="details?.name" class="description">
          <el-descriptions-item label-class-name="my-label" label="股票名称" key="name">{{ details?.name }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="股票代码" key="code">{{ details?.code }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="涨停日期" key="date">{{ details?.date }}</el-descriptions-item>

          <el-descriptions-item label-class-name="my-label" label="涨停类型" key="limit_up_type">{{ details?.limit_up_type }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="涨停天数" key="high_days">{{ details?.high_days }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="涨停原因" key="reason_type">{{ details?.reason_type }}</el-descriptions-item>

          <el-descriptions-item label-class-name="my-label" label="首次涨停" key="first_limit_up">{{ getTime(details?.first_limit_up_time ? details?.first_limit_up_time : "") }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="最终涨停" key="last_limit_up">{{ getTime(details?.last_limit_up_time ? details?.last_limit_up_time : "") }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="打开次数" key="open_num">{{ details?.open_num }}</el-descriptions-item>

          <el-descriptions-item label-class-name="my-label" label="流通市值" key="currency">{{ details?.currency_value.toLocaleString() }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="封单数量" key="order_volume">{{ details?.order_volume.toLocaleString() }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="封单金额" key="order_volume">{{ details?.order_amount.toLocaleString() }}</el-descriptions-item>

          <el-descriptions-item label-class-name="my-label" label="涨停分析" key="reason_info">{{ details?.reason_info }}</el-descriptions-item>
        </el-descriptions>

        <p></p>

        <el-descriptions title="关联板块" v-if="details?.blocks" class="description">
          <el-descriptions-item v-for="item in details.blocks" :key="item.code" :label="item.name" label-class-name="block-label">
            <ul>
              <li>板块排名: {{ item.rank_position }}</li>
              <li>板块涨幅: {{ item.change_rate }}%</li>
              <li>涨停家数: {{ item.limit_up_num }}</li>
              <li>最多涨停: {{ item.high }}</li>
            </ul>
          </el-descriptions-item>
        </el-descriptions>
      </el-col>
    </el-row>
  </div>
</template>
  
<script lang="ts" setup>
  import { ref, onMounted, computed } from 'vue';
  import { ElNotification } from 'element-plus';
  import { getLimitUpDetail, getPrediction, downloadOneDay } from '@/services/requests'
  import type { Prediction, LimitUpDetail } from '@/services/types';
  import 'dayjs/locale/zh-cn'

  const pickedDate = ref('')
  const prevDate = computed(() => {
    const date = new Date()
    date.setDate(new Date(pickedDate.value).getDate() - 1)
    return date.toISOString()
  })
  const tableData = ref<Prediction[]>([])
  const limitUpDetail = ref<{[key: string]: LimitUpDetail}>({})
  const details = ref<LimitUpDetail>()
  const stockInfo = computed(() => {
    if (details && details.value) {
      const {block_ids, blocks, ...rest} = details.value;
      return rest;
    }
  })

  const fetchPredictions = async () => {
    getLimitUpDetail(formatDate(prevDate.value)).then((resp) => {
      resp.data.data.map((item) => {
        limitUpDetail.value[item.code] = item;
      });
    });

    getPrediction(formatDate(pickedDate.value)).then((resp) => {
      tableData.value.length = 0;
      tableData.value.push(...resp.data.data)
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

  const showDetail = (row: Prediction, column: any, event: Event) => {
    console.log(row.code);
    if (row.code != '') {
      details.value = limitUpDetail.value[row.code];
      console.log(details.value);
    }
  }

  const disabledDate = (time: Date) => {
    return time.getTime() > Date.now()
  }

  const tableRowClassName = ({row, rowIndex}: {row: Prediction, rowIndex: number}) => {
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

  const getTime = (time: string) => {
    if (time === "") {
      return ""
    } else {
      let datetime = new Date(time);
      const hour = datetime.getHours().toString().padStart(2, '0')
      const minutes = datetime.getMinutes().toString().padStart(2, '0')
      const seconds = datetime.getSeconds().toString().padStart(2, '0')
      return `${hour}:${minutes}:${seconds}`;
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

  onMounted(() => {
    // fetchPredictions();
  });
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