<template>
  <div class="bigbox">
    <Tabinfor>
      <template #left>
        <div
          id="subtitle"
          style="font-size: 25px"
        >
          场景分类<i
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
              @click="upload('场景分类')"
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
      />
    </el-dialog>

    <el-row>
      <el-col>
        <el-card style="margin-bottom: 10px">
          <el-empty
            v-if="beforeImg.length === 0"
            :image-size="200"
          />
          <el-row
            :gutter="10"
            justify="center"
          >
            <el-col
              :lg="5"
              :xl="5"
            >
              <div
                v-for="(item,index) in scene"
                :key="index"
                class="img-index hidden-sm-and-down"
                :style="{ height: 301 + 'px' }"
              >
                <div>第<span class="index-number">{{ index + 1 }}</span>组</div>
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
                v-for="(item, index) in beforeList"
                :key="index"
                style="position: relative;"
              >
                <el-image
                  ref="tableTab"
                  :src="beforeList[index]"
                  :fit="fit"
                  :lazy="true"
                  class="gobig custom-pic"
                  :preview-src-list="[beforeList[index]]"
                  :preview-teleported="true"
                />

                <div class="img-infor">
                  <span>原图</span>
                </div>
                <span class="index-number hidden-md-and-up">{{ sceneKey[index][0] }}:<span>{{ scene[index][sceneKey[index][0]] }}</span></span>
              </div>
            </el-col>
            <el-col
              :lg="5"
              :xl="5"
            >
              <div
                v-for="(item,index) in scene"
                :key="index"
                class="img-index hidden-sm-and-down"
                :style="{ height: 301 + 'px' }"
              >
                <span class="index-number ">{{ Object.keys(item)[0] }}:{{ item[Object.keys(item)[0]] }}</span>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    
    <Bottominfor />
  </div>
</template>
<script>
import { showFullScreenLoading, hideFullScreenLoading } from "@/utils/loading";
import { createSrc, sceneClassifyUpload } from "@/api/upload";
import { historyGetPage } from "@/api/history";
import { getUploadImg, upload } from "@/utils/getUploadImg";


import Tabinfor from "@/components/Tabinfor";
import Bottominfor from "@/components/Bottominfor";
import MyVueCropper from "@/components/MyVueCropper";

export default {
  name: "Classifyscene",
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
      funtype: "场景分类",
      scrollTop: "",
      Loading: true,
      imgArr: [],
      scrollContainer: HTMLCollection,
      fit: "fill",
      wrapperElem: null,
      beforeImg: [],
      beforeList:[],
      afterList:[],   //未使用到，防止在getUploadImg.js里报错
      afterImg: [],
      fileList: [],
      uploadSrc: {
        list: [],
      },
      //场景键值对数组,[{'a':0.8},{},{}]
      scene:[],
      //构成场景键数组的数组，[['a'],['b'],['c']]
      sceneKey:[],
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
    this.getUploadImg("场景分类");
  },
  methods: {
    sceneClassifyUpload,
    historyGetPage,
    createSrc,
    getUploadImg,
    upload,
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
      this.getUploadImg("场景分类");
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
</style>
