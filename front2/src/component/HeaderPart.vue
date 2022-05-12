<template>
  <div class="HeaderPart">
    <div ref="tabs">
      <router-link to="/"><img src="https://weiyinfu.cn/learnSvg?text=推&background=white&color=purple"></router-link>
      <router-link to="/">题库</router-link>
      <router-link to="/add">贡献问题</router-link>
      <router-link to="/about">关于</router-link>
    </div>
    <div>
      <el-select v-model="skinIndex" placeholder="选择皮肤" @change="changeSkin">
        <el-option
                v-for="(item,ind) in $store.state.index.skins"
                :key="item.name"
                :label="item.name"
                :value="ind">
        </el-option>
      </el-select>
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        skinIndex: 0,
      }
    },
    props: {
      activeTab: {
        type: String,
        default: "题库",
      }
    },
    mounted() {
      this.skinIndex = this.$store.state.config.skinIndex;
      for (let tab of this.$refs.tabs.children) {
        if (tab.innerText === this.activeTab) {
          tab.style.color = 'red';
        }
      }
    },
    methods: {
      changeSkin(value) {
        this.$store.dispatch("loadSkin", value);
      }
    }
  }
</script>
<style lang="less">
  .HeaderPart {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: rgba(0, 0, 0, 0.65);
    height: 44px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);

    & > div {
      display: flex;
      align-items: center;
      height: 100%;

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
        margin: 0 10px;
        font-size: 14px;
      }

      & > * {
        margin: 0 10px;
      }
    }

  }

</style>