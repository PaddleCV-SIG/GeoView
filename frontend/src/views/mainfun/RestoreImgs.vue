<template>
  <div class="bigbox">
    <Tabinfor>
      <template #left>
        <div
          id="subtitle"
          style="font-size: 25px"
        >
          图像复原<i
            class="iconfont icon-dianji"
            style="font-size: 23px; margin-left: 17px; color: blue"
          />
        </div>
      </template>
      <template #mid />
      <template #right />
    </Tabinfor>
    <el-divider />
    <Tabinfor>
      <template #left>
        <p>
          请上传包含<span class="goweight">图片的文件夹</span><i
            class="iconfont icon-wenjianjia"
            style="color: blue"
          />或者<span
            class="goweight"
          >图片</span><i
            class="iconfont icon-tupiantianjia"
            style="color: skyblue"
          />
        </p>
      </template>
    </Tabinfor>
    <el-row
      type="flex"
      justify="center"
    >
      <el-col :span="24">
        <el-card style="border: 4px dashed var(--el-border-color)">
          <div
            v-if="fileList.length"
            class="clearQ"
          >
            <el-button
              type="primary"
              class="btn-animate2 btn-animate__surround"
              @click="clearQue"
            >
              清空图片
            </el-button>
          </div>
          <el-upload
            id="one "
            ref="upload"
            v-model:file-list="fileList"
            class="upload-demo imgcard"
            drag
            action="#"
            multiple
            :auto-upload="false"
            @change="beforeUpload(fileList[fileList.length - 1].raw)"
          >
            <i class="iconfont icon-yunduanshangchuan" />
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <div

              class="el-upload__tip"
            >
              只能上传一张或多张图片，请在下方上传文件夹
            </div>
          </el-upload>
          <el-row justify="center">
            <input
              id="ctrl"
              ref="myfile"
              type="file"
              webkitdirectory
              directory
              multiple
              @change="uploadMore()"
            >
            <i
              class="iconfont icon-wenjianshangchuan"
              @click="fileClick"
            >上传文件夹</i>
          </el-row>

          <el-row justify="center">
            <p>
              <label class="mylabel container">
                <input
                  ref="cut"
                  type="checkbox"
                  class="myinput"
                  @change="select()"
                >
                <span class="checkmark" />
                <span class="goweight label-words">上传时编辑图片</span><i
                  class="iconfont icon-crop-full"
                  style="margin-left: 10px; color: rgb(64, 158, 255)"
                />
              </label>
            </p>
          </el-row>

          <div style="text-align: center; margin-top: 12px">
            <el-button
              type="primary"
              class="btn-animate btn-animate__shiny"
              style="margin: 0 auto"
              @click="upload('图像复原')"
            >
              开始处理
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <Tabinfor>
      <template #left>
        <div
          id="subtitle"
          style="font-size: 25px"
        >
          结果图预览<i
            class="iconfont icon-dianji"
            style="font-size: 23px; margin-left: 17px; color: blue"
          />
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <Tabinfor>
      <template #left>
        <p>
          <span class="goweight">点击图片</span>即可预览
          <i
            class="iconfont icon-duigou"
            style="color: green; margin-right: 20px"
          />
          <span><span class="goweight">滑轮滚动</span>即可放大缩小</span>
        </p>
      </template>

      <template #right>
        <span class="goweight"><i
          class="iconfont icon-shuaxin"
          style="padding-right:55px"
          @click="getMore"
        ><span class="hidden-sm-and-down">点击刷新</span></i></span>
      </template>
    </Tabinfor>
    <el-dialog
      v-model="cutVisible"
      :modal="false"
      title="编辑"
      width="75%"
      top="0"
    >
      <MyVueCropper
        :fileimg="fileimg"
        :funtype="funtype"
        :file="file"
        :length="afterImg.length"
        :child_prehandle="uploadSrc.prehandle"
        :child_denoise="uploadSrc.denoise"
        @cut-changed="notvisible"
        @child-refresh="getMore"
      />
    </el-dialog>

    <el-card>
      <el-row
        justify="center"
        :gutter="20"
      >
        <el-col
          :xs="22"
          :sm="22"
          :md="22"
          :lg="22"
          :xl="22"
          class="restore-img"
        >
          <el-empty
            v-if="!isUpload"
            :image-size="300"
          />
          <div
            v-else
            id="image-slider"
            @mousemove="sliderMouseMove"
            @mousedown="sliderMouseDown"
            @mouseup="sliderMouseUp"
            @mouseleave="sliderMouseLeave"
          >
            <img
              :src="beforeList[currentIndex]"
              alt=""
            >
            <div class="img-wrapper">
              <img
                :src="afterList[currentIndex]"
                alt=""
              >
            </div>
            <div class="handle">
              <div class="handle-line" />
              <div class="handle-circle">
                &#171;&#187;
              </div>
              <div class="handle-line" />
            </div>
          </div>
          <div class="choose-restore">
            <el-divider style="margin-top:0" />
            <div class="style-title">
              选择图片
            </div>

            <el-empty
              v-if="beforeImg.length === 0"
              :image-size="100"
            />
            <div
              v-for="(item, index) in Math.ceil(beforeImg.length / 5)"
              :key="index"
              class="list"
            >
              <div
                class="list-number"
                @click="goShowThese(index)"
              >
                {{ 5 * index + 1 }}-----{{ 5 * (index + 1) }}
              </div>
            </div>
            <div
              v-show="beforeImg.length !== 0"
              style="text-align:center"
            >
              下载此图片：<el-button
                v-if="isUpload"
                type="primary"
                style="width:60px"
                class="btn-animate btn-animate__shiny"
                @click="
                  downloadimgWithWords(
                    idList[currentIndex],
                    afterList[currentIndex],
                    `图像复原结果图.png`
                  )
                "
              >
                下载
              </el-button>
              <p
                v-if="isUpload"
                style="text-align:center"
              >
                <span> <i
                  class="iconfont icon-dabaoxiazai"
                  @click="goCompress('图像复原')"
                >所有结果图打包</i></span>
              </p>
            </div>
          </div>
        </el-col>
      </el-row>
      <el-row class="swiper-img">
        <div
          v-for="(item, index) in 5"
          :key="index"
          class="img-box"
        >
          <el-image
            v-if="isExist[index]"
            :src="showingList[index]"
            :class="{'render-border':onRender===index}"
            @click="goShowThis(index)"
          />
        </div>
      </el-row>
    </el-card>
    <Bottominfor />
  </div>
