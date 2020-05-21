游戏视图
<template>
  <div class="GameView">
    <div class="console">
      <input type="button" value="上一关" @click="initGame(Math.max(0,curLevel-1),true)">
      <input type="button" value="下一关" @click="initGame(Math.min(curLevel+1,maps.length-1),true)">
      <input type="button" value="重玩本关" @click="initGame(curLevel,false)">
      <input type="button" value="自动演示" @click="doAutoPlay()">
      <input type="button" value="分享游戏" @click="shareGame()">
      <div class="desc">{{game.getOpList().length}}/{{answer?answer.length:"无"}}</div>
    </div>
    <div class="body">
      <CanvasSokoban ref="canvas" :game="game" @over="onOver"></CanvasSokoban>
    </div>
  </div>
</template>
<script>
  import {Game} from "../js/Game.ts";
  import CanvasSokoban from "../component/CanvasSokoban";

  const axios = require("axios");
  const GameMixin = require("../js/GameMixin.js");
  export default {
    components: {CanvasSokoban,},
    mixins: [GameMixin],
    data() {
      return {
        game: new Game(),
        curLevel: 0,
      };
    },
    computed: {
      maps() {
        return this.$store.state.maps;
      },
      answer() {
        return this.$store.state.maps[this.curLevel].answer;
      }
    },
    mounted() {
      document.body.onresize = () => this.$refs.canvas.drawMap();
      this.focusCanvas();
      window.onpopstate = (event) => {
        const gameIndex = parseInt(this.$route.params.game);
        this.initGame(gameIndex, false)
      }
      const gameIndex = parseInt(this.$route.params.game);
      this.initGame(gameIndex, false);
    },
    methods: {
      shareGame() {
        this.copyText(location.href);
        this.$message("网址已复制到剪贴板");
        this.focusCanvas();
      },
      doAutoPlay() {
        this.game.loadPsb(this.maps[this.curLevel].question);
        this.$refs.canvas.drawMap();
        this.$refs.canvas.autoPlay(this.answer || '')
        this.focusCanvas();
      },
      onOver(qa) {
        this.$nextTick(() => {
          this.$message("恭喜胜利！")
        })
        axios.get('/api/submit', {
          params: qa
        }).then(resp => {
          console.log(resp.data)
          this.$message(resp.data);
          if (qa.a.length < this.answer.length) {
            this.$store.commit("setAnswer", {
              level: this.curLevel,
              qa: qa,
            });
          }
        })
      },
      focusCanvas() {
        this.$refs.canvas.$el.focus();
      },
      initGame(mapIndex, updateHistory) {
        const title = `【推箱子】第${mapIndex}关`;
        const question = this.$store.state.maps[mapIndex];
        document.title = title;
        if (updateHistory) {
          this.$router.push({
            params: {
              game: mapIndex,
            }
          })
        }
        this.curLevel = mapIndex;
        this.game.loadPsb(question.question);
        this.$refs.canvas.drawMap();
        this.focusCanvas();
      },
    }
  };
</script>
<style lang="less">
  .GameView {
    @console-height: 50px;

    .console {
      height: @console-height;
      display: flex;

      & > * {
        height: 100%;
        flex: 1;
      }

      .desc {
        display: flex;
        align-items: center;
        justify-content: center;
      }

      align-items: center;
      justify-content: space-between;
    }

    .body {
      display: flex;
      background: black;
      height: calc(~"100% - " @console-height);
      align-items: center;
      justify-content: center;
    }
  }
</style>