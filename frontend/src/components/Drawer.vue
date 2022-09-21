<template>
  <div
    type="primary"
    style="margin-left: 16px"
    class="alldrawer hidden-md-and-down"
    @click="drawer = true"
  >
    <div class="drawer2">
      <span>快速导航</span>
    </div>
    <div class="drawer3">
      <i class="iconfont icon-feiji" />
    </div>
  </div>

  <el-drawer
    v-model="drawer"
    title="快速导航"
    :direction="direction"
    :size="size"
  >
    <el-menu
      class="el-menu-vertical-demo"
      :collapse="isCollapse"
      text-color="black"
      background-color="white"
      :default-active="activeIndex"
      active-text-color="#FFFFFF"
    >
      <el-menu-item-group>
        <el-menu-item
          index="/detectchanges"
          @click="goDetectChanges"
        >
          <h3>
            <i class="iconfont icon-bianhuajiance" />变化检测
          </h3>
        </el-menu-item>
        <el-menu-item
          index="/detecttargets"
          @click="goDetectTargets"
        >
          <h3>
            <i
              class="iconfont icon-mubiaojiance"
              style="font-size: 25px"
            />目标检测
          </h3>
        </el-menu-item>
        <el-menu-item
          index="/classify"
          @click="goClassify"
        >
          <h3>
            <i
              class="iconfont icon-erfenleibianhuajiance16px"
              style="font-size: 13px"
            />地物分类
          </h3>
        </el-menu-item>
        <el-menu-item
          index="/onlinemap"
          @click="goOnlineMap"
        >
          <h3>
            <i
              class="iconfont icon-zaixianditu"
              style="font-size: 19px"
            />在线地图
          </h3>
        </el-menu-item>
      </el-menu-item-group>
    </el-menu>
  </el-drawer>
</template>

<script>
import {
  goDetectChanges,
  goDetectTargets,
  goClassify,
  goOnlineMap
} from "@/utils/gosomewhere.js";
export default {
  name: "Drawer",
  props: ["activeIndex", "isCollapse"],
  data() {
    return {
      drawer: false,
      direction: "rtl",
      size: "15%",
    };
  },
  methods: {
    goDetectChanges,
    goDetectTargets,
    goClassify,
    goOnlineMap,
  },
};
</script>

<style lang="less" scoped>
.alldrawer {
  position: fixed;
  z-index: 100;
  background: rgb(252, 252, 252);
  top: 200px;
  right: 0;
  width: 34px;
  height: 120px;
  padding: 0.5rem;
  border-top-left-radius: 0.2rem;
  border-bottom-left-radius: 0.2rem;
  box-shadow: -5px 0px 10px 0px rgba(0, 0, 0, 0.1);
  transition: all 0.1s ease-in-out;
  cursor: pointer;
  font-family: Microsoft JhengHei UI, sans-serif;
}
.drawer2 {
  font-size: 17px;
  font-weight: 1000;
  -webkit-writing-mode: vertical-rl;
  writing-mode: vertical-rl;
  color: rgb(64,158,255);
  background: rgb(237, 242, 245);
  padding: 0.12rem;
  border-radius: 0.2rem;
  height: 80px;
  text-align: center;
  width: 33px;
  span {
    display: block;
    padding-right: 6px;
  }
}
.drawer3 {
  width: 37px;
  text-align: center;
  margin-top: 6px;
  color: rgb(64,158,255);
  background: rgb(237, 242, 245);
  border-radius: 0.2rem;
  height: 30px;
  .iconfont {
    display: block;
    padding-top: 5px;
  }
}
.drawer2:hover,
.drawer3:hover {
  background-color: rgb(228, 235, 240);
}
// .el-drawer rtl open {
//   z-index: 1000;
//   width: 50rem !important;
// }
.el-menu{
  width: 100%;
}
</style>