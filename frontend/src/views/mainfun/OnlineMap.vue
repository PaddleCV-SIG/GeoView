<template>
  <div style="width: 100%; height: 100%">
    <el-button
      class="button-dalod btn-animate2 btn-animate__surround"
      type="primary"
      title="截图上传"
      @click="toImage()"
    >
      截图上传
    </el-button>
    <el-input
      id="suggestId"
      v-model="address_detail"
      type="text"
      name="address_detail"
      placeholder="请输入地址"
      class="input_style"
    />
    <div
      id="map"
      ref="imageTofile"
      style="width: 100%; height: 100%"
      class="map"
    />
    <el-dialog
      v-model="choose"
      :modal="false"
      title="选择上传功能区"
      width="50%"
      top="12%"
    >
      <div class="upload-fun-select">
        <el-radio
          v-model="funtype"
          class="choose-item"
          label="目标检测"
          @change="selectFun"
        >
          目标检测
        </el-radio>
        <el-radio
          v-model="funtype"
          class="choose-item"
          label="地物分类"
          @change="selectFun"
        >
          地物分类
        </el-radio>
        <el-radio
          v-model="funtype"
          class="choose-item"
          label="场景分类"
          @change="selectFun"
        >
          场景分类
        </el-radio>
        <el-radio
          v-model="funtype"
          class="choose-item"
          label="图像复原"
          @change="selectFun"
        >
          图像复原
        </el-radio>
      </div>
      <div class="model-select">
        <span>选择处理模型：</span>
        <el-select
          v-model="uploadSrc.model_path"
          placeholder="请选择"
        >
          <el-option
            v-for="(item,index) in onSelectModelArr"
            :key="index"
            :label="item.model_name"
            :value="item.model_path"
          />
        </el-select>
      </div>
      <el-row>
        <el-button
          type="primary"
          class="btn-animate btn-animate__shiny"
          style="margin: 50px auto"
          @click="goUpload(funtype)"
        >
          开始处理
        </el-button>
      </el-row>
    </el-dialog>
    <el-dialog
      v-model="isShow"
      :modal="false"
      title="结果图展示"
      width="94%"
      top="6%"
    >
      <ImgShow
        :img-arr="imgArr"
      />
      <el-row justify="center">
        <el-button
          type="primary"
          class="btn-animate btn-animate__shiny"
          @click="removeImg"
        >
          确定
        </el-button>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import global from "@/global";
import html2canvas from "html2canvas";
import ImgShow from "@/components/ImgShow";
import { createSrc, imgUpload,getCustomModel} from "@/api/upload";
import {historyGetPage} from "@/api/history";
import loadMap from '@/utils/loadMap'

