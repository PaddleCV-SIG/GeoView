import { historyGetPage } from "@/api/history"
import global from '@/global'
import {showFullScreenLoading} from "@/utils/loading";

function getUploadImg(type) {
  historyGetPage(1, 20, type).then((res) => {
    this.imgArr = res.data.data.forEach((item)=>{
      item['before_img1']=global.BASEURL+item.before_img1
      item['before_img'] = global.BASEURL+item.before_img
      item['after_img'] = global.BASEURL+item.after_img
    })
    this.imgArr = res.data.data
    this.beforeImg = res.data.data.map((item) => {
      return { before_img:  item.before_img };
    });
    this.beforeList=res.data.data.map((item)=>{
      return  item.before_img
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
    this.afterImg = res.data.data.map((item) => {
      return { after_img:  item.after_img, id: item.id };
    });
    this.afterList = res.data.data.map((item) => {
      return  item.after_img
    });
    if(type === '图像复原') {
      this.idList = res.data.data.map((item) => {
        return item.id;
      });
      this.goShowThese(0)
    }
    this.checkUpload();
  }).catch((rej)=>{})
}

function goCompress(type,num) {
  this.historyGetPage(1, num, type).then((res) => {
    this.atchDownload(
        res.data.data.map((item) => {
          return { after_img: item.after_img, id: item.id };
        })
    );
  }).catch((rej)=>{});
}

function upload(type) {
  if (this.fileList.length === 0) {
    this.$message.error("请上传图片！");
  } else {
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
          this.$message.success("上传成功！");
          this.getMore()
        }).catch((rej)=>{})
      }
      else if (type === '目标检测') {
        this.detectObjectsUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          this.$message.success("上传成功！");
          this.getMore()
        }).catch((rej)=>{})
      }
      else if (type === '场景分类') {
        this.classificationUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          this.$message.success("上传成功！");
          this.getMore()
        }).catch((rej)=>{})
      }
      else if (type === '图像复原') {
        this.restoreImgsUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          this.$message.success("上传成功！");
          this.getMore()
        }).catch((rej)=>{})
      }
      if (this.uploadSrc.list.length >= 2 && type!=='场景分类') {
        this.$confirm("上传图片过多，是否压缩?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
            .then(() => {
              showFullScreenLoading('#load','压缩中')
              this.goCompress(type,this.uploadSrc.list.length)
            }).catch(() => {
        })
      }
      _this.$refs.upload.clearFiles();
    }).catch((rej)=>{});
  }
}


export { getUploadImg, goCompress, upload }