</template>
<script>
import { showFullScreenLoading, hideFullScreenLoading } from "@/utils/loading";
import {createSrc, restoreImgsUpload} from "@/api/upload";
import { historyGetPage } from "@/api/history";
import { getUploadImg, upload ,goCompress} from "@/utils/getUploadImg";
import { getImgArrayBuffer, atchDownload, downloadimgWithWords } from "@/utils/download.js";


import Tabinfor from "@/components/Tabinfor";
import Bottominfor from "@/components/Bottominfor";
import MyVueCropper from "@/components/MyVueCropper";

export default {
  name: "Restoreimgs",
  components: {
    Tabinfor,
    Bottominfor,
    MyVueCropper,
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      document.querySelector(".el-main").scrollTop = 0;
    });
  },
  data() {
    return {
      isUpload:true,
      canUpload:true,
      before:[],
      before1:[],
      radio: 0,
      fileimg: "",
      file: {},
      isNotCut: true,
      cutVisible: false,
      funtype: "图像复原",
      scrollTop: "",
      Loading: true,
      imgArr: [],
      scrollContainer: HTMLCollection,
      fit: "fill",
      wrapperElem: null,

      beforeImg: [],
      beforeList:[],
      afterList:[],
      afterImg: [],

      fileList: [],
      uploadSrc: {
        list: [],
      },

      isSliderLocked: false,

      isExist: [],
      onRender: 0,
      showingList:[],
      currentIndex:0,
      currentQroup:0,
      idList:[]
    };
  },
  watch:{
    uploadSrc:{
      handler(newVal,oldVal){
        this.uploadSrc = newVal
      },
      deep:true,
      immediate:true
    }
  },
  created() {
    this.getUploadImg("图像复原");
  },
  methods: {
    restoreImgsUpload,
    historyGetPage,
    createSrc,
    getUploadImg,
    upload,
    downloadimgWithWords,
    getImgArrayBuffer,
    atchDownload,
    goCompress,
    checkUpload() {
      if (this.beforeImg.length === 0) {
        this.isUpload = false;
      }else{
        this.isUpload = true
      }
    },
    clearQue() {
      this.fileList = [];
      this.$message.success("清除成功");
    },
    notvisible() {
      this.cutVisible = false;
      this.fileList = [];
    },
    getMore() {
      this.getUploadImg("图像复原");
    },
    uploadMore() {
      this.beforeUpload(...this.$refs.myfile.files)
      if(this.canUpload){
        this.fileList.push(...this.$refs.myfile.files);
      }else{
        setTimeout(() => {
          this.$message.error('检测到您上传的文件夹内存在不符合规范的图片类型')
        }, 1000);

      }
    },
    fileClick() {
      document.querySelector("#ctrl").click();
    },
    beforeUpload(file) {
      if (this.$refs.cut.checked) {
        this.cutVisible = true;
      } else {
        this.cutVisible = false;
      }
      const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1)
      const whiteList = ['jpg','jpeg','png','JPG','JPEG']
      if (whiteList.indexOf(fileSuffix) === -1) {
        this.$message.error("上传只能是 jpg,jpeg,png,JPG,JPEG格式,请重新上传");
        this.fileList= []
        this.canUpload = false
        this.cutVisible = false;
      }
      else{
        this.canUpload = true
        let data = window.URL.createObjectURL(new Blob([file]));
        this.fileimg = data;}
    },
    select() {
      if (this.$refs.cut.checked) {
        this.isNotCut = true;
      } else {
        this.isNotCut = false;
      }
    },
    checkExist(val) {
      this.isExist = val.map((item) => {
        if (typeof item == "undefined") {
          return false;
        } else return true;
      });
    },
    goShowThis(index) {
      this.currentIndex = this.currentQroup;
      this.currentIndex += index;
      this.onRender = index
    },
    goShowThese(index) {
      this.currentQroup = 5 * index;
      this.currentIndex = 5 * index;
      this.showingList = []

      for (let i = 0; i <= 4; i++) {
        this.showingList.push(this.afterList[this.currentIndex++]);
      }
      this.checkExist(this.showingList);
      this.goShowThis(0)
    },
    setNormalWay(){},
    sliderMouseMove(event) {
      const slider = document.querySelector("#image-slider");
      const wrapper = document.querySelector(".img-wrapper");
      const handle = document.querySelector(".handle");

      if (this.isSliderLocked) return;

      const sliderLeftX = slider.offsetLeft;

      const sliderWidth = slider.clientWidth;

      const sliderHandleWidth = handle.clientWidth;

      let mouseX = event.clientX - sliderLeftX;

      if (mouseX < 0) mouseX = 0;
      else if (mouseX > sliderWidth) mouseX = sliderWidth;

      wrapper.style.width = `${((1 - mouseX / sliderWidth) * 100).toFixed(4)}%`;

      handle.style.left = `calc(${((mouseX/ sliderWidth) * 100).toFixed(
          4
      )}% - ${sliderHandleWidth / 2}px)`;

    },
    sliderMouseDown() {
      if (this.isSliderLocked) this.isSliderLocked = false;
      this.sliderMouseMove(event);
    },
    sliderMouseUp() {
      if (!this.isSliderLocked) this.isSliderLocked = true;
    },
    sliderMouseLeave() {
      if (this.isSliderLocked) this.isSliderLocked = true;
    },
  },
}
</script>

