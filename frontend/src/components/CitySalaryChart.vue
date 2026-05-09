<template>
    <div class="chart-container">
      <div v-if="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <ApexChart
        v-else
        type="bar"
        height="400"
        :options="chartOptions"
        :series="chartSeries"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import {getCitySalary} from '../api'
  const chartSeries = ref([{
    name: '平均薪资',
    data: []
  }])
  
  const chartOptions = ref({
    chart: { type: 'bar' },
    xaxis: { 
      categories: [],
      labels: {
        formatter: (value) => value.length > 3 ? `${value.slice(0,3)}...` : value  // 处理长城市名
      }
    },
    yaxis: { title: { text: '薪资 (元)' } },
    colors: ['#3F51B5']
  })
  
  const loading = ref(true)
  const error = ref(null)
  
  onMounted(async () => {
    try {
      const response = await getCitySalary()
      const rawData = response.data || []
  
      // 按薪资排序
      const sortedData = rawData.sort((a, b) => b.avg_salary - a.avg_salary)
  
      // 更新图表数据
      chartSeries.value[0].data = sortedData.map(item => Math.round(item.avg_salary))
      chartOptions.value.xaxis.categories = sortedData.map(item => item.city)
  
    } catch (err) {
      error.value = `数据加载失败: ${err.message}`
    } finally {
      loading.value = false
    }
  })
  </script>