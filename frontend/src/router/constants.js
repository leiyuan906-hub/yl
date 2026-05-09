/**
 * 路由常量配置文件
 * 集中管理所有前端路由路径和API请求路径
 * 避免硬编码，提高代码可维护性
 */

/**
 * 前端路由路径常量
 * 用于Vue Router导航和菜单配置
 */
export const ROUTES = {
  // 主页/仪表盘路由 - 显示数据概览和搜索功能
  DASHBOARD: '/',
  
  // 各类数据分析页面路由
  CITY_ANALYSIS: '/city',       // 城市分布分析页面
  EXPERIENCE_ANALYSIS: '/experience',  // 工作经验分析页面
  EDUCATION_ANALYSIS: '/education',    // 教育背景分析页面
  SALARY_ANALYSIS: '/salary',          // 薪资水平分析页面
  
  // 数据管理页面路由 - 提供数据更新和维护功能
  DATA_MANAGEMENT: '/data-management'
}

/**
 * API请求路径常量
 * 用于前端与后端API通信
 * 按业务模块分类组织
 */
export const API_ROUTES = {
  
  // 数据分析相关API
  CITY_JOB_COUNT: '/api/citi_job_count',    // 获取城市职位数量统计
  EDUCATION_SALARY: '/api/education_salary', // 获取教育程度薪资统计
  CITY_SALARY: '/api/city_salary',          // 获取城市薪资统计
  INDUSTRY_SALARY: '/api/industry_salary',   // 获取行业薪资统计
  MAJOR_SALARY: '/api/major_salary',         // 获取专业薪资统计
  
  // 数据管理相关API
  DATA_STATUS: '/api/data_status',    // 获取数据状态信息
  UPDATE_DATA: '/api/update_data',    // 触发数据更新操作
  STATISTICS: '/api/statistics'        // 获取平台整体统计数据
}

export default {
  ROUTES,
  API_ROUTES
}