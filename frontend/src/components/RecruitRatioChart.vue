<template>
  <div ref="chartRef" class="chart-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { getRecruitRatio } from '../api';

const chartRef = ref(null);
let chartInstance = null;

onMounted(async () => {
  try {
    const response = await getRecruitRatio();
    const rawData = response.data || [];
    const processedData = rawData
      .sort((a, b) => b.count - a.count)
      .map(item => ({
        ...item,
        truncatedName: truncateText(item.industry, 20),
        color: getColorByCount(item.count)
      }));

    // 增加对 processedData 是否为空的检查
    if (processedData.length > 0) {
      initChart(processedData);
    } else {
      console.error('处理后的数据为空，无法初始化图表。');
    }
  } catch (error) {
    console.error('数据加载失败:', error);
  }
})

const initChart = (processedData) => {
  if (!chartRef.value) return;

  chartInstance = echarts.init(chartRef.value);
  
  const option = {
    title: {
      text: '职位数量分布',
      left: 'center'
    },
    tooltip: {
      formatter: (params) => {
        const dataItem = processedData[params.dataIndex];
        return `${dataItem.industry}<br/>数量: ${dataItem.count}`;
      }
    },
    xAxis: {
      type: 'category',
      data: processedData.map(item => item.truncatedName),
      axisLabel: { rotate: 45, fontSize: 12 }
    },
    yAxis: {
    type: 'value',
    name: '数量',
  },
    series: [{
      type: 'bar',
      data: processedData.map(item => ({
        value: item.count,
        itemStyle: { color: item.color }
      })),
      label: {
        show: true, // 始终启用标签
        position: 'top', // 显示在柱子顶部
        overflow: 'truncate', // 超出容器时截断
        ellipsis: '...', // 截断时显示省略号
        distance: 5, // 标签与柱子的距离
        // 仅在数据点可见且空间足够时显示
        showAbove: true, // 仅在柱子高度足够时显示
        formatter: ({ value }) => value // 显示数值
      }
    }],
    toolbox: {
      right: 20,
      feature: {
        saveAsImage: { title: '保存图片' },
        dataView: { title: '数据视图' }
      }
    },
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
  };

  chartInstance.setOption(option);

  window.addEventListener('resize', handleResize);
};

const truncateText = (text, maxLength) => {
  return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
};

const getColorByCount = (count) => {
  return count >= 1000 ? '#5470c6' 
       : count >= 950  ? '#91cc75' 
       : '#fac858';
};

const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
};

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 600px;
  min-width: 800px;
}
</style>