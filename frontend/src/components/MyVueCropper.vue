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
  classifyUpload,
  detectTargetsUpload,
} from "@/api/upload";
import { showFullScreenLoading, hideFullScreenLoading } from "@/utils/loading";
import { getUploadImg, upload, goCompress } from "@/utils/getUploadImg";
import { getImgArrayBuffer, atchDownload } from "@/utils/download";
import { historyGetPage } from "@/api/history";

export default {
  components: {
    VueCropper,
  },
  props: {
    prehandle:{
      type:Number
    },
    denoise:{
      type:Number
    },
    fileimg: {
      type: String,
      default: () => "",
    },
    funtype: {
      type:String
    },
    file: {
      type: Object,

    },
    length: {
      type:Number,
      default:0
    },
  },
  emits: ["finish", "cutChanged"],
  data() {
    return {
      setprehandle:'',
      setdenoise:'',
      uploadSrc: { list: [], prehandle: 0, denoise: 0 },
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
    data(){
       this.prehandle = this.setprehandle
      this.denoise = this.setdenoise

    }
  },

  methods: {
    createSrc,
    classifyUpload,
    detectTargetsUpload,
    getUploadImg,
    upload,
    goCompress,
    getImgArrayBuffer,
    atchDownload,
    historyGetPage,
    goRenderThis(){},
    goRenderThese(){},
    checkUpload(){},
    setNormalWay(){},
    submitUpload(funtype) {
      // this.finish(funtype);
    },
    handleRemove(file, fileList) {},
    handlePreview(file) {
      //   let data = window.URL.createObjectURL(new Blob([file]));
      //   this.option.img = data;
    },
    //放大/缩小
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
 
     showFullScreenLoading('#load')
      this.$refs.cropper.getCropData((data) => {
        // this.model = true
        // this.modelSrc = data
        const File = this.base64toFile(data, this.file.name);
        let formData = new FormData();
        formData.append("files", File);
        formData.append("type", funtype);
        this.createSrc(formData).then((res) => {
          this.uploadSrc.list = res.data.data.map((item) => {
            return item.src;
          });
          if (this.length >= 20) {
            this.$confirm(
              "上传图片过多，是否压缩?在此期间不能进行其他操作",
              "提示",
              {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
              }
            )
              .then(() => {
            
                // this.goCompress(funtype);
                setTimeout(() => {
                  this.$message({
                    type: "info",
                    message: "正在压缩，请勿进行其他操作！刷新界面取消压缩",
                    duration: 4000,
                    center: true,
                    showClose: true,
                  });
                }, 1000);

                this.historyGetPage(1, 99999, funtype).then((res) => {
               
                  this.atchDownload(
                    res.data.data.map((item) => {
                      return { after_img: item.after_img, id: item.id };
                    })
                  );
                });
              })
              .catch(() => {
            
              });
          }

          if (funtype === "地物分类") {
            this.classifyUpload(this.uploadSrc).then((res) => {
              this.fileList = [];
              hideFullScreenLoading("#load");
              this.$message.success("上传成功！");
              setTimeout(() => {
                     this.getUploadImg("地物分类");
              }, 200);
         
            });
          } else if (funtype === "目标检测") {
            this.detectTargetsUpload(this.uploadSrc).then((res) => {
              this.fileList = [];
              hideFullScreenLoading("#load");
              this.$message.success("上传成功！");
              this.getUploadImg("目标检测");
            });
          }
          this.$emit("cutChanged", false);
        });
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