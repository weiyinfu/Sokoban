基于canvas的推箱子
<template>
  <canvas></canvas>
</template>
<script>
  export default {
    props: {
      game: {
        type: Object,
      },
      Skin: {
        type: Object,
      },
      index: {
        type: Object,
      }
    },
    data() {
      return {
        canvas: null,
        ctx: null,
      }
    },
    mounted() {
      this.canvas = this.$el.querySelector("canvas") || this.$el;
      this.ctx = this.canvas.getContext("2d");
    },
    methods: {
      //绘制每个游戏关卡地图
      drawMap() {
        //不同的行可能长度不相同
        const a = this.game.curMap;
        const body = this.$el.parentElement;
        const maxCols = a.map(x => x.length).reduce((o, n) => Math.max(o, n), 0);
        const size = Math.floor(Math.min(body.clientWidth / maxCols, body.clientHeight / a.length));
        this.canvas.height = size * a.length;
        this.canvas.width = maxCols * size;
        const ctx = this.ctx;
        //获取皮肤
        const skin = this.Skin.getSkin();
        const images = skin.images;
        let manPos = null;
        const lastMove = this.game.getLastMove();
        for (let i = 0; i < a.length; i++) {
          for (let j = 0; j < a[i].length; j++) {
            ctx.drawImage(images.space, size * j, size * i, size, size);
            if (a[i][j]) {
              //如果不是空白，那么再画一层
              let name = this.index.images[a[i][j]];
              if (name === "man" || name === "manSlot") {
                //如果是人或者墙，size应该大一些
                manPos = [i, j];
                continue;
              }
              let sz = size;
              if (name === "slot") {
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
        const pic = images[lastMove];
        let [i, j] = manPos;
        let sz = size;
        if (skin.name === "skin1") {
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
</script>