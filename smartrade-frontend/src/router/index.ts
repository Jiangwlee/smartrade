import { createRouter, createWebHistory } from 'vue-router';
import TheLayout from '@/layout/TheLayout.vue';

const routes = [
  {
    path: '/',
    component: TheLayout,
    alias: '/home',
    children: [
      {
        path: '',
        component: () => import('@/components/HelloWorld.vue'),
        name: 'home',
      },
    ],
  },
  {
    path: '/prediction',
    name: '预测',
    component: TheLayout,
    redirect: '/prediction/index',
    children: [
      {
        path: 'index',
        component: () => import('@/components/Prediction.vue'),
        name: 'prediction',
      },
    ],
  },
  {
    path: '/helloworld',
    name: '测试',
    component: TheLayout,
    redirect: '/helloworld/index',
    children: [
      {
        path: 'index',
        component: () => import('@/components/HelloWorld.vue'),
        name: 'helloworld',
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
});

export default router;