export default {
  name: "Onlinemap",
  components: {  ImgShow },
  data() {
    return {
      beforeImg: [],
      beforeList:[],
      afterImg: [],
      fit:'fill',
      isShow: false,
      tmpFile: "",
      choose: false,
      funtype: "目标检测",
      address_detail: null, //详细地址
      userlocation: { lng: "", lat: "" },
      lng: "",
      lat: "",
      htmlUrl: "",
      uploadSrc: { list: [], prehandle: 0, denoise: 0 ,model_path:''},
      scene:[{}],
      sceneKey:[['']],
      classificationModelArr:[],
      detectObjectsModelArr:[],
      segmentationModelArr:[],
      onSelectModelArr:[],
      restorationModelArr:[],
      imgArr:[],
    };
  },
  created() {
    this.getCustomModel('classification').then((res)=>{
      this.classificationModelArr = res.data.data
    })
    this.getCustomModel('object_detection').then((res)=>{
      this.detectObjectsModelArr = res.data.data
      this.onSelectModelArr = this.detectObjectsModelArr
      this.uploadSrc.model_path = this.onSelectModelArr[0]?.model_path
    })
    this.getCustomModel('semantic_segmentation').then((res)=>{
      this.segmentationModelArr = res.data.data
    })
    this.getCustomModel('image_restoration').then((res)=>{
      this.restorationModelArr = res.data.data
    })
  },
  mounted() {
  this.initMap()
  },

  methods: {
    createSrc,
    imgUpload,
    historyGetPage,
    getCustomModel,
    loadMap,
    initMap() {
      loadMap(process.env.VUE_APP_BAIDU_MAP_ACCESS_KEY)
          .then(() => {
            // 百度地图API功能
            let myMap = new BMap.Map("map") // 创建Map实例
            myMap.centerAndZoom(new BMap.Point(116.404, 39.915), 19) // 初始化地图,设置中心点坐标和地图级别
            myMap.setMapType(BMAP_HYBRID_MAP);
            //添加地图类型控件
            myMap.addControl(
                new BMap.MapTypeControl({
                  mapTypes: [BMAP_SATELLITE_MAP, BMAP_HYBRID_MAP],
                })
            )
            myMap.setCurrentCity('北京') // 设置地图显示的城市 此项是必须设置的
            myMap.enableScrollWheelZoom(true) //开启鼠标滚轮缩放

            this.$nextTick(function () {
              let th = this;
              let ac = new BMap.Autocomplete({
                //建立一个自动完成的对象
                input: "suggestId",
                location: this.myMap,
              });
              let myValue;
              ac.addEventListener("onconfirm", function (e) {
                //鼠标点击下拉列表后的事件
                let _value = e.item.value;
                myValue =
                    _value.province +
                    _value.city +
                    _value.district +
                    _value.street +
                    _value.business;
                th.address_detail = myValue;
                setPlace();
              });

              function setPlace() {
                myMap.clearOverlays(); //清除地图上所有覆盖物
                function myFun() {
                  th.userlocation = local.getResults().getPoi(0).point; //获取第一个智能搜索的结果
                  myMap.centerAndZoom(th.userlocation, 18);
                  // eslint-disable-next-line no-undef
                  myMap.addOverlay(new BMap.Marker(th.userlocation)); //添加标注
                  th.lng = th.userlocation.lng;
                  th.lat = th.userlocation.lat;
                }

                // eslint-disable-next-line no-undef
                let local = new BMap.LocalSearch(myMap, {
                  //智能搜索
                  onSearchComplete: myFun,
                });
                local.search(myValue)
                //测试输出坐标（指的是输入框最后确定地点的经纬度）
                myMap.addEventListener("click", function () {
                  this.lng = th.userlocation.lng;
                  this.lat = th.userlocation.lat;
                });
              }
            });

          })
          .catch(err => {
            console.log('地图加载失败')
          })
    },
    selectFun(val){
      switch (val){
        case '地物分类':
          this.onSelectModelArr = this.segmentationModelArr;break
        case '目标检测':
          this.onSelectModelArr = this.detectObjectsModelArr;break
        case '场景分类':
          this.onSelectModelArr = this.classificationModelArr;break
        case '图像复原':
          this.onSelectModelArr = this.restorationModelArr;break

      }
      this.uploadSrc.model_path = this.onSelectModelArr[0]?.model_path
    },
    goUpload(type) {
      let formData = new FormData();
      formData.append("files", this.tmpFile);
      formData.append("type", type);
      this.createSrc(formData).then((res) => {
        this.uploadSrc.list = res.data.data.map((item) => {
          return item.src;
        })
        if (type === "目标检测") {
          this.uploadSrc.prehandle = 0
          this.uploadSrc.denoise = 0
          this.imgUpload(this.uploadSrc,'object_detection').then((res) => {
            this.$message.success("上传成功！");
            this.choose = false;
            this.historyGetPage(1, 1, "目标检测").then((res) => {
              this.imgArr = res.data.data.forEach((item)=>{
                item['before_img'] = global.BASEURL+item.before_img
                item['after_img'] = global.BASEURL+item.after_img
              })
              this.imgArr = res.data.data
              this.isShow = true;
            });
          }).catch((rej)=>{})
        }
        if (type === "地物分类") {
          this.uploadSrc.prehandle = 0
          this.uploadSrc.denoise = 0
          this.imgUpload(this.uploadSrc,'semantic_segmentation').then((res) => {
            this.$message.success("上传成功！");
            this.choose = false;
            this.historyGetPage(1, 1, "地物分类").then((res) => {
              this.imgArr = res.data.data.forEach((item)=>{
                item['before_img'] = global.BASEURL+item.before_img
                item['after_img'] = global.BASEURL+item.after_img
              })
              this.imgArr = res.data.data
              this.isShow = true;
            }).catch((rej)=>{})
          }).catch((rej)=>{})
        }
        if (type === "场景分类") {
          delete(this.uploadSrc.denoise)
          delete (this.uploadSrc.prehandle)
          this.imgUpload(this.uploadSrc,'classification').then((res) => {
            this.$message.success("上传成功！");
            this.choose = false;
            this.historyGetPage(1, 1, "场景分类").then((res) => {
              this.imgArr = res.data.data.forEach((item)=>{
                item['before_img'] = global.BASEURL+item.before_img
              })
              this.imgArr = res.data.data
              this.isShow = true;
            }).catch((rej)=>{})
          }).catch((rej)=>{})
        }
        else if (type === "图像复原") {
          delete(this.uploadSrc.denoise)
          delete (this.uploadSrc.prehandle)
          this.imgUpload(this.uploadSrc,'image_restoration').then((res) => {
            this.$message.success("上传成功！");
            this.choose = false;
            this.historyGetPage(1, 1, "图像复原").then((res) => {
              this.imgArr = res.data.data.forEach((item)=>{
                item['before_img'] = global.BASEURL+item.before_img
                item['after_img'] = global.BASEURL+item.after_img
              })
              this.imgArr = res.data.data
              this.isShow = true;
            }).catch((rej)=>{})
          }).catch((rej)=>{})
        }
      }).catch((rej)=>{})
    },
    // 页面元素转图片
    toImage() {
      this.choose = true;
      // 手动创建一个 canvas 标签
      const canvas = document.createElement("canvas");
      // 获取父标签，意思是这个标签内的 DOM 元素生成图片
      // imageTofile是给截图范围内的父级元素自定义的ref名称
      let canvasBox = this.$refs.imageTofile;
      // 获取父级的宽高
      const width = parseInt(window.getComputedStyle(canvasBox).width);
      const height = parseInt(window.getComputedStyle(canvasBox).height);
      // 宽高 * 2 并放大 2 倍 是为了防止图片模糊
      canvas.width = width * 2.2;
      canvas.height = height * 2.2;
      canvas.style.width = width + "px";
      canvas.style.height = height + "px";
      const context = canvas.getContext("2d");
      context.scale(2, 2);
      const options = {
        backgroundColor: null,
        canvas: canvas,
        useCORS: true,
      };
      html2canvas(canvasBox, options).then((canvas) => {
        // toDataURL 图片格式转成 base64
        let dataURL = canvas.toDataURL("image/png");
        // this.downloadImage(dataURL)
        this.tmpFile = this.base64toFile(dataURL);
      });
    },
    base64toFile(dataurl) {
      let arr = dataurl.split(",");
      let mime = arr[0].match(/:(.*?);/)[1];
      let suffix = mime.split("/")[1];
      let bstr = atob(arr[1]);
      let n = bstr.length;
      let u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], `undifined.${suffix}`, {
        type: mime,
      });
    },
    removeImg() {
      this.isShow = false;
    },
  },
};
</script>
<style  scoped lang="less">
.button-dalod {
  position: absolute;
  top: 55vh;
  z-index: 1;
  width: 100px;
}
.input_style {
  font-size: 18px;
  font-weight: 600;
  font-family: Microsoft JhengHei UI, sans-serif;
  margin-bottom: 10px;
}
.choose-item {
  font-size: 25px;
}
.img-index {
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  flex-wrap: wrap;
}
.index-number {
  font-family: Yu Gothic Medium;
  font-style: oblique;
  font-size: 30px;

}
.img-infor {
  text-align: center;
  font-size: 25px;
  margin-top: 5px;
  margin-bottom: 10px;
  width: 256px;
  height: 30px;
  font-weight: 500;
  font-family: Microsoft JhengHei UI, sans-serif;
}
.custom-pic{
  width: 256px;
  height: 256px;
}
.upload-fun-select{
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex-wrap: wrap;
}
.model-select{
  margin-top: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>