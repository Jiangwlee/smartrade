<template>
  <div class="common-layout">
    <el-container>
      <el-header>Header</el-header>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </div>
</template>

<script>
    import { RouterView } from 'vue-router';
    export default {
        name: 'Layout'
    };
</script>
