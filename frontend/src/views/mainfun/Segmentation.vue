<template>
  <div>
    <Tabinfor>
      <template #left>
        <div id="sub-title">
          地物分类<i class="iconfont icon-dianji" />
        </div>
      </template>
    </Tabinfor>
    <el-divider />

    <p>
      请上传包含<span class="go-bold">图片的文件夹</span><i class="iconfont icon-wenjianjia" />或者<span
        class="go-bold"
      >图片</span><i class="iconfont icon-tupiantianjia" />，<i class="iconfont icon-zidingyi" />自定义模型文件请上传至<span class="go-bold">backend/model文件夹</span><i class="iconfont icon-wenjianjia" />下的<span class="go-bold">semantic_segmentation文件夹</span>
    </p>

    <el-row
      type="flex"
      justify="space-evenly"
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
            accpet=".jpg,.jpeg,.png,.JPG,.JPEG"
            :auto-upload="false"
            @change="beforeUpload(fileList[fileList.length - 1].raw)"
          >
            <i class="iconfont icon-yunduanshangchuan" />
            <div class="el-upload__text">
              将图片拖到此处，或<em>点击上传</em>
            </div>
            <div class="el-upload__tip">
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
          <el-row
            justify="center"
            align="middle"
          >
            <i
              class="iconfont icon-tuxingtuxiangchuli"
            />
            <p>图像增强：</p>
            <p>
              <label class="prehandle-label container">
                <input
                  ref="clahe"
                  type="checkbox"

                  @change="selectClahe(4)"
                >
                <span class="checkmark" />
                <span class="go-bold label-words">CLAHE</span>
              </label>
            </p>
            <p>
              <label class="prehandle-label container">
                <input
                  ref="sharpen"
                  type="checkbox"

                  @change="selectSharpen(4)"
                >
                <span class="checkmark" />
                <span class="go-bold label-words">锐化</span>
              </label>
            </p>
          </el-row>
          <el-row
            justify="center"
            align="middle"
          >
            <i
              class="iconfont icon-agora_AIjiangzao"
            />
            <p>降噪处理：</p>
            <p>
              <label class="prehandle-label container">
                <input
                  ref="smooth"
                  type="checkbox"

                  @change="selectSmooth()"
                >
                <span class="checkmark" />
                <span class="go-bold label-words">平滑</span>
              </label>
              <label class="prehandle-label container">
                <input
                  ref="filter"
                  type="checkbox"

                  @change="selectFilter()"
                >
                <span class="checkmark" />
                <span class="go-bold label-words">滤波</span>
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
              @click="upload('地物分类','semantic_segmentation')"
            >
              开始处理
            </el-button>
          </div>
          <el-divider v-if="!uploadSrc.prehandle" />
          <div v-if="uploadSrc.prehandle">
            <div v-if="uploadSrc.prehandle===2">
              <div
                id="sub-title"
              >
                CLAHE处理结果预览<i
                  class="iconfont icon-dianji"
                />
              </div>
            </div>
            <div v-else-if="uploadSrc.prehandle===4">
              <div
                id="sub-title"
              >
                锐化处理结果预览<i
                  class="iconfont icon-dianji"
                />
              </div>
            </div>
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
                  v-for="(item,index) in before"
                  :key="index"
                >
                  <el-image
                    :src="item"
                    :preview-src-list="[item]"
                    :preview-teleported="true"
                  />
                  <div class="handle-words">
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
                  v-for="(item,index) in claheImg"
                  :key="index"
                >
                  <el-image
                    :src="item"
                    :preview-src-list="[item]"
                    :preview-teleported="true"
                  />
                  <div class="handle-words">
                    CLAHE处理后 <span
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
                  v-for="(item,index) in sharpenImg"
                  :key="index"
                >
                  <el-image
                    :src="item"
                    :preview-src-list="[item]"
                    :preview-teleported="true"
                  />
                  <div class="handle-words">
                    锐化处理后 <span
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
        <div class="go-bold">
          <i
            class="iconfont icon-shuaxin"
            style="padding-right:65px"
            @click="getMore"
          ><span
            class="hidden-sm-and-down"
          >点击刷新</span></i>
        </div>
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
        :child-prehandle="uploadSrc.prehandle"
        :child-denoise="uploadSrc.denoise"
        :child-model-path="uploadSrc.model_path"
        @cut-changed="notvisible"
        @child-refresh="getMore"
      />
    </el-dialog>
    <ImgShow
      :img-arr="imgArr"
    />
    <Bottominfor />
  </div>
