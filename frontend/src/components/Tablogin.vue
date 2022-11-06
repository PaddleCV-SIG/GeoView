<template>
  <span class="date hidden-sm-and-down"><i
    class="iconfont icon-shijian"
  /><span class="hms">{{ currenthour }}:{{ currentminute }}:{{
    currentsecond
  }}</span><span class="ymd">[{{ currentyear }}-{{ currentmonth }}-{{
    currentday
  }}]</span></span>

  <div style="margin-left:15px">
    <i
      class="iconfont icon-github"
      @click="goGithub"
    />
  </div>
</template>

<script>
import {getCurrentTime} from "@/utils/gettime.js"
export default {
  data() {
    return {
      currentyear: "",
      currentday: "",
      currentmonth: "",
      currenthour: "",
      currentminute: "",
      currentsecond: "",
      getDate: "",
    };
  },
  mounted() {
    this.getCurrentTime();
  },
  unmounted() {
    clearTimeout(this.getDate);
  },
  methods: {
    getCurrentTime,
    goGithub(){
      window.open('https://github.com/PaddleCV-SIG/GeoView');
    },
  },
};
</script>
<style scoped>
* {
    font-family: Microsoft JhengHei UI, sans-serif;
}
.date {
  font-family: Microsoft YaHei;
  font-weight: 400;
}
.hms {
  color: rgb(64,158,255);
  font-size: 18px;
}
.ymd {
  color: var(--theme--color);
  font-size: 18px;
}

</style>
