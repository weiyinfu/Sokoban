<template>
  <div class="About">
    <header-part active-tab="关于"></header-part>
    <div class="body">
      <div class="wrapper">
        <h1>推箱子的来历</h1>
        <p>
          推箱子游戏起源于日本，名为sokoban。推箱子是日本人今林宏行于1981年发明并且编写程序实现的，1982年由Thinking Rabbit公司在日本发行。日文原名《仓库番》，英语音译为
          Sokoban，中文目前最通用的叫法是推箱子。
        </p>
        <h1>推箱子的玩法</h1>
        <p>
          用键盘上的上、下、左、右键移动小人，把箱子全部推到指定的位置即可过关。箱子只能推，不能拉，并且小人一次只能推动一个箱子。
        </p>
        <h1>推箱子地图的XSB格式</h1>
        <p>
          XSB格式是一种纯文本格式，用来描述推箱子地图。

        </p>
        <p>- 空白</p>
        <p>. 插槽</p>
        <p>@ 人</p>
        <p>+ 人在插槽处</p>
        <p>$ 箱子</p>
        <p>* 箱子在插槽处</p>
        <p># 墙</p>
        <h1>推箱子的乐趣</h1>
        <p>推箱子为什么吸引人？有以下几个方面：

        </p>
        <ul>
          <li>推箱子很简单：推箱子定义是很简单的，“华容道”中每个物体大小不一样，机关很难被人理解，而推箱子每个物体只占有一个空格。箱子只能推不能拉，符合“人体力学”。好的游戏一定是符合“人体力学”，容易被人理解的。</li>
          <li>推箱子是开放的问题：棋类游戏通常有固定的开局和终局，而推箱子丰富多彩，可以有无数种地图，无论是设计地图还是解决推箱子问题，都是开放的问题，永远不嫌多，就像棋类游戏的残局一样。</li>
          <li>推箱子只需要一个人就能玩：当自己感到无聊时，思考一下推箱子，是很有趣的一件事。</li>
          <li>推箱子很难：推箱子无法用计算机求解，推箱子是NP问题，现有的计算机算力只能处理较小地图的推箱子。一旦一个问题能够用计算机解决，人就会觉得没有意义。</li>
        </ul>
        <h1>相关链接</h1>
        <p>
          <a href="https://github.com/weiyinfu/Sokoban" target="_blank">本程序</a>是一个开源网站，后端使用Python语言实现，前端使用Vue技术栈（Vue+Vuex+VueRouter）。
        </p>
      </div>
    </div>
  </div>
</template>
<script>
  import HeaderPart from "./HeaderPart";

  export default {
    components: {
      HeaderPart
    },
    data() {
      return {}
    },
    activated() {
      document.title = "推箱子-关于"
    }
  }
</script>
<style lang="less">
  .About {
    .body {
      padding: 20px;
      box-sizing: border-box;
      display: flex;
      align-items: center;
      justify-content: center;

      .wrapper {
        padding: 30px;
        max-width: 500px;
        background: whitesmoke;
      }
    }
  }
</style>