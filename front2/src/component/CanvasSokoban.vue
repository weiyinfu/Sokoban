基于canvas的推箱子
<template>
  <canvas class="CanvasSokoban"
          @keydown="onKeydown"
          v-hammer:swipe="onSwipe"
          tabindex="-1"
          style="outline: none"></canvas>
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
        autoPlayId: 1,
        autoPlayInterval: 200,
      }
    },
    watch: {
      "$store.state.config.skinIndex"() {
        this.drawMap();
      },
      "game.question"() {
        //当游戏问题发生改变之后，停止自动播放
        this.autoPlayId++;
      }
    },
    methods: {
      onSwipe(event) {
        const direction = this.getDirection(event.angle);
        console.log(direction);
        this.move(direction);
      },
      onKeydown(event) {
        const k = event.key.toLowerCase();
        if (k.startsWith("arrow")) {
          const direction = k.slice(5);//移动的方向
          this.move(direction);
          event.preventDefault();
          event.stopPropagation();
          return;
        }
        if (event.ctrlKey && event.key.toLowerCase() === 'z') {
          //ctrl+z，撤销一步
          this.game.back();
          this.drawMap();
        }
      },
      stopAutoPlay() {
        this.autoPlayId++;
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
        //当用户移动一步的时候，清空自动演示
        this.autoPlayId++;
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
        const canvas = this.$el.querySelector("canvas") || this.$el;
        const ctx = canvas.getContext("2d");
        const a = this.game.curMap;
        const body = this.$el.parentElement;
        const dim = this.game.getSize();
        const size = Math.floor(Math.min(body.clientWidth / dim.cols, body.clientHeight / dim.rows));
        canvas.height = size * dim.rows;
        canvas.width = size * dim.cols;
        //获取皮肤
        const images = this.skin.images;
        let manPos = null;
        const lastMove = this.game.getLastMove();
        const index = this.index;
        for (let i = 0; i < a.length; i++) {
          for (let j = 0; j < a[i].length; j++) {
            ctx.drawImage(images.space, size * j, size * i, size, size);
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
              ctx.drawImage(pic, size * j - (sz - size) / 2, size * i - (sz - size) / 2, sz, sz);
            }
          }
        }
        //在编辑模式下，可能没有人，所以此处需要添加判断
        if (manPos) {
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
          ctx.drawImage(pic, size * j - (sz - size) / 2, size * i - (sz - size) / 2, sz, sz);
        }
      }
    }
  }
</script>