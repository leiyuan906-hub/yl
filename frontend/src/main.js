import { createApp } from 'vue'
import App from './App.vue'
import VueApexCharts from "vue3-apexcharts";
import router from './router' 
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


const app = createApp(App);
app.use(VueApexCharts);
app.use(ElementPlus);
app.use(router);
app.component('ApexChart', VueApexCharts)  // 注册为 PascalCase

app.mount('#app')