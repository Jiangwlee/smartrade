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

          <el-button type="primary" size="small" :onclick="download">下载行情</el-button>
          <el-button type="primary" size="small" :onclick="topOfHistory">历史新高</el-button>
          <el-button type="primary" size="small" :onclick="eastmoneyRank">东财人气榜</el-button>
        </el-space>
      </el-col>
    </el-row>

    <el-row>
      <BoardReview :date="formattedDate" />
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <EmotionReview :date="formattedDate" />
        <!-- <TrendChart :source="limitUpDownTrend" /> -->
      </el-col>
      <el-col :span="12">
        <div>
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
                  <el-tag
                    type="primary"
                    v-for="item in scope.row.stocks"
                    :class="stockCodeStyle(item.code)"
                  >
                    <div style="display: flex; align-items: center">
                      <a :href="getEastmoneyLink(item.code)" target="_blank">{{
                        item.name
                      }}</a>
                    </div>
                  </el-tag>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <el-divider class="card-divider"/>

        <el-row :gutter="6">
          <el-col :span="12">
            <el-card>
              <template #header>
                <div class="card-title">
                  <span>昨日首板断板</span>
                </div>
              </template>
              <ul v-if="breakLossStats.length > 0" class="card-list">
                <li>平均涨幅：{{ (breakLossStats[0].first_limitup_loss.chg * 100).toFixed(2) }}%</li>
                <li>断板家数：{{ breakLossStats[0].first_limitup_loss.count }}</li>
                <li>断板上涨：{{ breakLossStats[0].first_limitup_loss.up }}</li>
                <li>断板下跌：{{ breakLossStats[0].first_limitup_loss.down }}</li>
                <li>最大涨幅：{{ (breakLossStats[0].first_limitup_loss.max * 100).toFixed(2) }}%</li>
                <li>最大跌幅：{{ (breakLossStats[0].first_limitup_loss.min * 100).toFixed(2) }}%</li>
              </ul>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card>
              <template #header>
                <div class="card-title">
                  <span>昨日连板断板</span>
                </div>
              </template>
              <ul v-if="breakLossStats.length > 0" class="card-list">
                <li>平均涨幅：{{ (breakLossStats[0].continue_limitup_loss.chg * 100).toFixed(2)}}%</li>
                <li>断板家数：{{ breakLossStats[0].continue_limitup_loss.count }}</li>
                <li>断板上涨：{{ breakLossStats[0].continue_limitup_loss.up }}</li>
                <li>断板下跌：{{ breakLossStats[0].continue_limitup_loss.down }}</li>
                <li>最大涨幅：{{ (breakLossStats[0].continue_limitup_loss.max * 100).toFixed(2) }}%</li>
                <li>最大跌幅：{{ (breakLossStats[0].continue_limitup_loss.min * 100).toFixed(2) }}%</li>
              </ul>
            </el-card>
          </el-col>
        </el-row>
        <el-divider class="card-divider"/>

        <el-card>
          <template #header>
            <div class="card-title">
              <span>今日反包个股</span>
            </div>
          </template>
          <div class="flex-gap">
            <el-tag
              type="primary"
              v-for="item in reversalPatternStocks"
              :class="stockCodeStyle(item.toString())"
            >
              <div style="display: flex; align-items: center">
                <a :href="getEastmoneyLink(item[0])" target="_blank">{{
                  item[1]
                }}</a>
              </div>
            </el-tag>
          </div>
        </el-card>
        <el-divider class="card-divider"/>
        <el-card>
          <template #header>
            <div class="card-title">
              <span>今日断板个股（二连板以上断板）</span>
            </div>
          </template>
          <div class="flex-gap">
            <el-tag
              type="primary"
              v-for="item in breakPatternStocks"
              :class="stockCodeStyle(item.toString())"
            >
              <div style="display: flex; align-items: center">
                <a :href="getEastmoneyLink(item[0])" target="_blank">{{
                  item[1]
                }}</a>
              </div>
            </el-tag>
          </div>
        </el-card>
        <el-divider class="card-divider"/>
        <TopStocks :date="formattedDate" />
        <el-divider class="card-divider"/>
        <LonghuStats :date="formattedDate" />
      </el-col>
    </el-row>

    <el-row :gutter="20">
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import { type BreakLossDataItem, type LimitUpLadder } from '@/services/types'
import {
  downloadOneDay,
  getLimitUpLadder,
  getLimitUpDownTrend,
  getReversalStocks,
  getBreakStocks,
  getBreakLossStats
} from '@/services/requests'
import EmotionReview from './EmotionReview.vue'
import BoardReview from './BoardReview.vue'
import LonghuStats from './LonghuStats.vue'
import TopStocks from './TopStocks.vue'
import 'dayjs/locale/zh-cn'
import { getEastmoneyLink } from '@/utils/stocks'

interface ReviewData {
  ladder: LimitUpLadder[]
}

const pickedDate = ref(new Date().toISOString())
const formattedDate = computed(() => formatDate(pickedDate.value))
const reviewData = ref<ReviewData>({
  ladder: [],
})
const limitUpDownTrend = ref<Array<Array<string | number>>>([])
const reversalPatternStocks = ref<Array<Array<string>>>([])
const breakPatternStocks = ref<Array<Array<string>>>([])
const breakLossStats = ref<BreakLossDataItem[]>([])

const fetchBreakLossStats = async () => {
  getBreakLossStats(formattedDate.value).then(
    (resp) => { 
      breakLossStats.value = resp.data.data
    }
  )
}

const getReversalPatternStocks = async () => {
  getReversalStocks(formattedDate.value).then(
    (resp) => reversalPatternStocks.value = resp.data.data,
  )
}

const getBreakPatternStocks = async () => {
  getBreakStocks(formattedDate.value).then(
    (resp) => breakPatternStocks.value = resp.data.data,
  )
}

const stockCodeStyle = (code: string) => {
  return code.startsWith("3") ? "stock-tag-3" : "stock-tag";
}

const review = async () => {
  getLimitUpLadder(formatDate(pickedDate.value)).then(
    (resp) => (reviewData.value.ladder = resp.data.data),
  )
}

const fetchLimitUpDownTrend = async () => {
  getLimitUpDownTrend(formatDate(pickedDate.value)).then((resp) => {
    limitUpDownTrend.value = resp.data.data
  })
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

const topOfHistory = () => {
  const targetUrl = 'http://data.10jqka.com.cn/rank/cxg/###';
  window.open(targetUrl, "_blank");
}

const eastmoneyRank = () => {
  const targetUrl = 'https://guba.eastmoney.com/rank/';
  window.open(targetUrl, "_blank");
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
    review()
    fetchLimitUpDownTrend()
    fetchBreakLossStats()
  }
})

onMounted(() => {
  review()
  fetchLimitUpDownTrend()
  getReversalPatternStocks()
  getBreakPatternStocks()
  fetchBreakLossStats()
})
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

.stock-tag {
  font-size: small;
  width: 80px;
  background-color: white;
  color: gray;
  border-color: coral;
}

.stock-tag-3 {
  font-size: small;
  width: 80px;
  background-color: #ec7063;
  color: white;
  border-color: coral;
}

.board-card {
    width: 15.5%;
    margin: 0.5%;
    color: gray
}

.card-title {
    font-weight: bold;
    color: gray
}

.card-list {
    text-align: left;
}

.card-divider {
  // margin-top: 1px;
  margin-bottom: 0px;
}
</style>
