// router.js
import { createRouter, createWebHistory } from 'vue-router'



// 路由表
const routes = [
  {
    path: '/overview',
    name: 'overview',
    component: () => import('../views/Overview.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('../components/JobSearch.vue')
  },
  {
    path: '/visual/city-salary',
    name: 'city-salary',
    component: () => import('../components/CitySalaryChart.vue')
  },
  {
    path: '/visual/education-salary',
    name: 'education-salary',
    component: () => import('../components/EducationSalaryChart.vue')
  },
  {
    path: '/visual/industry-salary',
    name: 'industry-salary',
    component: () => import('../components/IndustrySalaryChart.vue')
  },
  {
    path: '/visual/major-salary',
    name: 'major-salary',
    component: () => import('../components/MajorSalaryChart.vue')
  },
  {
    path:'/visual/china-map',
    name:'china-map',
    component: () => import('../components/ProvinceMap.vue')
  },
  {
    path:'/visual/recruit-ratio',
    name:'recruit-ratio',
    component: () => import('../components/RecruitRatioChart.vue')
  },
  {
    path: '/',
    redirect: '/overview'
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router