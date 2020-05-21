<template>
  <div class="ProblemSet">
    <HeaderPart></HeaderPart>
    <div class="body">
      <div class="total-desc">已解决 {{solvedCount}}/{{maps.length}}</div>
      <el-table :data="maps" :row-class-name="tableRowClassName">
        <el-table-column
                label="#">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{scope.$index }}</span>
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
    data() {
      return {}
    },
    computed: {
      solvedCount() {
        return this.$store.state.maps.filter(map => map.answer).length
      },
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
    @header-height: 44px;

    .HeaderPart {
      height: @header-height;
    }

    .body {
      padding: 20px;
      box-sizing: border-box;
    }

    .solved {
      background: #d9f0d9;
    }

    .total-desc {
      border-radius: 10px;
      background: #337ab7;
      display: inline-block;
      color: white;
      padding: 4px;
      font-size: 12px;
    }

    .map-link {
      cursor: pointer;
      display: block;
    }
  }
</style>