<template>
  <div class="review">
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

          <el-button type="primary" size="small" :onclick="download"
            >下载行情</el-button
          >
        </el-space>
      </el-col>
    </el-row>

    <el-row>标题栏</el-row>
    <el-row>最强板块</el-row>
    <el-row :gutter="20">
      <el-col :span="12" justify="start">
        <el-table
          :data="reviewData.ladder"
          style="width: 100%"
          header-row-class-name="review-header"
        >
          <el-table-column
            prop="height"
            label="连板高度"
            class-name="height-col"
            width="80"
          >
            <template #default="scope">
              <el-badge :value="scope.row.stocks.length" class="badge-item">
                <el-button size="small">{{ scope.row.height }}</el-button>
              </el-badge>
            </template>
          </el-table-column>
          <el-table-column
            prop="stocks"
            label="连板股票"
            class-name="stock-col"
          >
            <template #default="scope">
              <div class="flex-gap">
                <el-tag type="primary" v-for="item in scope.row.stocks">{{
                  item
                }}</el-tag>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="12" justify="start">
        <!-- <ContinuousLimitUpChart /> -->
        <LineChart :date="formattedDate" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import type { LimitUpLadder } from '@/services/types'
import { downloadOneDay, getLimitUpLadder } from '@/services/requests'
import ContinuousLimitUpChart from '@/components/chats/ContinuousLimitUpChart.vue'
import LineChart from './chats/LineChart.vue'
import 'dayjs/locale/zh-cn'

interface ReviewData {
  ladder: LimitUpLadder[]
}

const pickedDate = ref(new Date().toISOString())
const formattedDate = computed(() => formatDate(pickedDate.value))
const reviewData = ref<ReviewData>({
  ladder: [],
})

const review = async () => {
  getLimitUpLadder(formatDate(pickedDate.value)).then(
    (resp) => (reviewData.value.ladder = resp.data.data),
  )
}

const download = async () => {
  downloadOneDay(formatDate(pickedDate.value))
    .then((resp) => {
      ElNotification({
        title: '行情下载成功!',
        message: resp.data.msg,
        type: 'success',
      })
    })
    .catch((ex) => {
      ElNotification({
        title: '行情下载失败!',
        message: ex,
        type: 'error',
      })
    })
}

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
  console.log('Date: ' + value)
  if (value) {
    const date = new Date(value)
    const year = date.getFullYear()
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    return `${year}${month}${day}`
  } else {
    return ''
  }
}

watch(pickedDate, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    review();
  }
})

onMounted(() => review())
</script>

<style lang="scss" scoped>
.review {
  width: 100%;

  :deep(.review-header .cell) {
    font-weight: bold;
    text-align: center;
  }

  :deep(.height-col .cell) {
    text-align: center;
  }

  :deep(.height-col .badge-item) {
    margin-top: 10px;
    margin-right: 40px;
  }

  :deep(.height-col .badge-item .el-button) {
    width: 30px;
  }
}

.flex-gap {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
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
</style>
