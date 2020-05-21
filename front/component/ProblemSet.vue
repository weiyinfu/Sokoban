<template>
  <div class="ProblemSet">
    <HeaderPart></HeaderPart>
    <div class="body">
      <div class="total-desc">已解决 {{solvedCount}}/{{maps.length}}</div>
      <el-table :data="maps" :row-class-name="tableRowClassName">
        <el-table-column label="#">
          <template slot-scope="scope">
            {{scope.$index }}
          </template>
        </el-table-column>
        <el-table-column label="地图">
          <template slot-scope="scope">
            <router-link target="_blank" :to="'/game/'+scope.$index" class="map-link">
              <StaticMap :map="scope.row.question"></StaticMap>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="解法">
          <template slot-scope="scope">
            {{describeSolution(scope.row.answer)}}
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
  import StaticMap from "./StaticMap";
  import HeaderPart from "./HeaderPart";

  const GameMixin = require("../js/GameMixin.js");
  export default {
    components: {StaticMap, HeaderPart},
    mixins: [GameMixin],
    computed: {
      solvedCount() {
        return this.$store.state.maps.filter(map => map.answer).length
      },
    },
    activated() {
      document.title = "推箱子-题库"
    },
    methods: {
      tableRowClassName({row, rowIndex}) {
        return row.answer ? 'solved' : "";
      }
    }
  }
</script>
<style lang="less">
  .ProblemSet {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;

    .body {
      padding: 20px;
      box-sizing: border-box;
    }

    .solved {
      //已解决的问题的背景色
      background: #d9f0d9;
    }

    .total-desc {
      //已解决/未解决 标签
      border-radius: 10px;
      background: #337ab7;
      display: inline-block;
      color: white;
      padding: 4px;
      font-size: 12px;
    }

    .map-link {
      //地图超链接
      cursor: pointer;
      display: block;
    }

    .el-table--enable-row-hover .el-table__body tr:hover > td {
      background: unset;
    }
  }
</style>