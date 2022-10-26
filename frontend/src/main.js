import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

import '@/assets/font/iconfont.css'
import './assets/css/normalize.css'
import '@/assets/css/app.css'
import '@/assets/css/font.css'
import 'element-plus/theme-chalk/display.css'
import 'animate.css';

import JSZIP from "jszip"
import zhCn from 'element-plus/es/locale/lang/zh-cn'

const app = createApp(App)
app.use(router).use(ElementPlus,{locale: zhCn}).use(JSZIP).mount('#app')
app.directive('drag',{
    mounted(el, binding, vnode, prevVnode) {
        const mouseDown = (e) => {
            let X = e.clientX - el.offsetLeft
            let Y = e.clientY - el.offsetTop
            const mouseMove = (e) => {
                el.style.left = e.clientX - X + 'px'
                el.style.top = e.clientY - Y + 'px'
            }
            document.addEventListener('mousemove', mouseMove)
            document.addEventListener('mouseup', () => {
                document.removeEventListener('mousemove', mouseMove)
            })
        }
        el.addEventListener('mousedown', mouseDown)
    },
})