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
        component: () => import('@/components/Review.vue'),
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
    path: '/evaluation',
    name: '评估',
    component: TheLayout,
    redirect: '/evaluation/index',
    children: [
      {
        path: 'index',
        component: () => import('@/components/Evaluation.vue'),
        name: 'evaluation',
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
});

export default router;