</template>

<script>
import { atchDownload, downloadimgWithWords, getImgArrayBuffer } from "@/utils/download.js";
import { imgUpload, createSrc ,getCustomModel } from "@/api/upload";
import { historyGetPage } from "@/api/history";
import { getUploadImg, goCompress, upload } from "@/utils/getUploadImg";
import { selectClahe, selectFilter, selectSharpen, selectSmooth, } from "@/utils/preHandle";
import ImgShow from "@/components/ImgShow";
import Tabinfor from "@/components/Tabinfor";
import Bottominfor from "@/components/Bottominfor";
import MyVueCropper from "@/components/MyVueCropper";

export default {
  name: "Segmentation",
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
      isUpload: true,
      canUpload: true,
      claheImg: [],
      sharpenImg: [],
      before: [],
      fileimg: "",
      file: {},
      isNotCut: true,
      cutVisible: false,
      fileList: [],
      funtype: "地物分类",
      scrollTop: "",
      fit: "fill",

      uploadSrc: { list: [], prehandle: 0, denoise: 0 ,model_path:''},

      modelPathArr:[],

      prePhoto: {
        list: [],
        prehandle: 0,
        type: 4
      },
      imgArr:[]
    };
  },
  watch: {
    uploadSrc: {
      handler(newVal, oldVal) {
        this.uploadSrc = newVal
      },
      deep: true,
      immediate: true
    }
  },
  created() {
    this.getUploadImg("地物分类");
    this.getCustomModel('semantic_segmentation').then(res=>{
      this.modelPathArr = res.data.data
      this.uploadSrc.model_path = this.modelPathArr[0]?.model_path
    }).catch((rej)=>{})
  },
  methods: {
    getImgArrayBuffer,
    atchDownload,
    imgUpload,
    getCustomModel,
    historyGetPage,
    createSrc,
    getUploadImg,
    upload,
    goCompress,
    selectSharpen,
    selectFilter,
    selectSmooth,
    selectClahe,
    downloadimgWithWords,
    checkUpload() {
      this.isUpload = this.afterImg.length !== 0;
    },
    clearQueue() {
      this.fileList = [];
      this.$message.success("清除成功");
    },
    notvisible() {
      this.cutVisible = false;
      this.fileList = [];
    },
    uploadMore() {
      this.beforeUpload(...this.$refs.uploadFile.files)
      if (this.canUpload) {
        this.fileList.push(...this.$refs.uploadFile.files);
      } else {
        setTimeout(() => {
          this.$message.error('检测到您上传的文件夹内存在不符合规范的图片类型')
        }, 1000);

      }
    },
    getMore() {
      this.getUploadImg("地物分类");
    },
    fileClick() {
      document.querySelector("#folder").click();
    },
    beforeUpload(file) {
      this.cutVisible = this.$refs.cut.checked;
      const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1)
      const whiteList = ['jpg', 'jpeg', 'png', 'JPG', 'JPEG']
      if (whiteList.indexOf(fileSuffix) === -1) {
        this.$message.error("只允许上传jpg, jpeg, png, JPG, 或JPEG格式,请重新上传");
        this.fileList = []
        this.cutVisible = false;
        this.canUpload = false
      }
      else {
        this.canUpload = true
        this.fileimg = window.URL.createObjectURL(new Blob([file]));
      }

    },
    select() {
      this.isNotCut = this.$refs.cut.checked;
    },
  },
};
</script>
<style lang="less" scoped>
* {
  font-family: SimHei sans-serif;
}
#sub-title {
  font-size: 25px;
}
#sub-title:hover:after {
  left: 0;
  right: 0;
  width: 220px;
}

.clear-queue {
  position: absolute;
  left: 5px;
  top: 10%;
  z-index: 100;
}

.el-radio /deep/{
  height: 62px;
}

</style>
