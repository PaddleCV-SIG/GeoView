<template>
  <div id="app">
    <router-view />
    <el-backtop :bottom="40" :visibility-height="50" :right="27"> </el-backtop>
  </div>
</template>
<script>
import * as echarts from 'echarts'
import { provide } from 'vue'
export default {
   name: 'App',
  setup(){
    provide('echarts',echarts)               //provide
  },
 
}
</script>


