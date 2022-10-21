<template>
  <div
    id="cards"
    v-drag
    class="drag-box"
  >
    <div class="drag-title">
      相关信息
    </div>
    <span
      class="shut-bitton"
      @click="shutDown"
    ><i class="iconfont icon-guanbi" /></span>
    <el-divider style="margin-top: 10px" />
    <div class="infor-row">
      <div class="infor">
        <slot name="left-1" />
      </div>
      <div class="icon">
        <slot name="rightIcon-1" />
      </div>
    </div>
    <div class="infor-row">
      <div class="infor">
        <slot name="left-2" />
      </div>
      <div class="icon">
        <slot name="rightIcon-2" />
      </div>
    </div>
    <div class="drag-box-item">
      {{ childImgInfor.id }}
    </div>
    <slot />
  </div>
</template>

<script>
export default {
  name: "DraggableItem",
  props:{
    imgInfor:{
      type:Object,
      default:()=>{
        return {}
      }
    }
  },
  emits:['child-vannish'],
  data(){
    return{
      childImgInfor:{}
    }
  },
  mounted() {
    this.childImgInfor = this.imgInfor
  },
  updated() {
    this.childImgInfor = this.imgInfor
  },
  methods:{
    shutDown(){
      this.$emit('child-vannish')
    }
  },
}
</script>

<style scoped lang="less">
.drag-box{
  position: absolute;
  top: 420px;
  left: -60px;
  width: 300px;
  height: 200px;
  padding: 10px;
  z-index: 200;
  background-color: white;
  cursor: pointer;
  box-shadow: 1px 1px 5px #535353;
  border-radius: 10px;
  outline: 2px dashed var(--theme--color);
  outline-offset: -4px;
  .shut-bitton{
    position: absolute;
    right: 20px;
    top: 10px;
  }
  .drag-title{
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: "幼圆", sans-serif;
    font-weight: 500;
    font-size: 22px;
  }
  .drag-box-item{
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
  }
}
.infor-row{
  margin: 10px;
  display: flex;
  justify-content: space-between;
}

</style>