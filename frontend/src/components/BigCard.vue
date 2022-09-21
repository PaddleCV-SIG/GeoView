<template>
  <el-row :gutter="60" justify="center" style="margin-bottom: 40px">
    <el-col :xs="20" :sm="10" :md="10" :lg="7" :xl="7" id="go-big1"
      ><div class="singlecard">
        <div class="cardinfor"><slot name="left"></slot></div></div
    ></el-col>

    <el-col :xs="20" :sm="10" :md="10" :lg="7" :xl="7" id="go-big2"
      ><div class="singlecard">
        <div class="cardinfor"><slot name="middle"></slot></div></div
    ></el-col>

    <el-col :xs="20" :sm="10" :md="10" :lg="7" :xl="7" id="go-big3"
      ><div class="singlecard">
        <div class="cardinfor"><slot name="right"></slot></div></div
    ></el-col>
  </el-row>
</template>

<script>
export default {
  name: "bigcard",
}
</script>

<style>
.cardinfor:hover::after {
  width: 100%;
  background: #2878eb;
}
.cardinfor::after {
  position: absolute;
  content: "";
  width: 0;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 2px 2px 0 0;
  transition: 0.5s;
  z-index: -1;
}
.singlecard:hover * {
  color: #ecf4ff !important;
}
.cardinfor {
  z-index: 1;
}

.cardinfor {
  overflow: hidden;
  margin: 0 auto;
  width: auto;
  height: 400px;
  position: relative !important;
  border-radius: 2px !important;
  border-bottom: 5px solid rgb(40, 120, 235) !important;
}
.singlecard {
  width: auto;
  height: 400px;
  background-color: rgb(236, 244, 255);
  position: relative;
  /* border-width: 5px!important; */
}
</style>