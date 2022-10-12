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
      <el-row justify="center">
        <el-radio
          v-model="funtype"
          class="choose-item"
          label="目标检测"
        >
          目标检测
        </el-radio>
        <el-radio
          v-model="funtype"
          class="choose-item"
          label="地物分类"
        >
          地物分类
        </el-radio>
        <el-radio
          v-model="funtype"
          class="choose-item"
          label="场景分类"
        >
          场景分类
        </el-radio>
      </el-row>
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
        v-show="funtype!=='场景分类'"
        :before-img="beforeImg"
        :after-img="afterImg"
        :funtype="funtype"
      />
      <el-row v-if="funtype==='场景分类'">
        <el-col>
          <el-card>
            <el-row
              :gutter="10"
              justify="center"
            >
              <el-col
                :lg="5"
                :xl="5"
              >
                <div
                  class="img-index hidden-sm-and-down"
                  style=" height: 301px"
                >
                  <div>第<span class="index-number">1</span>组</div>
                </div>
              </el-col>
              <el-col
                :xs="20"
                :sm="10"
                :md="6"
                :lg="6"
                :xl="6"
              >
                <div
                  style="position: relative;"
                >
                  <el-image
                    ref="tableTab"
                    :src="beforeList[0]"
                    :fit="fit"
                    :lazy="true"
                    class="custom-pic"
                    :preview-src-list="[beforeList[0]]"
                    :preview-teleported="true"
                  />

                  <div class="img-infor">
                    <span>原图</span>
                  </div>
                  <span
                    v-if="sceneKey"
                    class="index-number hidden-md-and-up"
                  >{{ sceneKey[0][0] }}:<span>{{ scene[0][sceneKey[0][0]] }}</span></span>
                </div>
              </el-col>
              <el-col
                :lg="5"
                :xl="5"
              >
                <div
                  class="img-index hidden-sm-and-down"
                  style="height:301px"
                >
                  <span
                    v-if="scene"
                    class="index-number "
                  >{{ Object.keys(scene[0])[0] }}:{{ scene[0][Object.keys(scene[0])[0]] }}</span>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
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
import {classifyUpload, createSrc, detectTargetsUpload, sceneClassifyUpload,} from "@/api/upload";
import {hideFullScreenLoading, showFullScreenLoading} from "@/utils/loading";
import {historyGetPage} from "@/api/history";

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
      uploadSrc: { list: [], prehandle: 0, denoise: 0 },
      scene:[{}],
      sceneKey:[['']]
    };
  },
  mounted() {
    // 创建Map实例
    let map = new BMap.Map("map");
    // 初始化地图,设置中心点坐标和地图级别
    map.centerAndZoom(new BMap.Point(104.07258, 30.550701), 20);
    map.setMapType(BMAP_HYBRID_MAP);
    // map.centerAndZoom：第一个参数可以是根据之前创建好的一个点为中心，创建出地图，也可以根据城市地区的中文名称创建地图。第二个参数是地图缩放级别，最大为19，最小为0
    map.addControl(
        //添加地图类型控件
        new BMap.MapTypeControl({
          mapTypes: [BMAP_SATELLITE_MAP, BMAP_HYBRID_MAP],
        })
    );
    map.setCurrentCity("北京"); // 设置地图显示的城市 此项是必须设置的
    map.enableScrollWheelZoom(true);

    this.$nextTick(function () {
      let th = this;
      // 创建Map实例
      // eslint-disable-next-line no-undef
      // let map = new BMap.Map("map");
      // // 初始化地图,设置中心点坐标，
      // // eslint-disable-next-line no-undef
      //     map.setMapType(BMAP_HYBRID_MAP);
      // let point = new BMap.Point(117.155827, 36.695916); // 创建点坐标，汉得公司的经纬度坐标
      // map.centerAndZoom(point, 15);
      // map.enableScrollWheelZoom();
      let ac = new BMap.Autocomplete({
        //建立一个自动完成的对象
        input: "suggestId",
        location: map,
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
        map.clearOverlays(); //清除地图上所有覆盖物
        function myFun() {
          th.userlocation = local.getResults().getPoi(0).point; //获取第一个智能搜索的结果
          map.centerAndZoom(th.userlocation, 18);
          // eslint-disable-next-line no-undef
          map.addOverlay(new BMap.Marker(th.userlocation)); //添加标注
          th.lng = th.userlocation.lng;
          th.lat = th.userlocation.lat;
        }

        // eslint-disable-next-line no-undef
        let local = new BMap.LocalSearch(map, {
          //智能搜索
          onSearchComplete: myFun,
        });
        local.search(myValue)
        //测试输出坐标（指的是输入框最后确定地点的经纬度）
        map.addEventListener("click", function () {
          this.lng = th.userlocation.lng;

          this.lat = th.userlocation.lat;
        });
      }
    });
  },
  methods: {
    createSrc,
    classifyUpload,
    detectTargetsUpload,
    sceneClassifyUpload,
    historyGetPage,
    goUpload(type) {
      showFullScreenLoading("#load");
      let formData = new FormData();
      formData.append("files", this.tmpFile);
      formData.append("type", type);
      this.createSrc(formData).then((res) => {
        this.uploadSrc.list = res.data.data.map((item) => {
          return item.src;
        });
        if (type === "目标检测") {
          this.uploadSrc.prehandle = 0
          this.uploadSrc.denoise = 0
          this.detectTargetsUpload(this.uploadSrc).then((res) => {
            hideFullScreenLoading("#load");
            this.$message.success("上传成功！");
            this.choose = false;
            this.historyGetPage(1, 1, "目标检测").then((res) => {
              this.beforeImg = res.data.data.map((item) => {
                return { before_img: global.BASEURL + item.before_img };
              });
              this.afterImg = res.data.data.map((item) => {
                return {
                  after_img: global.BASEURL + item.after_img,
                  id: item.id,
                };
              });
              this.isShow = true;
            });
          });
        }
        if (type === "地物分类") {
          this.uploadSrc.prehandle = 0
          this.uploadSrc.denoise = 0
          this.classifyUpload(this.uploadSrc).then((res) => {
            hideFullScreenLoading("#load");
            this.$message.success("上传成功！");
            this.choose = false;
            this.historyGetPage(1, 1, "地物分类").then((res) => {
              this.beforeImg = res.data.data.map((item) => {
                return { before_img: global.BASEURL + item.before_img };
              });
              this.afterImg = res.data.data.map((item) => {
                return {
                  after_img: global.BASEURL + item.after_img,
                  id: item.id,
                };
              });
              this.isShow = true;
            });
          });
        }
        if (type === "场景分类") {
          delete(this.uploadSrc.denoise)
          delete (this.uploadSrc.prehandle)
          this.sceneClassifyUpload(this.uploadSrc).then((res) => {
            hideFullScreenLoading("#load");
            this.$message.success("上传成功！");
            this.choose = false;
            this.historyGetPage(1, 1, "场景分类").then((res) => {
              this.beforeList=res.data.data.map((item)=>{
                return global.BASEURL + item.before_img
              })
              this.scene = res.data.data.map(item=>item.data)     //场景键值对数组,[{'a':0.8},{‘b’:0.6},{'c':0.8}]
              this.sceneKey = this.scene.map(item=>Object.keys(item))  //构成场景键数组的数组，[['a'],['b'],['c']]
              this.isShow = true;
            });
          });
        }
      });
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
<style  scoped>
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
</style>