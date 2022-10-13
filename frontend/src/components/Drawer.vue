<template>
  <div
    type="primary"
    style="margin-left: 16px"
    class="aside-nagvator hidden-md-and-down"
    @click="isNavigator = true"
  >
    <div class="aside-nagvator-title">
      <span>快速导航</span>
    </div>
    <div class="aside-nagvator-icon">
      <i class="iconfont icon-feiji" />
    </div>
  </div>

  <el-drawer
    v-model="isNavigator"
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
          index="/detectobjects"
          @click="goDetectObjects"
        >
          <h3>
            <i class="iconfont icon-mubiaojiance" />目标检测
          </h3>
        </el-menu-item>
        <el-menu-item
          index="/segmentation"
          @click="goSegmentation"
        >
          <h3>
            <i class="iconfont icon-erfenleibianhuajiance16px" />地物分类
          </h3>
        </el-menu-item>
        <el-menu-item
          index="/classification"
          @click="goClassification"
        >
          <h3>
            <i class="iconfont icon-changjingguanli" />场景分类
          </h3>
        </el-menu-item>
        <el-menu-item
          index="/restoreimgs"
          @click="goRestoreImgs"
        >
          <h3>
            <i class="iconfont icon-jishu" />图像复原
          </h3>
        </el-menu-item>
        <el-menu-item
          index="/onlinemap"
          @click="goOnlineMap"
        >
          <h3>
            <i class="iconfont icon-zaixianditu" />在线地图
          </h3>
        </el-menu-item>
      </el-menu-item-group>
    </el-menu>
  </el-drawer>
</template>

<script>
import {
  goDetectChanges,
  goDetectObjects,
  goSegmentation,
  goClassification,
  goRestoreImgs,
  goOnlineMap
} from "@/utils/gosomewhere.js";
export default {
  name: "Drawer",
  props: {
    isCollapse: {
      type: Boolean,
      default: false
    },
    activeIndex: {
      type: String,
      default: '/detectchanges'
    }
  },
  data() {
    return {
      isNavigator: false,
      direction: "rtl",
      size: "15%",
    };
  },
  methods: {
    goDetectChanges,
    goDetectObjects,
    goSegmentation,
    goClassification,
    goRestoreImgs,
    goOnlineMap,
  },
};
</script>

<style lang="less" scoped>
.aside-nagvator {
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
  box-shadow: -5px 0 10px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.1s ease-in-out;
  cursor: pointer;
  font-family: Microsoft JhengHei UI, sans-serif;

  .aside-nagvator-title {
    font-size: 17px;
    font-weight: 1000;
    -webkit-writing-mode: vertical-rl;
    writing-mode: vertical-rl;
    color: rgb(64, 158, 255);
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

  .aside-nagvator-icon {
    width: 37px;
    text-align: center;
    margin-top: 6px;
    color: rgb(64, 158, 255);
    background: rgb(237, 242, 245);
    border-radius: 0.2rem;
    height: 30px;

    .iconfont {
      display: block;
      padding-top: 5px;
    }
  }
}

.aside-nagvator-title:hover,
.aside-nagvator-icon:hover {
  background-color: rgb(228, 235, 240);
}
.el-menu {
  width: 100%;
  overflow-y: hidden;
}


</style>