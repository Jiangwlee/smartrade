<template>
  <el-table
    :data="currentPageData"
    style="width: 100%"
    element-loading-text="数据加载中..."
    :element-loading-spinner="loadingIcon"
    element-loading-svg-view-box="-10, -10, 50, 50"
    :default-sort="{ prop: 'pred_prob', order: 'descending' }"
    size="small"
    class="top-stock-table"
  >
    <el-table-column prop="code" label="股票代码">
      <template #default="scope">
        <div style="align-items: center">
          <a :href="getEastmoneyLink(scope.row.code)" target="_blank">{{
            scope.row.code
          }}</a>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="name" label="股票名称" />
    <el-table-column prop="count" label="涨停次数" />
    <el-table-column prop="high" label="高度" />
    <el-table-column prop="first" label="首次涨停" />
    <el-table-column prop="last" label="最近涨停" />
    <el-table-column prop="duration" label="涨停周期" />
  </el-table>
  <el-pagination
    size="small"
    layout="total,prev,pager,next,jumper"
    :total="tableData?.length || 0"
    v-model:page-size="pageSize"
    v-model:current-page="currentPage"
    @current-change="handleCurrentChange"
  ></el-pagination>
</template>

<script setup lang="ts">
import { ref, defineProps, watch, onMounted, computed } from 'vue'
import type { TopStock } from '@/services/types'
import { getTopStocks } from '@/services/requests'
import { loadingIcon } from './icons/icons'
import { getEastmoneyLink } from '@/utils/stocks'

const props = defineProps<{
  date: string
}>()

const tableData = ref<TopStock[]>()
const pageSize = ref(10)
const currentPage = ref(1)
const currentPageData = computed(() =>
  tableData.value?.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value,
  ),
)

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

const fetchData = async () => {
  getTopStocks(props.date).then((resp) => (tableData.value = resp.data.data))
}

watch(props, (oldVal, newValue) => {
  fetchData()
})

onMounted(() => {
  fetchData()
})
</script>

<style lang="scss" scoped>
.top-stock-table {
  :deep(.cell) {
    text-align: center;
  }
}
</style>
