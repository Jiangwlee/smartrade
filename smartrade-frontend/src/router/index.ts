import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Layout from '@/layout/index.vue'
import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'

const routes = [
  { 
    path: '/', 
    component: Layout,
    alias: '/home',
    children: [
      {
        path: '',
        component: () => import('@/components/HelloWorld.vue'),
        name: 'home', 
      }
    ] 
  },
  { 
    path: '/prediction', 
    name: '预测', 
    component: Layout, 
    redirect: '/prediction/index',
    children: [
      {
        path: 'index',
        component: () => import('@/components/Prediction.vue'),
        name: 'prediction'
      }
    ] 
  },
  { 
    path: '/helloworld', 
    name: '测试', 
    component: Layout,
    redirect: '/helloworld/index',
    children: [
      {
        path: 'index',
        component: () => import('@/components/HelloWorld.vue'),
        name: 'helloworld'
      }
    ]
  } 
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export default router
