地图组件
<template>
  <div class="MapView">
    <div>
      选择皮肤：
      <select v-model="skinIndex">
        <option v-for="(skin,ind) in index.skins" :value="ind">{{skin.name}}</option>
      </select>
    </div>
    <div>
      一共有{{maps.length}}个地图
      <div v-for="(map,ind) in maps">
        第{{ind}}关
        <div v-for="row in map">
          <img v-for="col in row" :src="getImage(col)">
        </div>
        <hr>
      </div>
    </div>
  </div>
</template>
<script>
  import {loadPsbString} from "../js/lib.ts";

  const axios = require("axios");
  export default {
    data() {
      return {
        index: {},
        maps: [],
        skinIndex: 0,
        music: '',
      }
    },
    mounted() {
      axios.get("index.json").then(resp => {
        this.index = resp.data;
      })
      axios.get("/api/get_maps").then(resp => {
        const maps = resp.data;
        for (let i = 0; i < maps.length; i++) {
          this.$set(this.maps, i, loadPsbString(maps[i].question));
        }
      })
    },
    methods: {
      getImage(ind) {
        let name = this.index.images[ind];
        if (name.startsWith('man')) {
          name = "down";
        }
        return this.index.skins[this.skinIndex].images[name];
      }
    },
  }
</script>
<style lang="less">
  .MapView {
    img {
      width: 20px;
      height: 20px;
    }
  }
</style>