<template>
  <div class="bigbox">
    <Tabinfor>
      <template #left>
        <div
          id="subtitle"
          style="font-size: 25px"
        >
          目标检测<i
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
          <el-row
            justify="center"
            align="middle"
          >
            <i
              class="iconfont icon-tuxingtuxiangchuli"
              style="color: rgb(64, 158, 255); font-size: 20px"
            />
            <p>图像预处理：</p>
            <p>
              <label class="mylabel container">
                <input
                  ref="clahe"
                  type="checkbox"
                  class="myinput"
                  @change="selectClahe(2)"
                >
                <span class="checkmark" />
                <span class="goweight label-words">CLAHE</span>
              </label>
            </p>
            <p>
              <label class="mylabel container">
                <input
                  ref="sharpen"
                  type="checkbox"
                  class="myinput"
                  @change="selectSharpen(2)"
                >
                <span class="checkmark" />
                <span class="goweight label-words">锐化</span>
              </label>
            </p>
          </el-row>
          <el-row
            justify="center"
            align="middle"
          >
            <i
              class="iconfont icon-agora_AIjiangzao"
              style="color: rgb(64, 158, 255); font-size: 35px"
            />
            <p>降噪处理：</p>
            <p>
              <label class="mylabel container">
                <input
                  ref="smooth"
                  type="checkbox"
                  class="myinput"
                  @change="selectSmooth()"
                >
                <span class="checkmark" />
                <span class="goweight label-words">平滑</span>
              </label>
              <label class="mylabel container">
                <input
                  ref="filter"
                  type="checkbox"
                  class="myinput"
                  @change="selectFilter()"
                >
                <span class="checkmark" />
                <span class="goweight label-words">滤波</span>
              </label>
            </p>
          </el-row>

          <div style="text-align: center; margin-top: 12px">
            <el-button
              type="primary"
              class="btn-animate btn-animate__shiny"
              style="margin: 0 auto"
              @click="upload('目标检测')"
            >
              开始处理
            </el-button>
          </div>
          <el-divider v-if="!uploadSrc.prehandle" />
          <div v-if="uploadSrc.prehandle">
            <template v-if="uploadSrc.prehandle===2">
              <div
                id="subtitle"
                style="font-size: 25px"
              >
                CLAHE处理结果预览<i
                  class="iconfont icon-dianji"
                  style="font-size: 23px; margin-left: 17px; color: blue"
                />
              </div>   
            </template>
            <tempalte v-else-if="uploadSrc.prehandle===4">
              <div
                id="subtitle"
                style="font-size: 25px"
              >
                锐化处理结果预览<i
                  class="iconfont icon-dianji"
                  style="font-size: 23px; margin-left: 17px; color: blue"
                />
              </div>   
            </tempalte>
            <el-divider />
            <el-row
              justify="center"
              :gutter="20"
            >
              <el-col
                :xs="24"
                :sm="24"
                :md="6"
                :lg="6"
                :xl="6"
              >
                <div
                  v-for="(index,item) in before"
                  :key="index"
                >
                  <el-image
                    :src="item"
                    :preview-src-list="[item]"
                    :preview-teleported="true"
                  /><div class="his-words">
                    原图
                  </div>
                </div>
              </el-col>
              <el-col
                :md="2"
                :lg="2"
                :xl="2"
              />
              <el-col
                v-if="uploadSrc.prehandle===2"
                :xs="24"
                :sm="24"
                :md="6"
                :lg="6"
                :xl="6"
              >
                <div
                  v-for="(index,item) in claheImg"
                  :key="index"
                >
                  <el-image
                    :src="item"
                    :preview-src-list="[item]"
                    :preview-teleported="true"
                  /><div class="his-words">
                    CLAHE处理后       <span
                      @click="
                        downloadimgWithWords(
                          -1,
                          item,
                          `CLAHE处理图.png`
                        )
                      "
                    ><i class="iconfont icon-xiazai" /></span>
                  </div>
                </div>
              </el-col>
              <el-col
                v-if="uploadSrc.prehandle===4"
                :xs="24"
                :sm="24"
                :md="6"
                :lg="6"
                :xl="6"
              >
                <div
                  v-for="(index,item) in sharpenImg"
                  :key="index"
                >
                  <el-image
                    :src="item"
                    :preview-src-list="[item]"
                    :preview-teleported="true"
                  /><div class="his-words">
                    锐化处理后      <span
                      @click="
                        downloadimgWithWords(
                          -1,
                          item,
                          `锐化处理图.png`
                        )
                      "
                    ><i class="iconfont icon-xiazai" /></span>
                  </div>
                </div>
              </el-col>
            </el-row>
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
      <template #mid>
        <p v-if="isUpload">
          <i
            class="iconfont icon-dabaoxiazai"
            @click="goCompress('目标检测')"
          >结果图打包</i>
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
        :prehandle="uploadSrc.prehandle"
        :denoise="uploadSrc.denoise"
        @cutChanged="notvisible"
      />
    </el-dialog>
    <ImgShow
      :before-img="beforeImg"
      :after-img="afterImg"
      :funtype="funtype"
    />
    <Bottominfor />
  </div>
</template>
<script>
import { showFullScreenLoading, hideFullScreenLoading } from "@/utils/loading";
import { getImgArrayBuffer, atchDownload, downloadimgWithWords } from "@/utils/download.js";
import { createSrc, detectTargetsUpload } from "@/api/upload";
import { historyGetPage } from "@/api/history";
import { getUploadImg, upload, goCompress } from "@/utils/getUploadImg";
import {
  selectSharpen,
  selectFilter,
  selectSmooth,
  selectClahe,
} from "@/utils/preHandle";
import ImgShow from "@/components/ImgShow";
import Tabinfor from "@/components/Tabinfor";
import Bottominfor from "@/components/Bottominfor";
import MyVueCropper from "@/components/MyVueCropper";

export default {
  name: "Detecttargets",
  components: {
    ImgShow,
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
       claheImg:[],
      sharpenImg:[],
      before:[],
      before1:[],
      lava: [],
      desert: [],
      field: [],
      ocean: [],
      radio: 0,
      fileimg: "",
      file: {},
      isNotCut: true,
      cutVisible: false,
      funtype: "目标检测",
      scrollTop: "",
      Loading: true,
      imgArr: [],
      scrollContainer: HTMLCollection,
      fit: "fill",
      wrapperElem: null,
      beforeImg: [],
      afterImg: [],
      fileList: [],
      uploadSrc: {
        list: [],
        prehandle: 0,
        denoise: 0,
      },
         prePhoto:{
        list:[],
        prehandle:0,
        type:4
      }
    };
  },
  created() {
    this.getUploadImg("目标检测");
  },
  methods: {
    getImgArrayBuffer,
    atchDownload,
     downloadimgWithWords,
    detectTargetsUpload,
    historyGetPage,
    createSrc,
    getUploadImg,
    upload,
    goCompress,
    selectSharpen,
    selectFilter,
    selectSmooth,
    selectClahe,
    checkUpload() {
      if (this.afterImg.length === 0) {
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
      this.getUploadImg("目标检测");
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
    goRenderThis() {},
    goRenderThese() {},
 
    setNormalWay(){}
  },
};
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
  position: absolute;
  left: 5px;
  top: 10%;
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
</style>
