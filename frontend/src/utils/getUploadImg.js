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
    }
    if (type === '场景分类') {
      this.scene = res.data.data.map(item=>item.data)     //场景键值对数组,[{'a':0.8},{‘b’:0.6},{'c':0.8}]
      this.sceneKey = this.scene.map(item=>Object.keys(item))  //构成场景键数组的数组，[['a'],['b'],['c']]
    }
    this.afterImg = res.data.data.map((item) => {
      return { after_img: global.BASEURL + item.after_img, id: item.id };
    });
    this.checkUpload(); 
    // if(type=='地物分类'&&!this.isUpload){
    //   this.beforeImg = [{before_img:'https://u5l5066767.goho.co/_uploads/photos/b038eb0aa89c272bedb12da531a5e9c7_T073142_5.jpg',id:0}]
    //   this.beforeList= ['https://u5l5066767.goho.co/_uploads/photos/b038eb0aa89c272bedb12da531a5e9c7_T073142_5.jpg']
    //   this.afterImg = [{after_img:'https://u5l5066767.goho.co/_uploads/photos/res/21d63754c5ba8d834807f4bea5863703_b038eb0aa89c272bedb12da531a5e9c7_T073142_5.jpg',id:0}]
    //   this.afterList = ['https://u5l5066767.goho.co/_uploads/photos/res/21d63754c5ba8d834807f4bea5863703_b038eb0aa89c272bedb12da531a5e9c7_T073142_5.jpg']
    // }
    // if(type=='目标检测'&&!this.isUpload){
    //   this.beforeImg = [{before_img:'https://u5l5066767.goho.co/_uploads/photos/675522696836c169328af7e4fa29af83_playground_344_5.jpg',id:0}]
    //   this.beforeList= ['https://u5l5066767.goho.co/_uploads/photos/675522696836c169328af7e4fa29af83_playground_344_5.jpg']
    //   this.afterImg = [{after_img:'https://u5l5066767.goho.co/_uploads/photos/res/90e49cb6c7ac462704ba57440b892891_675522696836c169328af7e4fa29af83_playground_344_5.jpg',id:0}]
    //   this.afterList = ['https://u5l5066767.goho.co/_uploads/photos/res/90e49cb6c7ac462704ba57440b892891_675522696836c169328af7e4fa29af83_playground_344_5.jpg']
    // }
    if(!this.isUpload){
      this.setNormalWay()
    }
  }).then((rej)=>{
    hideFullScreenLoading("#load");
  })
}

function goCompress(type) {
  setTimeout(() => {
    this.$message({
      type: 'info',
      message: "正在压缩，请勿进行其他操作！刷新界面取消压缩",
      duration: 4000,
      center: true,
      showClose: true
    });
  }, 500);
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
        this.classifyUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          hideFullScreenLoading("#load")
          this.$message.success("上传成功！");
          this.getMore()
        });
      }
      else if (type === '目标检测') {
        this.detectTargetsUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          hideFullScreenLoading("#load")
          this.$message.success("上传成功！");
          this.getMore()
        })
      }
      else if (type === '场景分类') {
        this.sceneClassifyUpload(this.uploadSrc).then((res) => {
          this.fileList = []
          hideFullScreenLoading("#load")
          this.$message.success("上传成功！");
          this.getMore()
        })
      }
      if (this.afterImg.length >= 20 && type!=='场景分类') {
        this.$confirm("上传图片过多，是否压缩?在此期间不能进行其他操作", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
          
            showFullScreenLoading('#load')
            this.goCompress(type)
          }).catch(() => {
           
          })
      }
      _this.$refs.upload.clearFiles();
    });
  }
}


export { getUploadImg, goCompress, upload }