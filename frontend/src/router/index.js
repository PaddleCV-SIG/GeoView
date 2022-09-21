import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('@/views/Home.vue')
const DetectChanges = () => import('@/views/mainfun/DetectChanges.vue')
const DetectTargets = () => import('@/views/mainfun/DetectTargets.vue')
const Classify = () => import('@/views/mainfun/Classify.vue')
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
    name: 'home',
    component: Home,
    children: [
       {
        path: '/detectchanges',
        name: 'detectchanges',
        component: DetectChanges,

      }, {
        path: '/detecttargets',
        name: 'detecttargets',
        component: DetectTargets
      },  {
        path: '/classify',
        name: 'classify',
        component: Classify
      }, {
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
