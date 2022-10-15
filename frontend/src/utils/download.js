//https://blog.csdn.net/tattoo_jie/article/details/122251905压缩打包功能
import JSZIP from "jszip"
import FileSaver from 'file-saver'

import global from '@/global'
import {hideFullScreenLoading} from "@/utils/loading";
function downloadimgWithWords(index, src, funtype) {
  fetch(src)
    .then((response) => response.blob())//链式编程
    .then((res) => {
      let blob = new Blob([res]);
      // 通过URL.createObjectURL生成文件路径
      let url = window.URL.createObjectURL(blob);
      // 创建a标签
      let ele = document.createElement("a");
      ele.style.display = "none";
      // 设置href属性为文件路径，download属性可以设置文件名称
      ele.href = url;
      if(index === -1){ele.download = `${funtype}`}
      else{
        ele.download = `第${index}组${funtype}`;
      }
      // 将a标签添加到页面并模拟点击
      document.querySelectorAll("body")[0].appendChild(ele);
      ele.click();
      // 移除a标签
      ele.remove();
    });
}
function getImgArrayBuffer(url) {
  return new Promise((resolve, reject) => {
    //通过请求获取文件blob格式
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET",global.BASEURL+url, true);
    xmlhttp.responseType = "blob";
    xmlhttp.onload = function () {
      if (this.status === 200) {
        resolve(this.response);
      } else {
        reject(this.status);
      }
    };
    xmlhttp.send();
  });
}
//批量下载
function atchDownload(compressImg) {
  // this.images 是要下载的图片数组  [{url: 图片地址, id: 图片名称}]
  // 定时器 loading

  let _this = this;
  let zip = new JSZIP();
  let cache = {};
  let promises = [];
  for (let item of compressImg) {
    const promise = _this.getImgArrayBuffer(item.after_img).then((data) => {    //获取单个文件的promise返回
      // 下载文件, 并存成ArrayBuffer对象(blob)
      zip.file(item.id + ".png", data, { binary: true }); // 逐个添加文件
      cache[item.id] = data;
    });
    promises.push(promise);
  }

  Promise.all(promises)
    .then(() => {
      zip.generateAsync({ type: "blob" }).then((content) => {

        // 生成Blob二进制流
        FileSaver.saveAs(content, "打包图片"); // 利用file-saver保存文件  自定义文件名
        _this.$message.success("压缩完成！");
        hideFullScreenLoading()
      });
    })
    .catch((res) => {
        hideFullScreenLoading()
      _this.$message.error('压缩失败！')
    });
}


export { downloadimgWithWords, getImgArrayBuffer, atchDownload}