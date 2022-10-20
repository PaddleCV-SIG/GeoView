<template>
  <div>
    <div class="cropper">
      <el-row
        align="middle"
        justify="center"
      >
        <el-col
          :xs="10"
          :sm="20"
          :md="20"
          :lg="19"
          :xl="19"
        >
          <div class="cropper-content">
            <div class="cropper">
              <vueCropper
                ref="cropper"
                :img="fileimg"
                :output-size="option.size"
                :output-type="option.outputType"
                :info="true"
                :full="option.full"
                :can-move="option.canMove"
                :can-move-box="option.canMoveBox"
                :original="option.original"
                :auto-crop="option.autoCrop"
                :auto-crop-width="option.autoCropWidth"
                :auto-crop-height="option.autoCropHeight"
                :fixed-box="option.fixedBox"
              />
            </div>
          </div>
        </el-col>
        <el-col
          :xs="20"
          :sm="20"
          :md="20"
          :lg="5"
          :xl="5"
        >
          <div>
            <br>
            <el-button
              type="primary"
              class="iconfont icon-xiangyouxuanzhuan"
              circle
              @click="rotateRight"
            />
            <el-button
              type="success"
              class="iconfont icon-xiangzuoxuanzhuan"
              circle
              @click="rotateLeft"
            />
            <el-button
              type="danger"
              class="iconfont icon-max"
              circle
              @click="changeScale(1)"
            />
            <el-button
              type="warning"
              class="iconfont icon-fangxiaojing"
              circle
              @click="changeScale(-1)"
            />
          </div>
          <el-button
            style="margin-top: 20px; margin-left: 40px"
            type="success"
            @click="submitUpload(funtype, false)"
          >
            编辑并上传
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script>
//https://blog.csdn.net/HH18700418030/article/details/120976087裁剪参考
import "vue-cropper/dist/index.css";
import { VueCropper } from "vue-cropper";
import {
  createSrc,
  imgUpload
} from "@/api/upload";
import { upload, goCompress } from "@/utils/getUploadImg";
import { getImgArrayBuffer, atchDownload } from "@/utils/download";
import { historyGetPage } from "@/api/history";

export default {
  components: {
    VueCropper,
  },
  props: {
    childPrehandle:{
      type:Number,
      default:0
    },
    childDenoise:{
      type:Number,
      default:0
    },
    childModelPath:{
      type:String,
      default:''
    },
    fileimg: {
      type: String,
      default: () => "",
    },
    funtype: {
      type:String,
      default:''
    },
    file: {
      type: Object,
      default:()=>{}
    },
  },
  emits: ["finish", "cut-changed",'child-refresh'],

  data() {
    return {
      uploadSrc: { list: [], prehandle: 0, denoise: 0,model_path:'' },
      headImg: "",
      //剪切图片上传
      crap: false,
      previews: {},
      option: {
        img: "",
        outputSize: 1, //剪切后的图片质量（0.1-1）
        full: false, //输出原图比例截图 props名full
        outputType: "png",
        canMove: true,
        original: false,
        canMoveBox: true,
        autoCrop: true,
        autoCropWidth: 800,
        autoCropHeight: 800,
        fixedBox: false,
      },
      fileName: "", //本机文件地址
      downImg: "#",
      imgFile: "",
      uploadImgRelaPath: "", //上传后的图片的地址（不带服务器域名）
    };
  },
  watch:{
    childDenoise:{
      handler(newVal,oldVal){
        this.uploadSrc.denoise = newVal
      },
      deep:true,
      immediate:true
    },
    childPrehandle:{
      handler(newVal,oldVal){
        this.uploadSrc.prehandle = newVal
      },
      deep:true,
      immediate:true
    },
    childModelPath:{
      handler(newVal,oldVal){
        this.uploadSrc.model_path = newVal
      },
      deep:true,
      immediate:true
    }
  },
  methods: {
    createSrc,
    imgUpload,
    upload,
    goCompress,
    getImgArrayBuffer,
    atchDownload,
    historyGetPage,
    submitUpload(funtype) {
      this.finish(funtype);
    },
    changeScale(num) {
      num = num || 1;
      this.$refs.cropper.changeScale(num);
    },
    //坐旋转
    rotateLeft() {
      this.$refs.cropper.rotateLeft();
    },
    //右旋转
    rotateRight() {
      this.$refs.cropper.rotateRight();
    },
    //上传图片（点击上传按钮）
    finish(funtype, cutVisible) {
      // 输出
      this.$refs.cropper.getCropData((data) => {
        const File = this.base64toFile(data, this.file.name);
        let formData = new FormData();
        formData.append("files", File);
        formData.append("type", funtype);
        this.createSrc(formData).then((res) => {
          this.uploadSrc.list = res.data.data.map((item) => {
            return item.src;
          });
          if (funtype === "地物分类") {
            this.imgUpload(this.uploadSrc,'semantic_segmentation').then((res) => {
              this.fileList = [];
              this.$message.success("上传成功！");
              this.$emit('child-refresh')
            }).catch((rej)=>{})
          } else if (funtype === "目标检测") {
            this.imgUpload(this.uploadSrc,'object_detection').then((res) => {
              this.fileList = [];
              this.$message.success("上传成功！");
              this.$emit('child-refresh')
            }).catch((rej)=>{})
          }
          else if (funtype === "场景分类") {
            delete this.uploadSrc.prehandle
            delete this.uploadSrc.denoise
            this.imgUpload(this.uploadSrc,'classification').then((res) => {
              this.fileList = [];
              this.$message.success("上传成功！");
              this.$emit('child-refresh')
            }).catch((rej)=>{})
          }
          else if(funtype === "图像复原"){
            delete this.uploadSrc.prehandle
            delete this.uploadSrc.denoise
            this.imgUpload(this.uploadSrc).then((res) => {
              this.fileList = [];
              this.$message.success("上传成功！");
              this.$emit('child-refresh')
            }).catch((rej)=>{})
          }
          this.$emit("cut-changed", false);
        }).catch((rej)=>{})
      });
    },
    base64toFile(dataurl, filename) {
      let arr = dataurl.split(",");
      let mime = arr[0].match(/:(.*?);/)[1];
      let suffix = mime.split("/")[1];
      let bstr = atob(arr[1]);
      let n = bstr.length;
      let u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], `${filename}.${suffix}`, {
        type: mime,
      });
    },
  },
};
</script>

<style scoped>
.cropper-content {
  min-width: 540px;
}
.cropper-content .cropper {
  width: 800px;
  height: 800px;
}
.cropper-content .show-preview {
  flex: 1;
  -webkit-flex: 1;
  display: flex;
  display: -webkit-flex;
  justify-content: center;
  -webkit-justify-content: center;
}
.cropper-content .show-preview .preview {
  overflow: hidden;
  border-radius: 50%;
  border: 1px solid #cccccc;
  background: #cccccc;
  margin-left: 40px;
}

.cropper-content .show-preview .preview {
  margin-left: 0;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
</style>