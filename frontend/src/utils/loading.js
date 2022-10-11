import { Loading } from "element-plus/es/components/loading/src/service";
 
// loading框设置局部刷新，且所有请求完成后关闭loading框
let loading

let needLoadingRequestCount = 0 // 声明一个对象用于存储请求个数
function startLoading (targetdq,text) {
  loading = Loading({
    lock: true,
    text: `努力${text}...`,
    background: 'rgba(255, 255, 255, 0.9)',
    target: document.querySelector(targetdq) // 设置加载动画区域
  })
}
function endLoading () {
    loading.close()
}
export function showFullScreenLoading (targetdq,text = '加载中') {
  if (needLoadingRequestCount === 0) {
    startLoading(targetdq,text)
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

export default {
  showFullScreenLoading,
  hideFullScreenLoading,
}
