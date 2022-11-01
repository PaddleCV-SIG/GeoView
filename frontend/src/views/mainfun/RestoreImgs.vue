<template>
  <div>
    <Tabinfor>
      <template #left>
        <div
          id="sub-title"
        >
          图像复原<i
            class="iconfont icon-dianji"
          />
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <p>
      请上传包含<span class="go-bold">图片的文件夹</span><i class="iconfont icon-wenjianjia" />或者<span
        class="go-bold"
      >图片</span><i class="iconfont icon-tupiantianjia" />，<i class="iconfont icon-zidingyi" />自定义模型文件请上传至<span class="go-bold">backend/model文件夹</span><i class="iconfont icon-wenjianjia" />下的<span class="go-bold">image_restoration文件夹</span>
    </p>
    <el-row
      type="flex"
      justify="center"
    >
      <el-col :span="24">
        <el-card style="border: 4px dashed var(--el-border-color)">
          <div
            v-if="fileList.length"
            class="clear-queue"
          >
            <el-button
              type="primary"
              class="btn-animate2 btn-animate__surround"
              @click="clearQueue"
            >
              清空图片
            </el-button>
          </div>
          <el-upload
            ref="upload"
            v-model:file-list="fileList"
            class="upload-card"
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
              id="folder"
              ref="uploadFile"
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
              <label class="prehandle-label container">
                <input
                  ref="cut"
                  type="checkbox"
                  @change="select()"
                >
                <span class="checkmark" />
                <span class="go-bold label-words">上传时编辑图片</span><i
                  class="iconfont icon-crop-full"
                />
              </label>
            </p>
          </el-row>
          <el-row justify="center">
            <div class="custom-model">
              可选训练模型：
              <span v-if="modelPathArr.length===0">未检测到模型文件，请查看上传目录是否有误</span>
              <el-radio
                v-for="(item,index) in modelPathArr"
                :key="index"
                v-model="uploadSrc.model_path"
                class="choose-item"
                :label="item.model_path"
              >
                {{ item.model_name }}
              </el-radio>
            </div>
          </el-row>
          <div class="handle-button">
            <el-button
              type="primary"
              class="btn-animate btn-animate__shiny"
              @click="upload('图像复原','image_restoration')"
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
          id="sub-title"
        >
          结果图预览<i
            class="iconfont icon-dianji"
          />
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <Tabinfor>
      <template #left>
        <p>
          <span class="go-bold">点击图片</span>即可预览
          <i
            class="iconfont icon-duigou"
          />
          <span><span class="go-bold">滑轮滚动</span>即可放大缩小</span>
        </p>
      </template>

      <template #right>
        <span class="go-bold"><i
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
        :child_prehandle="uploadSrc.prehandle"
        :child_denoise="uploadSrc.denoise"
        :child-model-path="uploadSrc.model_path"
        @cut-changed="notvisible"
        @child-refresh="getMore"
      />
    </el-dialog>

    <el-card>
      <div
        class="restore-img-box"
      >
        <div>
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
              :src="imgArr[currentIndex]?.before_img"
              alt=""
            >
            <div class="img-wrapper">
              <img
                :src="imgArr[currentIndex]?.after_img"
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
        </div>
        <div class="choose-restore">
          <el-divider style="margin-top:0" />
          <div class="style-title">
            选择图片
          </div>
          <el-empty
            v-if="!isUpload"
            :image-size="100"
          />
          <div v-else>
            <div
              v-for="(item, index) in Math.ceil(imgArr.length / 5)"
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
              style="text-align:center"
            >
              下载此图片：<el-button
                type="primary"
                style="width:60px"
                class="btn-animate btn-animate__shiny"
                @click="
                  downloadimgWithWords(
                    imgArr[currentIndex].id,
                    imgArr[currentIndex].after_img,
                    `图像复原结果图.png`
                  )
                "
              >
                下载
              </el-button>
              <p
                style="text-align:center"
              >
                <span> <i
                  class="iconfont icon-dabaoxiazai"
                  @click="goCompress('图像复原')"
                >所有结果图打包</i></span>
              </p>
            </div>
          </div>
        </div>
      </div>
      <el-row class="swiper-img">
        <div
          v-for="(item, index) in 5"
          :key="index"
          class="img-box"
        >
          <el-image
            v-if="imgArr[currentQroup+index]?.after_img"
            :src="imgArr[currentQroup+index]?.after_img"
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
import {createSrc,imgUpload,getCustomModel} from "@/api/upload";
import {historyGetPage} from "@/api/history";
import {getUploadImg, goCompress, upload} from "@/utils/getUploadImg";
import {atchDownload, downloadimgWithWords, getImgArrayBuffer} from "@/utils/download.js";
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
      canUpload:true,
      fileimg: "",
      file: {},
      isNotCut: true,
      cutVisible: false,
      funtype: "图像复原",
      scrollTop: "",
      fit: "fill",
      fileList: [],
      uploadSrc: {
        list: [],
        model_path:''
      },
      modelPathArr:[],
      isSliderLocked: false,
      onRender: 0,
      currentIndex:0,
      currentQroup:0,
      imgArr:[],
      isUpload:false
    };
  },
  watch:{
    uploadSrc:{
      handler(newVal,oldVal){
        this.uploadSrc = newVal
      },
      deep:true,
      immediate:true
    },
    isUpload:{
      handler(newVal, oldVal) {
        this.isUpload = newVal
      }
    }
  },
  created() {
    this.getUploadImg("图像复原")
    this.getCustomModel('image_restoration').then((res)=>{
      this.modelPathArr = res.data.data
      this.uploadSrc.model_path = this.modelPathArr[0]?.model_path
    }).catch((rej)=>{})
  },
  methods: {
    imgUpload,
    getCustomModel,
    historyGetPage,
    createSrc,
    getUploadImg,
    upload,
    downloadimgWithWords,
    getImgArrayBuffer,
    atchDownload,
    goCompress,
    clearQueue() {
      this.fileList = [];
      this.$message.success("清除成功");
    },
    notvisible() {
      this.cutVisible = false;
      this.fileList = [];
    },
    getMore() {
      this.getUploadImg("图像复原");
      this.goShowThese(0)
      console.log(this.imgArr.length)
    },
    uploadMore() {
      this.beforeUpload(...this.$refs.uploadFile.files)
      if(this.canUpload){
        this.fileList.push(...this.$refs.uploadFile.files);
      }else{
        setTimeout(() => {
          this.$message.error('检测到您上传的文件夹内存在不符合规范的图片类型')
        }, 1000);
      }
    },
    fileClick() {
      document.querySelector("#folder").click();
    },
    beforeUpload(file) {
      this.cutVisible = this.$refs.cut.checked;
      const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1)
      const whiteList = ['jpg','jpeg','png','JPG','JPEG']
      if (whiteList.indexOf(fileSuffix) === -1) {
        this.$message.error("只允许上传jpg, jpeg, png, JPG, 或JPEG格式,请重新上传");
        this.fileList= []
        this.canUpload = false
        this.cutVisible = false;
      }
      else{
        this.canUpload = true
        this.fileimg = window.URL.createObjectURL(new Blob([file]));
      }
    },
    select() {
      this.isNotCut = this.$refs.cut.checked;
    },
    goShowThis(index) {
      this.currentIndex = this.currentQroup;
      this.currentIndex += index;
      this.onRender = index
    },
    goShowThese(index) {
      this.currentQroup = 5 * index;
      this.currentIndex = 5 * index;
      this.goShowThis(0)
    },
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
#sub-title{
  font-size: 25px;
}
#sub-title:hover:after {
  left: 0%;
  right: 0%;
  width: 220px;
}
.clear-queue {
  position: relative;
  left: -20px;
  top: 14%;
  z-index: 100;
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
  cursor: col-resize;
  display: inline-block;
}

#image-slider img {
  display: block;
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

//.el-row{
//  position: inherit;
//  //获取滑窗容器的左偏移量
//}
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

.swiper-img {
  display: flex;
  flex-wrap: nowrap;
  flex-direction: row;
  width: 100%;
  margin-top: 30px;
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
  border: var(--theme--color) 0.5rem solid;
}
.el-radio /deep/{
  height: 62px;
}
.restore-img-box{
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  flex-direction: row;
  .choose-restore{
    width: 250px;
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    justify-content:center;
  }
}
</style>