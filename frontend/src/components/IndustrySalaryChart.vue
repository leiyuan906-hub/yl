<template>
  <div class="chart-container">
    <!-- 图表容器 -->
    <div ref="chartRef" class="chart-box"></div>
    <!-- 功能按钮 -->
    <div class="tool-bar">
      <button @click="exportChart">导出图表</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { getIndustrySalary } from '../api';

const chartRef = ref(null);
let chartInstance = null;

// 初始化图表
onMounted(async () => {
  const response = await getIndustrySalary();
  const rawData = response.data; 

  // 处理数据（按行业顺序排序，提取x/y轴数据）
  const sortedData = rawData.sort((a, b) => a.avg_salary - b.avg_salary);
  const xData = sortedData.map(item => item.industry);
  const yData = sortedData.map(item => item.avg_salary);

  // 初始化图表实例
  chartInstance = echarts.init(chartRef.value);
  // 生成折线图配置
  const option = createLineChartOption(xData, yData);
  chartInstance.setOption(option);

  // 组件卸载时清理
  onUnmounted(() => {
    chartInstance.dispose();
  });
});

// 折线图配置项
const createLineChartOption = (xData, yData) => ({
  backgroundColor: '#ffffff',
  title: {
    text: '行业平均薪资趋势',
    left: 'center',
    textStyle: { color: '#2c3e50' }
  },
  tooltip: {
    trigger: 'axis',
    formatter: (params) => `${params[0].name}<br>薪资：${params[0].value.toFixed(2)} 元`
  },
  legend: {
    data: ['平均薪资'],
    top: '10px',
    right: '20px'
  },
  xAxis: {
    type: 'category',
    data: xData,
    axisTick: { alignWithLabel: true },
    axisLabel: { rotate: 45, fontSize: 12 } // 倾斜标签避免重叠
  },
  yAxis: {
    type: 'value',
    name: '平均薪资（元）',
    splitLine: { lineStyle: { type: 'dashed' } }
  },
  series: [
    {
      name: '平均薪资',
      type: 'line', // 关键：折线图类型
      data: yData,
      symbol: 'circle', // 标记点样式
      symbolSize: 8, // 标记点大小
      lineStyle: { width: 2, color: '#3498db' }, // 线条样式
      areaStyle: { // 区域填充（可选）
        color: new echarts.graphic.LinearGradient(
          0, 0, 0, 1,
          [{ offset: 0, color: '#3498db' }, { offset: 1, color: '#ecf0f1' }]
        )
      }
    }
  ],
  // 缩放功能配置（重点）
  dataZoom: [
    {
      type: 'inside', // 内置缩放（鼠标滚轮/拖动）
      start: 0, // 初始显示比例（0-100%）
      end: 100,
      xAxisIndex: 0 // 作用于x轴
    },
    {
      type: 'slider', // 底部滑动条缩放（可选）
      show: true,
      height: 8,
      left: '10%',
      right: '10%',
      bottom: '10px',
      xAxisIndex: 0
    }
  ]
});

// 导出图表为图片
const exportChart = () => {
  if (!chartInstance) return;
  // 生成图片URL
  const imgUrl = chartInstance.getDataURL({
    type: 'png', // 支持 'png'/'jpeg'/'webp'
    pixelRatio: 2 // 图片清晰度
  });
  // 创建下载链接
  const a = document.createElement('a');
  a.href = imgUrl;
  a.download = `行业薪资趋势_${new Date().getTime()}.png`;
  a.click();
};
</script>

<style scoped>
.chart-container {
  position: relative;
  padding: 20px;
}
.chart-box {
  width: 100%;
  height: 600px;
  box-shadow: 0 2px 8px rgba(250, 250, 250, 0.997);
  border-radius: 12px;
}
.tool-bar {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
}
button {
  padding: 8px 16px;
  border: 1px solid #eee;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  color: #333;
}
button:hover {
  background: #f5f7fa;
}
</style>