import { Loading } from "element-plus/es/components/loading/src/service";
 
// loading框设置局部刷新，且所有请求完成后关闭loading框
let loading

let needLoadingRequestCount = 0 // 声明一个对象用于存储请求个数
let needCompressRequestCount  = 0
function startLoading (targetdq) {
  loading = Loading({
    lock: true,
    text: '努力加载中...',
    background: 'rgba(255, 255, 255, 0.9)',
    target: document.querySelector(targetdq) // 设置加载动画区域
  })
}
function compressLoading (targetdq) {
  loading = Loading({
    lock: true,
    text: '努力压缩中...',
    background: 'rgba(255, 255, 255, 0.9)',
    target: document.querySelector(targetdq) // 设置加载动画区域
  })
}
function endLoading () {
    loading.close()
}
export function showFullScreenLoading (targetdq) {
  if (needLoadingRequestCount === 0) {
    startLoading(targetdq)
  }
  needLoadingRequestCount++
}
export function hideFullScreenLoading () {
  if (needLoadingRequestCount <= 0) return
  needLoadingRequestCount--
  if (needLoadingRequestCount === 0) {
    endLoading()
  }
}
export function showCompressLoading (targetdq) {
  if (needCompressRequestCount === 0) {
    compressLoading(targetdq)
  }
  needCompressRequestCount++
}
export function hideCompressLoading () {
  if (needCompressRequestCount <= 0) return
  needCompressRequestCount--
  if (needCompressRequestCount === 0) {
    endLoading()
  }
}
 
export default {
  showFullScreenLoading,
  hideFullScreenLoading,
  showCompressLoading,
  hideCompressLoading
}
