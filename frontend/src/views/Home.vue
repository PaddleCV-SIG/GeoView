<template>
  <el-container>
    <el-aside width="auto">
      <AsideVue
        :is-collapse="isCollapse"
        :active-index="activeIndex"
      />
    </el-aside>
    <el-container>
      <el-main
        class="main-ctx"
      >
        <el-header class="platform-header">
          <el-row align="middle">
            <i
              class="iconfont icon-caidan"
              @click="goCollapse"
            /><Tablogin />
          </el-row>
        </el-header>
        <router-view v-slot="{ Component }">
          <transition
            name="fade"
            mode="out-in"
          >
            <component :is="Component" />
          </transition>
        </router-view>
        <el-backtop
          target=".main-ctx"
          :bottom="40"
          :visibility-height="50"
          :right="27"
        />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import "@/assets/css/app.css";
import AsideVue from "@/components/AsideVue";
import Tablogin from "@/components/Tablogin";

export default {
  name: "Home",
  components: {
    AsideVue,
    Tablogin,
  },
  data() {
    return {
      isCollapse: false,
      scrollTop: "",
      activeIndex: this.$route.path,
    };
  },
  mounted() {
    window.onresize = () => {
      this.isCollapse = document.documentElement.clientWidth <= 1100;
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
.main-ctx {
  height: 100vh;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s 
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.platform-header{
  left: -20px;
  width: 105%;
}
</style>