import { historyGetPage } from "@/api/history"
import { showFullScreenLoading, hideFullScreenLoading } from "@/utils/loading";
import global from '@/global'

function getUploadImg(type) {
  showFullScreenLoading("#load");
  historyGetPage(1, 20, type).then((res) => {
    hideFullScreenLoading("#load")
    this.beforeImg = res.data.data.map((item) => {
      return { before_img: global.BASEURL + item.before_img };
    });
    this.beforeList=res.data.data.map((item)=>{
      return global.BASEURL + item.before_img
    })
    if (type === '变化检测') {
      this.beforeImg1 = res.data.data.map((item) => {
        return { before_img1: global.BASEURL + item.before_img1 };
      });
      this.checkUpload();
      if(!this.isUpload){
        this.setNormalWay()
      }
    }
    if (type === '场景分类') {
      this.scene = res.data.data.map(item=>item.data)     //场景键值对数组,[{'a':0.8},{‘b’:0.6},{'c':0.8}]
      this.sceneKey = this.scene.map(item=>Object.keys(item))  //构成场景键数组的数组，[['a'],['b'],['c']]
    }
    this.afterImg = res.data.data.map((item) => {
      return { after_img: global.BASEURL + item.after_img, id: item.id };
    });
    this.afterList = res.data.data.map((item) => {
      return global.BASEURL + item.after_img
    });
    if(type === '图像复原') {
      this.idList = res.data.data.map((item) => {
        return item.id;
      });
      this.goShowThese(0)
    }
    this.checkUpload();
  }).then((rej)=>{
    hideFullScreenLoading("#load");
  })
}

function goCompress(type) {
  this.historyGetPage(1, 99999, type).then((res) => {
    this.atchDownload(
        res.data.data.map((item) => {
          return { after_img: item.after_img, id: item.id };
        })
    );
  });
}

function upload(type) {
  if (this.fileList.length === 0) {
    this.$message.error("请上传图片！");
  } else {
    showFullScreenLoading("#load");
    let formData = new FormData();
    let _this = this;

    for (const item of this.fileList) {
      formData.append("files", item) || formData.append('files', item.raw);
      formData.append("type", type);
    }
    this.createSrc(formData).then((res) => {
      this.uploadSrc.list = res.data.data.map((item) => {
        return item.src;
      });
      if (type === '地物分类') {
        this.SegmentationUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          hideFullScreenLoading("#load")
          this.$message.success("上传成功！");
          this.getMore()
        });
      }
      else if (type === '目标检测') {
        this.detectObjectsUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          hideFullScreenLoading("#load")
          this.$message.success("上传成功！");
          this.getMore()
        })
      }
      else if (type === '场景分类') {
        this.classificationUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          hideFullScreenLoading("#load")
          this.$message.success("上传成功！");
          this.getMore()
        })
      }
      else if (type === '图像复原') {
        this.restoreImgsUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          hideFullScreenLoading("#load")
          this.$message.success("上传成功！");
          this.getMore()
        })
      }
      if (this.uploadSrc.list.length >= 10 && type!=='场景分类') {
        this.$confirm("上传图片过多，是否压缩?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
            .then(() => {

              showFullScreenLoading('#load','压缩中')
              this.goCompress(type)
            }).catch(() => {

        })
      }
      _this.$refs.upload.clearFiles();
    });
  }
}


export { getUploadImg, goCompress, upload }