import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'

import '@/assets/font/iconfont.css'
import './assets/css/normalize.css'
import '@/assets/css/app.css'
import 'element-plus/theme-chalk/display.css'
import VueParticles from 'vue-particles'
import JSZIP from "jszip"
import zhCn from 'element-plus/es/locale/lang/zh-cn'



createApp(App).use(store).use(router).use(ElementPlus,{locale: zhCn}).use(VueParticles).use(JSZIP).mount('#app')