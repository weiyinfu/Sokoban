静态地图组件，只用来展示地图，无法操作
<template>
  <CanvasSokoban :game="game" ref="canvas" class="StaticMap"></CanvasSokoban>
</template>
<script>
  import CanvasSokoban from "./CanvasSokoban";
  import {Game} from "../js/Game.ts";

  export default {
    props: {
      map: {
        type: String,
      }
    },
    components: {
      CanvasSokoban,
    },
    data() {
      const game = new Game();
      game.loadXsb(this.map);
      return {
        game
      }
    },
    mounted() {
      this.$refs.canvas.drawMap();
    }
  }
</script>