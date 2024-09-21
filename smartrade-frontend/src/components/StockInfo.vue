<template>
    <div>
        <el-descriptions :title="props.details?.name" class="description">
          <el-descriptions-item label-class-name="my-label" label="股票名称" key="name">{{ props.details?.name }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="股票代码" key="code">{{ props.details?.code }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="涨停日期" key="date">{{ props.details?.date }}</el-descriptions-item>

          <el-descriptions-item label-class-name="my-label" label="涨停类型" key="limit_up_type">{{ props.details?.limit_up_type }}</el-descriptions-item>
          <el-descriptions-item label-class-name="my-label" label="涨停天数" key="high_days">{{ props.details?.high_days }}</el-descriptions-item>
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
    </div>
</template>

<script lang="ts" setup>
import { type LimitUpDetail } from '@/services/types'
import { formatTime } from '@/utils/timeutils'

const props = defineProps<{
    details?: LimitUpDetail
}>();

const getTime = (timestr: string) => formatTime(timestr);
</script>

<style lang="scss" scoped>
    
</style>