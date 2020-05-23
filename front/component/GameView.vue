游戏视图
<template>
  <div class="GameView">
    <div class="console">
      <input type="button" value="上一关(P)" @click="doPrevLevel">
      <input type="button" value="下一关(N)" @click="doNextLevel()">
      <input type="button" value="重玩本关(R)" @click="doReset()">
      <input type="button" value="自动演示(A)"
             :disabled="!(answer&&answer.length>0)" @click="doAutoPlay()">
      <input type="button" value="分享游戏(S)" @click="shareGame()">
    </div>
    <div class="body" @keydown="onKeydown" @click="focusCanvas()">
      <CanvasSokoban ref="canvas" :game="game" @over="onOver"></CanvasSokoban>
    </div>
    <div class="footer">{{game.getOpList().length}}/{{answer?answer.length:"无"}}</div>
  </div>
</template>
<script>
  import {Game} from "../js/Game.ts";
  import CanvasSokoban from "../component/CanvasSokoban";
  import {wrapUrl} from "../js/lib";

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
      answer() {
        return this.$store.state.maps[this.curLevel].answer;
      },
      canvas() {
        return this.$refs.canvas;
      }
    },
    mounted() {
      document.body.onresize = () => this.canvas.drawMap();
      this.focusCanvas();
      window.onpopstate = (event) => {
        const gameIndex = parseInt(this.$route.params.game);
        this.initGame(gameIndex, false)
      }
      const gameIndex = parseInt(this.$route.params.game);
      this.initGame(gameIndex, false);
    },
    methods: {
      onKeydown(e) {
        switch (e.key) {
          case 'a': {
            this.doAutoPlay();
            break;
          }
          case 'r': {
            this.doReset();
            break;
          }
          case 'p': {
            this.doPrevLevel();
            break;
          }
          case 'n': {
            this.doNextLevel();
            break;
          }
          case 's': {
            this.shareGame();
            break;
          }
        }
      },
      doPrevLevel() {
        this.initGame(Math.max(0, this.curLevel - 1), true);
      },
      doNextLevel() {
        this.initGame(Math.min(this.curLevel + 1, this.maps.length - 1), true)
      },
      doReset() {
        this.initGame(this.curLevel, false);
        this.canvas.stopAutoPlay();
      },
      shareGame() {
        this.copyText(location.href);
        this.$message("网址已复制到剪贴板");
        this.focusCanvas();
      },
      doAutoPlay() {
        this.game.loadXsb(this.maps[this.curLevel].question);
        this.canvas.drawMap();
        this.canvas.autoPlay(this.answer || '')
        this.focusCanvas();
      },
      onOver(qa) {
        this.$nextTick(() => {
          this.$message("恭喜胜利！")
        })
        axios.post(wrapUrl('/api/submit'), qa).then(resp => {
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
        this.canvas.$el.focus();
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
        this.canvas.stopAutoPlay();
        this.game.loadXsb(question.question);
        this.canvas.drawMap();
        this.focusCanvas();
      },
    }
  };
</script>
<style lang="less">
  .GameView {
    @console-height: 50px;
    @footer-height: 40px;
    @header-footer-height: @console-height+@footer-height;

    .console {
      height: @console-height;
      display: flex;
      width: 100%;

      & > * {
        height: 100%;
        flex: 1;
      }


      align-items: center;
      justify-content: space-between;
    }

    .body {
      display: flex;
      background: black;
      height: calc(~"100% - " @header-footer-height);
      align-items: center;
      justify-content: center;
    }

    .footer {
      height: @footer-height;
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      background: antiquewhite;
    }
  }
</style>