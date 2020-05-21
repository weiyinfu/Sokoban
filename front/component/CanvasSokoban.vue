基于canvas的推箱子
<template>
  <canvas @keydown="onKeydown" tabindex="-1" style="outline: none"></canvas>
</template>
<script>
  const GameMixin = require("../js/GameMixin.js");
  export default {
    props: {
      game: {
        type: Object,
      }
    },
    mixins: [GameMixin],
    data() {
      return {
        canvas: null,
        ctx: null,
        autoPlayId: 0,
        autoPlayInterval: 500,
      }
    },
    watch: {
      "$store.state.config.skinIndex"() {
        this.drawMap();
      }
    },
    mounted() {
      this.canvas = this.$el.querySelector("canvas") || this.$el;
      this.ctx = this.canvas.getContext("2d");
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
          this.drawMap();
        }
      },
      autoPlay(oplist) {
        //自动演示一个操作序列
        const go = (index, autoPlayId) => {
          if (index >= oplist.length) return;
          if (autoPlayId !== this.autoPlayId) return;
          const ind = "udlr".indexOf(oplist[index]);
          const direction = "up down left right".split(/\s+/)[ind];
          this.game.move(direction);
          this.drawMap();
          setTimeout(() => go(index + 1, autoPlayId), this.autoPlayInterval)
        }

        //每秒钟走一步
        const autoPlayId = ++this.autoPlayId;
        setTimeout(() => {
          go(0, autoPlayId)
        }, this.autoPlayInterval);
      },
      move(direction) {
        const moved = this.game.move(direction);
        if (!moved) return;
        this.drawMap();
        if (this.game.isOver()) {
          this.$emit("over", {
            q: this.game.question,
            a: this.game.getOpList(),
          })
        }
      },
      //绘制每个游戏关卡地图
      drawMap() {
        /**
         * 此处为了美观，对skin1做了特殊处理，代码不够优雅
         * */
            //不同的行可能长度不相同
        const a = this.game.curMap;
        const body = this.$el.parentElement;
        const dim = this.game.getSize();
        const size = Math.floor(Math.min(body.clientWidth / dim.cols, body.clientHeight / dim.rows));
        this.canvas.height = size * dim.rows;
        this.canvas.width = size * dim.cols;
        //获取皮肤
        const images = this.skin.images;
        let manPos = null;
        const lastMove = this.game.getLastMove();
        const index = this.index;
        for (let i = 0; i < a.length; i++) {
          for (let j = 0; j < a[i].length; j++) {
            this.ctx.drawImage(images.space, size * j, size * i, size, size);
            if (a[i][j]) {
              //如果不是空白，那么再画一层
              let name = index.images[a[i][j]];
              if (name === "man" || name === "manSlot") {
                //如果是人或者墙，size应该大一些
                manPos = [i, j];
                continue;
              }
              let sz = size;
              if (name === "slot" && this.skin.name === "skin1") {
                //slot应该小一些
                sz /= 3;
              }
              if (name === "man") {
                name = lastMove;
              }
              const pic = images[name];
              if (!pic) {
                throw new Error("cannot find " + name);
              }
              this.ctx.drawImage(pic, size * j - (sz - size) / 2, size * i - (sz - size) / 2, sz, sz);
            }
          }
        }
        const pic = images[lastMove];
        let [i, j] = manPos;
        let sz = size;
        if (this.skin.name === "skin1") {
          //此处特殊处理一下，只有skin2才让人物变得大一点
          sz = size * 1.3;
        }
        if (!pic) {
          throw new Error("cannot find picture of " + lastMove);
        }
        this.ctx.drawImage(pic, size * j - (sz - size) / 2, size * i - (sz - size) / 2, sz, sz);
      }
    }
  }
</script>