import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

/**
 * 通用图表管理Hook
 * @param {Object} options - 配置选项
 * @param {string} options.domId - 图表DOM元素ID
 * @param {Object} [options.initOptions] - 初始化图表选项
 * @returns {Object} 图表操作方法和实例
 */
export function useChart(options) {
  const chartInstance = ref(null)

  // 初始化图表
  const initChart = () => {
    const dom = document.getElementById(options.domId)
    if (dom) {
      chartInstance.value = echarts.init(dom)
      if (options.initOptions) {
        chartInstance.value.setOption(options.initOptions)
      }
    }
  }

  // 更新图表数据
  const updateChart = (option) => {
    if (chartInstance.value) {
      chartInstance.value.setOption(option)
    }
  }

  // 调整图表大小
  const resizeChart = () => {
    chartInstance.value?.resize()
  }

  // 销毁图表
  const destroyChart = () => {
    if (chartInstance.value) {
      chartInstance.value.dispose()
      chartInstance.value = null
    }
  }

  onMounted(() => {
    initChart()
    window.addEventListener('resize', resizeChart)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', resizeChart)
    destroyChart()
  })

  return {
    chartInstance,
    updateChart,
    resizeChart,
    destroyChart
  }
}

/**
 * 创建多图表管理Hook
 * @param {Array<Object>} chartsConfig - 图表配置数组
 * @returns {Object} 多图表操作方法和实例
 */
export function useMultipleCharts(chartsConfig) {
  const charts = ref({})
  
  // 初始化所有图表
  const initAllCharts = () => {
    chartsConfig.forEach(config => {
      const dom = document.getElementById(config.domId)
      if (dom) {
        charts.value[config.domId] = echarts.init(dom)
        if (config.initOptions) {
          charts.value[config.domId].setOption(config.initOptions)
        }
      }
    })
  }
  
  // 更新指定图表
  const updateChart = (domId, option) => {
    if (charts.value[domId]) {
      charts.value[domId].setOption(option)
    }
  }
  
  // 调整所有图表大小
  const resizeAllCharts = () => {
    Object.values(charts.value).forEach(chart => {
      chart?.resize()
    })
  }
  
  // 销毁所有图表
  const destroyAllCharts = () => {
    Object.values(charts.value).forEach(chart => {
      if (chart) {
        chart.dispose()
      }
    })
    charts.value = {}
  }
  
  onMounted(() => {
    initAllCharts()
    window.addEventListener('resize', resizeAllCharts)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', resizeAllCharts)
    destroyAllCharts()
  })
  
  return {
    charts,
    updateChart,
    resizeAllCharts,
    destroyAllCharts
  }
}

/**
 * 创建响应式图表配置Hook
 * @param {Function} configFactory - 返回图表配置的工厂函数
 * @returns {Function} 根据数据生成图表配置的函数
 */
export function useChartOptions(configFactory) {
  return (data) => {
    return configFactory(data)
  }
}

export default {
  useChart,
  useMultipleCharts,
  useChartOptions
}