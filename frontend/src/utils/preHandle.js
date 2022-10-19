import {createSrc,prePhotoHandle} from '@/api/upload'
import global from '@/global'
function selectSharpen(type) {
  if(this.fileList.length  === 0){
    if( this.uploadSrc.prehandle === 4){
      this.$refs.sharpen.checked = false;
      this.uploadSrc.prehandle = 0
    }
    else{
      this.$refs.sharpen.checked = false;
      this.$message.error('请先上传图片')
    }

  }else{
    if (this.$refs.clahe.checked === true) {
      this.$refs.clahe.checked = false;
    }

    if (this.$refs.sharpen.checked === false) {
      this.$message.success("取消锐化处理");
      this.uploadSrc.prehandle=0
    } else {
      this.$message.success("锐化处理");
      this.uploadSrc.prehandle = 4

      let formData = new FormData();
      for (const item of this.fileList) {
        formData.append("files", item) || formData.append('files', item.raw);
        formData.append("type", type);
      }
      createSrc(formData).then((res) => {
        this.uploadSrc.list = res.data.data.map((item) => {
          return global.BASEURL+item.src;
        });
        this.before = this.uploadSrc.list.splice(0,3)
   
        this.prePhoto.list = this.before;
        this.prePhoto.prehandle = 4;
    
        prePhotoHandle(this.prePhoto).then((res)=>{
        
          this.sharpenImg = res.data.data.map((item)=>{
            return global.BASEURL + item
          })
        })
      }).catch((rej)=>{})
    }
  }
  }
  function selectClahe(type) {
    if(this.fileList.length === 0){
      if( this.uploadSrc.prehandle === 2){
        this.$refs.clahe.checked = false;
        this.uploadSrc.prehandle = 0
      }
      else{
        this.$refs.clahe.checked = false;
        this.$message.error('请先上传图片')
      }
    }else{
      if (this.$refs.sharpen.checked === true) {
        this.$refs.sharpen.checked = false;
      }
      if (this.$refs.clahe.checked === false) {
        this.$message.success("取消CLAHE处理");
        this.uploadSrc.prehandle = 0
      } else {
        this.$message.success("CLAHE处理");
        this.uploadSrc.prehandle = 2

        let formData = new FormData();
        for (const item of this.fileList) {
          formData.append("files", item) || formData.append('files', item.raw);
          formData.append("type", type);
        }
        createSrc(formData).then((res) => {
          this.uploadSrc.list = res.data.data.map((item) => {
            return global.BASEURL+item.src;
          });
          this.before = this.uploadSrc.list.splice(0,3)
      
          this.prePhoto.list = this.before
          this.prePhoto.prehandle = 2
       
          prePhotoHandle(this.prePhoto).then((res)=>{
       
            this.claheImg = res.data.data.map((item)=>{
              return global.BASEURL + item
            })
          }).catch((rej)=>{})
        }).catch((rej)=>{})
      }
    }
  }
 function selectFilter() {
    if (this.$refs.smooth.checked === true) {
      this.$refs.smooth.checked = false;
    }

    if (this.$refs.filter.checked === false) {
      this.$message.success("取消高斯滤波处理");
      this.uploadSrc.denoise = 0
    } else {
      this.$message.success("高斯滤波处理");
      this.uploadSrc.denoise = 5
    }
  }
  function selectSmooth() {
    if (this.$refs.filter.checked === true) {
      this.$refs.filter.checked = false;
    }

    if (this.$refs.smooth.checked === false) {
      this.$message.success("取消平滑处理");
      this.uploadSrc.denoise = 0
    } else {
      this.$message.success("平滑处理");
      this.uploadSrc.denoise = 3
    }
  }

  export {selectSharpen,selectFilter,selectSmooth,selectClahe}