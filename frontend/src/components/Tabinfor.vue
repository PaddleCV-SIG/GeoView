
<template>
  <el-row
    justify="center"
    align="middle"
  >
    <el-col
      :xs="8"
      :sm="8"
      :md="8"
      :lg="8"
      :xl="8"
    >
      <div><slot name="left" /></div>
    </el-col>
    <el-col
      :xs="8"
      :sm="8"
      :md="8"
      :lg="8"
      :xl="8"
      style="text-align:center"
    >
      <div><slot name="mid" /></div>
    </el-col>
    <el-col
      :xs="7"
      :sm="7"
      :md="7"
      :lg="7"
      :xl="7"
      style="text-align: right"
    >
      <div><slot name="right" /></div>
    </el-col>
    <el-col
      :xs="1"
      :sm="1"
      :md="1"
      :lg="1"
      :xl="1"
    />
  </el-row>
</template>

<script>
export default {
  name: "Tabinfor",
};
</script>

<style>
</style>