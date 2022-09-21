<template>
  <el-menu
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    text-color="black"
    background-color="rgb(247,246,242)"
    style="height: 100vh"
    :default-active="activeIndex"
    active-text-color="#FFFFFF"
  >
    <div class="ourtitle">
      <img :src="require('@/assets/image/logo/80.png')" style="width:45px;color:rgb(64,158,255);"  @click="goRemoteSense">
      <div v-if="!isCollapse" id="bigtitle">
        <a @click="goShow" class="platform"
          >Hippo智能遥感解译平台</a
        >
      </div>
    </div>
    <el-divider content-position="center">
      <span v-show="!isCollapse" class="funtitle" style="color: rgb(140, 157, 182)"
        >功能区</span
      >
    </el-divider>
    <div class="item-group">
      <el-menu-item index="/detectchanges" @click="goDetectChanges"
        ><i class="iconfont icon-bianhuajiance" v-show="isCollapse"></i>
        <h3 v-show="!isCollapse" >
          <i class="iconfont icon-bianhuajiance"></i>变化检测
        </h3></el-menu-item
      >
    </div>
    <div class="item-group">
      <el-menu-item index="/detecttargets" @click="goDetectTargets"
        ><i
          class="iconfont icon-mubiaojiance"
          v-show="isCollapse"
          style="font-size: 22px"
        ></i>
        <h3 v-show="!isCollapse">
          <i class="iconfont icon-mubiaojiance" style="font-size: 22px"></i
          >目标检测
        </h3></el-menu-item
      >
    </div>
    <div class="item-group">
      <el-menu-item index="/classify" @click="goClassify"
        ><i
          class="iconfont icon-erfenleibianhuajiance16px"
          v-show="isCollapse"
          style="font-size: 14px"
        ></i>
        <h3 v-show="!isCollapse">
          <i

            class="iconfont icon-erfenleibianhuajiance16px"
            style="font-size: 14px"
          ></i
          >地物分类
        </h3></el-menu-item
      >
    </div>
        <div class="item-group">
      <el-menu-item index="/onlinemap" @click="goOnlineMap"
        ><i
          class="iconfont icon-zaixianditu"
          v-show="isCollapse"
          style="font-size: 20px"
        ></i>
        <h3 v-show="!isCollapse">
          <i
            class="iconfont icon-zaixianditu"
            style="font-size: 20px"
          ></i
          >在线地图
        </h3></el-menu-item
      >
    </div>
    <el-divider content-position="center">
      <span v-show="!isCollapse" class="title">历史记录</span>
    </el-divider>
    <div class="item-group">
      <el-menu-item index="/history" @click="goHistory"
        ><i class="iconfont icon-history" v-show="isCollapse"></i>
        <h3 v-show="!isCollapse">
          <i class="iconfont icon-history"></i>我的历史记录
        </h3></el-menu-item
      >
    </div>
    <el-divider content-position="center">
      <span v-show="!isCollapse" class="title"></span>
    </el-divider>

  </el-menu>
</template>

<script>
import {
  goDetectChanges,
  goDetectTargets,
  goClassify,
  goHistory,
  goOnlineMap
} from "@/utils/gosomewhere.js";
export default {
  props: ["isCollapse", "activeIndex"],
  data() {
    return {};
  },
  methods: {
    goDetectChanges,
    goDetectTargets,
    goClassify,
    goHistory,
    goOnlineMap,
    goShow(){
      this.$message.success('欢迎来到本平台')
    }
  },
};
</script>


<style lang="less" >
.el-menu {
  position: relative;
  top: 0;
  bottom: 0;
  text-align: center;
  overflow-x: hidden;

 font-family: Microsoft JhengHei UI, sans-serif;

}
.el-menu-item {
  padding: 0 0;
  border-radius: 10px;
  position: relative;
      color: rgb(117,117,117);
  h3 {

    padding-right: 30px;
    width: 100%;
    margin: 0 auto;
    .iconfont {
      font-weight: normal;
      margin-right: 5px;
      font-size: 20px;
    }
  }
}
.item-group {
  position: relative;
}
.el-menu-item :hover::after {
  width: 100%;
  background: rgb(64,158,255);
}
.el-menu-item ::after {
  position: absolute;
  content: "";
  width: 0;
  height: 100%;
  top: 0;
  left: 0;
  // border-radius: 2px 2px 0 0;
  border-radius: 10px;
  transition: 0.25s;
  z-index: -1;
}
.item-group:hover * {
  color: #ecf4ff !important;
}
.el-menu-item {
  z-index: 1;
}
.item-group * {
  transition: 0.5s;
}
.el-menu-item {
  position: relative !important;
}

.el-menu-item:hover {
  background-color: rgb(247, 246, 242);
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
.is-active {
  background-color: rgb(64,158,255);
}
.el-aside {
  top: 0;
  bottom: 0;
}
.el-menu el-menu-vertical-demo {
  height: 100vh;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 250px;
}
.ourtitle {
  margin-top: 9px;
  margin-bottom: -15px;
  text-align: center;
  color: rgb(64,158,255);
  height: 80px;
  width: auto;
  overflow: hidden;
  .iconfont {
    cursor: pointer;
    transition: all 0.5s;
  }
  .iconfont:hover {
    transform: scale(1.2);
  }
}
.funtitle {
  display: block;
  line-height: 24.4px;
  overflow: hidden;
  width: 70px;
}
.el-divider__text {
  background-color: rgb(247, 246, 242) !important;
}
#bigtitle {
  position: relative;
  font-size: 20px;
  font-weight: 1000;
  cursor: pointer;
}
#bigtitle::after {
  content: "";
  width: 0px;
  height: 3px;
  background:rgb(64,158,255);
  position: absolute;
  top: 100%;
  left: 50%;
  right: 50%;
  transition: all 0.5s;
}
#bigtitle:hover:after {
  left: 7%;
  right: 7%;
  width: 85%;
}

.platform{
  color: rgb(64,158,255);
  font-family: Microsoft JhengHei UI, sans-serif;
  font-size: 21px;
}
</style>
 
 