<template>
  <div ref="chart" class="china-map" style="width: 100%; height: 600px"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getProvinceStats } from '../api';

const chart = ref(null)
let myChart = null

// 加载地图数据
const loadMapData = async () => {
  try {
    const chinaJson = await fetch('../assets/MapData/china.json').then(res => res.json())
    echarts.registerMap('china', chinaJson)
    initChart()
  } catch (error) {
    console.error('地图数据加载失败:', error)
  }
}

// 初始化图表
const initChart = async () => {
  try {
    const response = await getProvinceStats()
    const mapData = response.data.map(item => ({
      name: item.province,
      value: Math.round(item.avg_salary),
      count: item.count
    }))

    const exportToCSV = (data) => {
  const csvContent = '省份,平均薪资,职位数量\n' + 
    data.map(d => `${d.name},${d.value},${d.count}`).join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = '省份薪资分布.csv';
  link.click();
};

const option = {
      title: {
        text: '各省份薪资热力图',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: params => `
          <b>${params.name}</b><br>
          平均薪资: ¥${params.data.value}<br>
          职位数量: ${params.data.count}
        `
      },
      visualMap: {
        min: Math.min(...mapData.map(d => d.value)),
        max: Math.max(...mapData.map(d => d.value)),
        left: 'right',
        text: ['高', '低'],
        calculable: true,
        inRange: { color: ['#e0f3f8', '#0868ac'] }
      },
      toolbox: {
        show: true,
        right: 20,
        top: 'top',
        feature: {
          myExportCSV: {
            show: true,
            title: '导出CSV',
            icon: 'path://M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2v9.67z',
            onclick: () => exportToCSV(mapData)
          },
          saveAsSVG: {
            title: '下载SVG',
            name: '省份薪资分布',
            icon: 'path://M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2v9.67z',
            type: 'svg',
            name: '省份薪资分布',
            title: '下载PNG',
            pixelRatio: 2
          },
          saveAsPNG: {
            title: '下载PNG',
            name: '省份薪资分布',
            title: '下载PNG',
            pixelRatio: 2
          }
        }
      },
      series: [{
        type: 'map',
        map: 'china',
        roam: true,
        label: { show: true },
        emphasis: { label: { show: true } },
        data: mapData
      }]
    }

    myChart = echarts.init(chart.value)
    myChart.setOption(option)
    
    // 窗口自适应
    window.addEventListener('resize', handleResize)
  } catch (error) {
    console.error('数据加载失败:', error)
  }
}

const handleResize = () => myChart?.resize()

onMounted(() => loadMapData())
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  myChart?.dispose()
})
</script>

<style scoped>
.china-map {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
</style>