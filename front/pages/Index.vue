<template>
  <div class="Index" v-loading="!$store.state.gameDataLoaded"
       element-loading-spinner="el-icon-loading"
       element-loading-text="正在加载游戏数据">
    <keep-alive v-if="$store.state.gameDataLoaded">
      <router-view></router-view>
    </keep-alive>
  </div>
</template>
<script>
  import GameView from "../component/GameView";
  import ProblemSet from "../component/ProblemSet";
  import VueRouter from "vue-router";
  import AddProblem from "../component/AddProblem";
  import About from "../component/About";

  export default {
    mounted() {
      this.$store.dispatch("init");
    },
    router: new VueRouter({
      routes: [
        {path: "/game/:game", component: GameView},
        {path: "/", component: ProblemSet},
        {path: "/add", component: AddProblem},
        {path: "/about", component: About}
      ]
    })
  }
</script>
<style lang="less">
  html, body {
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
