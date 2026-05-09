<template>
  <div class="chart-container">
      <div v-if="loading">加载中...</div>
      <div v-else-if="error" class="error">错误: {{ error }}</div>
      <div v-else ref="chartRef" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { getEducationSalary } from '../api';

const chartRef = ref(null);
const chartInstance = ref(null);
const loading = ref(true);
const error = ref(null);

const chartOption = {
  xAxis: {
      type: 'category',
      data: [],
      axisLabel: {
          fontSize: 12,
          fontStyle: 'normal',
          fontWeight: 'bold' // 字体加粗
      }
  },
  yAxis: {
      type: 'value',
      name: '薪资 (元)',
      axisLabel: {
          formatter: (value) => `¥${value.toLocaleString()}`,
          fontSize: 12,
          fontStyle: 'normal',
          fontWeight: 'bold' // 字体加粗
      }
  },
  series: [
      {
          name: '平均薪资',
          type: 'bar',
          data: [],
          itemStyle: {
              color: '#4CAF50'
          },
          label: {
              show: true,
              position: 'top',
              fontSize: 12,
              fontStyle: 'normal',
              fontWeight: 'bold' // 字体加粗
          },
          barBorderRadius: 4
      }
  ],
  title: {
      text: '教育程度与平均薪资关系',
      left: 'center',
      textStyle: {
          fontFamily: '黑体',
          fontSize: 15,
          fontStyle: 'normal',
          fontWeight: 'bold' // 字体加粗
      }
  },
  tooltip: {
      trigger: 'axis',
      axisPointer: {
          type: 'shadow'
      },
      textStyle: {
          fontFamily: '黑体',
          fontSize: 12,
          fontStyle: 'normal',
          fontWeight: 'bold' // 字体加粗
      }
  },
  toolbox: {
      show: true,
      feature: {
          saveAsImage: {
              show: true,
              type: 'png',
              name: '教育程度与平均薪资关系图',
              pixelRatio: 2
          }
      }
  }
};

onMounted(async () => {
  try {
      const response = await getEducationSalary();
      const rawData = response.data || [];

      // 按薪资排序
      const sortedData = rawData.sort((a, b) => b.avg_salary - a.avg_salary);

      // 更新图表数据
      chartOption.xAxis.data = sortedData.map(item => item.education);
      chartOption.series[0].data = sortedData.map(item => Math.round(item.avg_salary));
  } catch (err) {
      error.value = `数据加载失败: ${err.message}`;
  } finally {
      loading.value = false; // 先设为 false，触发 DOM 渲染
      await nextTick(); // 等待 DOM 渲染完成
      if (chartRef.value) {
          chartInstance.value = echarts.init(chartRef.value);
          chartInstance.value.setOption(chartOption);
      } 
  }
});

onUnmounted(() => {
  if (chartInstance.value) {
      chartInstance.value.dispose();
  }
});
</script>

<style scoped>
.chart-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}
.error {
  color: #ff4444;
}
</style>