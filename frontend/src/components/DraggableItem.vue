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
    >X</span>
    <el-divider style="margin-top: 10px" />
    <div class="drag-box-item">
      {{ childImgInfor.id }}
    </div>
    <slot />
  </div>>
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
  right: 150px;
  top: 400px;
  width: 220px;
  height: 300px;
  padding: 10px;
  z-index: 200;
  background-color: white;
  cursor: pointer;
  box-shadow: 1px 1px 11px #535353;
  .shut-bitton{
    position: absolute;
    right: 5px;
    top: 10px;
  }
  .drag-title{
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .drag-box-item{
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
  }
}
</style>