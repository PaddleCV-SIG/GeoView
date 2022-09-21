import axios from "axios"
import router from '../router'
import store from '@/store' 
import global from '@/global'
import { hideFullScreenLoading} from '@/utils/loading'
import { ElMessage } from 'element-plus'
export function request(config) {
  const instance = axios.create({
    baseURL:global.BASEURL
  })
  instance.interceptors.response.use(
    (response) => {
      return response
    },
    ({ response }) => {
      hideFullScreenLoading('#load')
      hideFullScreenLoading(".changes-box");
      hideFullScreenLoading(".fb-box")
      ElMessage.error('网络异常，请检查后端服务是否启动')
      return Promise.reject(error)
    },
  )
  return instance(config)
}