<style lang="less" scoped>
* {
  font-family: SimHei sans-serif;
}
.imgInfor {
  text-align: center;
  margin-bottom: 20px;
}
.imgcard {
  text-align: center;
}
.el-upload-dragger {
  border: 3px dashed var(--el-border-color);
  height: 180px;
  margin-top: 10px;
}
#subtitle:hover:after {
  left: 0%;
  right: 0%;
  width: 220px;
}
#ctrl {
  display: none;
}
.icon-wenjianshangchuan {
  font-size: 20px;
  margin-bottom: 20px;
  margin-top: 20px;
  transition: all 0.5s;
  color: rgb(64, 158, 255);
}
.icon-wenjianshangchuan:hover {
  color: rgb(64, 158, 255);
  transform: scale(1.2);
}
.icon-shuaxin {
  transition: all 0.5s;
}
.icon-shuaxin:hover {
  color: rgb(64, 158, 255);
}
.mylabel {
  margin-right: 10px;
}
.clearQ {
  position: relative;
  left: -20px;
  top: 14%;
  z-index: 100;
}
.his-words {
  margin-top: 15px;
  margin-bottom: 10px;
  font-size: 22px;
  text-align: center;
  font-weight: 600;
  font-family: Microsoft JhengHei UI, sans-serif;
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
  margin-left: 5px;
  margin-right: 10px;
}
.img-infor {
  text-align: center;
  font-size: 18px;
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

#image-slider {
  position: relative;
  max-width:600px;

  overflow: hidden;
  border-radius: 1em;
  // box-shadow: -4px 5px 10px 1px gray;
  cursor: col-resize;
  display: inline-block;
}

