<template>
  <div class="Index">
    <div class="header">
      <router-link to="/"><img src="https://weiyinfu.cn/learnSvg?text=推&background=white&color=purple"></router-link>
      <router-link to="/">题库</router-link>
      <router-link to="/game">游戏</router-link>
    </div>
    <div class="main">
      <router-view></router-view>
    </div>
  </div>
</template>
<script>
  import GameView from "../component/GameView";
  import MapView from "../component/MapView";
  import VueRouter from "vue-router";

  export default {
    components: {
      GameView, MapView
    },
    data() {
      return {}
    },
    router: new VueRouter({
      routes: [
        {path: "/game", component: GameView},
        {path: "/", component: MapView},
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
    @header-height: 44px;

    .header {
      height: @header-height;
      display: flex;
      align-items: center;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
      color: rgba(0, 0, 0, 0.65);

      img {
        max-height: 100%;
      }

      a {
        text-decoration: none;
        cursor: pointer;
        color: rgba(0, 0, 0, 0.65);
        height: 100%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        margin:0 10px;
        font-size: 14px;
      }
    }
  }
</style>
