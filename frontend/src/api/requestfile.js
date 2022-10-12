import axios from "axios"

import global from '@/global'
export function requestfile(config) {
  const instance = axios.create({
    // timeout: 5000,
    baseURL: global.BASEURL,
    transformRequest: [function(data, headers) {
        // 去除post请求默认的Content-Type
        delete headers.post['Content-Type']
        return data
      }],
      
  })
  instance.interceptors.request.use(
    (config) => {
        config.headers.Accept = 'multipart/form-data'
        config.headers['Content-Type'] = 'multipart/form-data';
        return config
    },
    (error) => Promise.reject(error),
  )

  instance.interceptors.response.use(
    (response) => {


      return response
    },
    ({ response }) => {
      const { status, data } = response
      const { message } = data
      alert('网络异常，请重试！')
      return Promise.reject(error)
    },
  )
  return instance(config)
}

