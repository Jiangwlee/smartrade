<template>
  <div class="common-layout">
    <el-container>
      <el-header class="smartrade-header">
        <el-row>
          <el-col :span="24">
            <h1>Smartrade</h1>
          </el-col>
          <el-col :span="24">
            <el-menu mode="horizontal" :router="true" :ellipsis="true">
              <el-menu-item index="/home">Go to Home</el-menu-item>
              <el-menu-item index="/prediction">连板预测</el-menu-item>
              <el-menu-item index="/evaluation">模型评估</el-menu-item>
            </el-menu>
          </el-col>
        </el-row>
      </el-header>

      <el-container>
        <!-- <el-aside width="200px">
            侧边栏
        </el-aside> -->
        <el-main>
          <RouterView />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<style lang="scss" scoped>
.smartrade-header {
  height: 100px;
}

.el-menu {
  height: 20px;
  background-color: #303133;
  --el-menu-text-color: white;
}
</style>
