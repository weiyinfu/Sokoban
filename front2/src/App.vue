<template>
  <div class="Index"
       v-loading="!$store.state.gameDataLoaded"
       element-loading-spinner="el-icon-loading"
       element-loading-text="正在加载游戏数据">
    <keep-alive v-if="$store.state.gameDataLoaded">
      <router-view></router-view>
    </keep-alive>
  </div>
</template>
<script>

export default {
  mounted() {
    this.$store.dispatch("init");
  },
}
</script>
<style lang="less">
html, body, #app {
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
}

.Index {
  width: 100%;
  height: 100%;
}
</style>