#image-slider img {
  display: block;
  height: 100%;
  width:580px;
  height:580px;
  object-fit: cover;
  pointer-events: none;
  user-select: none;
}

#image-slider .img-wrapper {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  width: 50%;
  overflow: hidden;
  z-index: 1;
}

#image-slider .img-wrapper img {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
}

#image-slider .handle {
  border: 0 solid red;
  position: absolute;
  top: 0;
  left: calc(50% - var(--image-slider-handle-width) / 2);
  width: var(--image-slider-handle-width);
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  user-select: none;
  z-index: 2;
}

#image-slider .handle-circle {

  color: white;
  border: 2px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
}

#image-slider .handle-line {
  width: 2px;
  flex-grow: 1;
  background: white;
}

.el-row{
  position: inherit;
  //获取滑窗容器的左偏移量
}
.restore-img{
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  flex-wrap: wrap;
}
.style-title {
  text-align: center;
  font-size: 22px;
  font-family: "幼圆", sans-serif;
  font-weight: 600;
  margin-bottom: 20px;
}
.list {
  text-align: center;
  cursor: pointer;
  width: auto;
  height: 20px;
  background-color: rgb(236, 244, 255);
  position: relative;
  margin-bottom: 10px;
}
.list-number:hover::after {
  width: 100%;
  background: rgb(64, 158, 255);
}
.list-number::after {
  position: absolute;
  content: "";
  width: 0;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 2px 2px 0 0;
  transition: 0.4s;
  z-index: -1;
}
.list:hover * {
  color: #ecf4ff !important;
}
.list-number {
  z-index: 1;
}
.list-number {
  overflow: hidden;
  margin: 0 auto;
  width: auto;
  height: 20px;
  position: relative !important;
  border-radius: 2px !important;
}
.choose-restore{
  width: 250px;
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  justify-content:center;
}
.swiper-img {
  width: 100%;
  margin-top: 30px;
  overflow: hidden;
  position: relative;
  max-height: 280px;
  min-height: 240px;
  .swiper-lbtn {
    opacity: 0.6;
    left: 0;
    height: 100%;
    z-index: 100;
    position: absolute;
  }

  .img-box {
    flex: 1;
    height: 100%;
    overflow: hidden;
    opacity: 0.7;
    transition: all 0.6s;
    margin-right: 10px;
    justify-content: space-between;
  }
}
.render-border {
  border: rgb(64, 158, 255) 0.5rem solid;
}
</style>