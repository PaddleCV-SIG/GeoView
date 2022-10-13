import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('@/views/Home.vue')
const DetectChanges = () => import('@/views/mainfun/DetectChanges.vue')
const DetectObjects = () => import('@/views/mainfun/DetectObjects.vue')
const Segmentation = () => import('@/views/mainfun/Segmentation.vue')
const Classification = ()=> import('@/views/mainfun/Classification')
const RestoreImgs = ()=> import('@/views/mainfun/RestoreImgs')
const OnlineMap = () => import('@/views/mainfun/OnlineMap.vue')
const History = () => import('@/views/history/History.vue')
const NotFound = () => import('@/views/NotFound.vue')
const routes = [
  {
    path: '/',
    redirect: '/detectchanges'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    children: [
      {
        path: '/detectchanges',
        name: 'Detectchanges',
        component: DetectChanges,

      }, {
        path: '/detectobjects',
        name: 'Detectobjects',
        component: DetectObjects
      },  {
        path: '/segmentation',
        name: 'Segmentation',
        component: Segmentation
      },
      {
        path: '/classification',
        name:'Classification',
        component:Classification
      },
      {
        path:'/restoreimgs',
        name:'Restoreimgs',
        component:RestoreImgs
      },
      {
        path: '/history',
        name: 'history',
        component: History,
      }
      , {
        path:'/onlinemap',
        name:'onlinemap',
        component:OnlineMap
      }
    ]
  },
  {
    path: "/:pathMatch(.*)*",
    name: 'notfound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})
export default router
