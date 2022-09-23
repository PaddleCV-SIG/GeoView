<template>
  <div id="app">
    <router-view />
    <el-backtop
      :bottom="40"
      :visibility-height="50"
      :right="27"
    />
  </div>
</template>
<script>


export default {
   name: 'App',

}
</script>


