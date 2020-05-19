<template>
  <div class="GameView">
    <div class="console">
      <select onchange="Skin.changeSkin()" id="skin">
      </select>
      <input type="button" value="上一关" @click="initGame(Math.max(0,curLevel-1),true)">
      <input type="button" value="下一关" @click="initGame(Math.min(curLevel+1,maps.length-1),true)">
      <input type="button" value="重玩本关" @click="initGame(curLevel,false)">
      <div>已移动{{game.getOpList().length}}步，目前记录{{(maps&&maps[curLevel]&&maps[curLevel].answer.length)||'未知'}}步</div>
    </div>
    <div class="body" @keydown="onKeydown" tabindex="-1">
      <CanvasSokoban ref="canvas" :game="game" :Skin="Skin" :index="index"></CanvasSokoban>
    </div>
  </div>
</template>
<script>
  import {Sokoban} from "../js/Game.ts";
  import CanvasSokoban from "../component/CanvasSokoban";

  const axios = require("axios");

  export default {
    components: {CanvasSokoban,},
    data() {
      const that = this;
      return {
        game: new Sokoban(),
        index: null,//游戏数据索引
        maps: null,//地图列表
        curLevel: 0,
        Skin: {
          init(skins, callback) {
            const el = document.querySelector("#skin")
            for (let skinInd = 0; skinInd < skins.length; skinInd++) {
              const skinItem = that.index.skins[skinInd];
              const op = document.createElement("option");
              op.value = skinInd;
              op.innerText = skinItem.name;
              el.append(op);
            }
            el.value = 0;
            this.loadSkin(0, () => {
              callback();
            })
          },
          changeSkin() {
            //更改皮肤
            const el = document.querySelector("#skin")
            el.blur();
            this.loadSkin(el.value, () => {
              this.$refs.canvas.drawMap();
            })
          },
          getSkin() {
            const skinIndex = parseInt(document.querySelector("#skin").value);
            return that.index.skins[skinIndex];
          },
          loadSkin(skinIndex, callback) {
            //加载皮肤
            const skin = that.index.skins[skinIndex];
            const imageKeys = Object.keys(skin.images);
            let loaded = 0;//已经加载成功的个数
            for (let k of imageKeys) {
              if (typeof (skin.images[k]) === "string") {
                //如果没有加载过，则加载之
                const img = new Image();
                img.onload = () => {
                  if (++loaded === imageKeys.length) {
                    callback();
                  }
                }
                img.src = skin.images[k];
                skin.images[k] = img;
              } else {
                //只要有一个已经加载过了，那就全部都加载过了
                callback();
                return;
              }
            }
          }
        }
      };
    },
    mounted() {
      document.body.onresize = () => this.$refs.canvas.drawMap();
      window.onpopstate = (event) => this.initGame(event.state || 0, false)
      axios.all([axios.get("index.json"), axios.get("/api/get_maps")]).then(responses => {
        const [indexResp, mapsResp] = responses;
        this.index = indexResp.data;
        this.Skin.init(this.index.skins, () => {
          let gameIndex = 0;
          const query = location.search.slice(1).split("&").map(x => x.split('='));
          let game = query.filter(x => x[0] === 'game');
          if (game.length) gameIndex = parseInt(game[0][1]);
          this.initGame(gameIndex, false);
        });
        this.maps = mapsResp.data;
      })
    },
    methods: {
      onKeydown(event) {
        const k = event.key.toLowerCase();
        if (k.startsWith("arrow")) {
          const direction = k.slice(5);//移动的方向
          this.move(direction);
          return;
        }
        if (event.ctrlKey && event.key.toLowerCase() === 'z') {
          //ctrl+z，撤销一步
          this.game.back();
          this.$refs.canvas.drawMap();
        }
      },
      move(direction) {
        const moved = this.game.move(direction);
        if (!moved) return;
        this.$refs.canvas.drawMap();
        if (this.game.isOver()) {
          const opList = this.game.getOpList();
          const map = this.maps[this.mapIndex].question;
          this.$nextTick(() => {
            this.$message("恭喜胜利！")
          })
          axios.get({
            params: {
              q: map,
              a: opList,
            }
          }).then(resp => {
            console.log(resp.data)
          })
        }
      },
      loadString(content) {
        //直接加载一个地图字符串
        this.game.loadPsb(content);
        this.$refs.canvas.drawMap();
      },
      initGame(mapIndex, updateHistory) {
        const title = `【推箱子】第${mapIndex}关`;
        const question = this.maps[mapIndex];
        console.log(question);
        document.title = title;
        if (updateHistory) {
          history.pushState(mapIndex, mapIndex, `?game=${mapIndex}`);
        }
        this.curLevel = mapIndex;
        this.loadString(question.question);
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