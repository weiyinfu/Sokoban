添加问题页面
<template>
  <div class="AddProblem">
    <header-part active-tab="贡献问题"></header-part>
    <div class="body">
      <div class="left">
        <canvas-sokoban ref="canvas" :game="game" tabindex="-1"
                        style="outline: none;"></canvas-sokoban>
      </div>
      <div class="right">

        <button @click="regularize">规范化地图</button>
        <button @click="searchQuestion">查询问题</button>
        <button @click="submitQuestion">提交问题</button>
        <textarea
                class="input-map"
                @change="inputChange"
                @keydown="inputKeydown"
                placeholder="请输入地图字符串，使用Ctrl+S进行渲染"
                v-model="mapString">
        </textarea>
        <div v-if="searchResult">{{searchResult.answer}}</div>
        <div class="remind">
          <p>- 空白</p>
          <p>. 插槽</p>
          <p>@ 人</p>
          <p>+ 人在插槽处</p>
          <p>$ 箱子</p>
          <p>* 箱子在插槽处</p>
          <p># 墙</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import HeaderPart from "./HeaderPart";
  import CanvasSokoban from "./CanvasSokoban";
  import {Game} from "../js/Game";
  import {wrapUrl} from "../js/lib";

  const axios = require("axios");
  export default {
    components: {
      HeaderPart, CanvasSokoban
    },
    data() {
      const game = new Game();
      return {
        game,
        mapString: "",
        searchResult: null,
      }
    },
    computed: {
      canvas() {
        return this.$refs.canvas;
      },
    },
    mounted() {
      window.onresize = () => {
        console.log("haha")
        this.canvas.drawMap();
      }
    },
    activated() {
      document.title = `推箱子-贡献问题`
    },
    methods: {
      submitQuestion() {
        //提交问题
        axios.get(wrapUrl("/api/add_question"), {
          params: {
            map: this.mapString,
          }
        }).then(resp => {
          this.$message(resp.data);
        })
      },
      searchQuestion() {
        axios.get(wrapUrl("/api/search_question"), {
          params: {
            map: this.mapString,
          }
        }).then(resp => {
          this.searchResult = resp.data;
          if (!this.searchResult) {
            this.$message("没有此问题，可以提交")
          }
        })
      },
      regularize() {
        axios.get(wrapUrl("/api/regularize_map"), {
          params: {
            map: this.mapString,
          }
        }).then(resp => {
          this.mapString = resp.data;
          this.inputChange();
        })
      },
      inputChange() {
        this.game.loadXsb(this.mapString);
        this.canvas.drawMap();
      },
      inputKeydown(event) {
        if (event.ctrlKey && event.key === 's') {
          this.inputChange();
          event.stopPropagation();
          event.preventDefault();
        }
      }
    }
  }
</script>
<style lang="less">
  .AddProblem {
    html, body {
      width: 100%;
      height: 100%;
      padding: 0;
      margin: 0;
    }

    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
    @header-height: 44px;

    .HeaderPart {
      height: @header-height;
    }

    .body {
      display: flex;
      height: calc(~"100% - " @header-height);
      overflow: hidden;

      .input-map {
        font-size: 25px;
        width: 100%;
        height: 280px;
        outline: none;
      }

      .left, .right {
        width: 50%;
        height: 100%;
      }

      .left {
        display: flex;
        align-items: center;
        justify-content: center;
        background: black;
        color: white;
      }

      .right {
        overflow: auto;

        .remind {
          color: grey;

          p {
            margin: 0;
          }
        }
      }
    }
  }
</style>