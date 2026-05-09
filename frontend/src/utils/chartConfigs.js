/**
 * 图表配置工具函数
 * 提供各种图表的默认配置，减少视图组件中的重复代码
 */

// 饼图默认配置
export const getPieChartConfig = (title, data, options = {}) => {
  return {
    title: { text: title },
    tooltip: { trigger: 'item' },
    series: [{
      name: options.seriesName || '数量',
      type: 'pie',
      radius: options.radius || '50%',
      data: data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      ...options.series
    }]
  }
}

// 柱状图默认配置
export const getBarChartConfig = (title, xData, yData, options = {}) => {
  return {
    title: { text: title },
    tooltip: { trigger: 'axis' },
    xAxis: { 
      type: 'category',
      data: xData,
      name: options.xAxisName || '',
      axisLabel: options.axisLabel || {}
    },
    yAxis: { 
      type: 'value',
      name: options.yAxisName || ''
    },
    series: [{
      name: options.seriesName || '数量',
      type: 'bar',
      data: yData,
      itemStyle: {
        color: options.color || '#409EFF'
      },
      ...options.series
    }]
  }
}

// 折线图默认配置
export const getLineChartConfig = (title, xData, series, options = {}) => {
  return {
    title: { text: title },
    tooltip: { trigger: 'axis' },
    xAxis: { 
      type: 'category',
      data: xData,
      name: options.xAxisName || ''
    },
    yAxis: { 
      type: 'value',
      name: options.yAxisName || ''
    },
    series: series,
    ...options
  }
}

// 多系列图表配置
export const getMultiSeriesConfig = (title, xData, seriesData, options = {}) => {
  return {
    title: { text: title },
    tooltip: { trigger: 'axis' },
    legend: options.legend || {},
    xAxis: { 
      type: 'category',
      data: xData,
      name: options.xAxisName || ''
    },
    yAxis: { 
      type: 'value',
      name: options.yAxisName || ''
    },
    series: seriesData,
    ...options
  }
}

export default {
  getPieChartConfig,
  getBarChartConfig,
  getLineChartConfig,
  getMultiSeriesConfig
}