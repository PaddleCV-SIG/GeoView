<template>
  <Drawer :active-index="activeIndex" />
  <div
    v-show="isLogin"
    class="common-layout"
  >
    <el-container>
      <el-aside width="auto">
        <AsideVue
          :is-collapse="isCollapse"
          :active-index="activeIndex"
        />
      </el-aside>
      <el-container>
        <el-main
          class="gotop"
          style="overflow-x:hidden"
        >
          <el-header class="theheader">
            <el-row align="middle">
              <i
                class="iconfont icon-caidan"
                style="margin-right:30px;font-size:32px"
                @click="goCollapse"
              /><Tablogin />
            </el-row>
          </el-header>
          <!-- https://segmentfault.com/a/1190000040935668界面渐入渐出效果 -->
          <router-view v-slot="{ Component }">
            <transition
              name="fade"
              mode="out-in"
            >
              <keep-alive
                include="detecttargets,detectchanges,classify,classifyscenes,restoreimgs,onlinemap"
              >
                <component :is="Component" />
              </keep-alive>
            </transition>
          </router-view>
          <el-backtop
            target=".gotop"
            :bottom="40"
            :visibility-height="50"
            :right="27"
          />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import "@/assets/css/app.css";
import AsideVue from "@/components/AsideVue";
import Tablogin from "@/components/Tablogin";
import Drawer from "@/components/Drawer.vue";
import BackTop from "@/components/BackTop";

export default {
  name: "Home",
  components: {
    AsideVue,
    Tablogin,
    Drawer,
    BackTop,
  },
  data() {
    return {
      isCollapse: false,
      isLogin: true,
      scrollTop: "",
      activeIndex: this.$route.path,
    };
  },
  mounted() {
    window.onresize = () => {

      if (document.documentElement.clientWidth <= 1100) {
        this.isCollapse = true;
      } else {
        this.isCollapse = false;
      }
    };
    document.body.style.overflow = "hidden";
  },
  updated(){
    this.activeIndex=this.$route.path
  },

  methods: {
    goCollapse() {
      this.isCollapse = !this.isCollapse;
    },
  }
};
</script>

<style scoped>
.el-main {
  --el-main-padding: 0px 20px 0 20px;
  height: auto;
  width: 100%;
  overflow-x: hidden;
}
.gotop {
  height: 100vh;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.theheader{
  left: -20px;
  width: 105%;
}
</style>