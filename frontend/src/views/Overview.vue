<template>
  <div class="overview">
    <el-row :gutter="20">
      <el-col 
        :xs="24" 
        :sm="12" 
        :md="12" 
        :lg="6" 
        v-for="metric in metrics" 
        :key="metric.title"
      >
      <!-- 统计卡片 -->
      <!-- <el-col :span="6" v-for="metric in metrics" :key="metric.title"> -->
        <el-card shadow="hover" class="metric-card" >
          <div class="metric-title">{{ metric.title }}</div>
          <div class="metric-value">{{ metric.value }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近职位列表 -->
    <el-card shadow="never" class="recent-jobs">
      <div class="card-header">
        <span>最新职位</span>
        <el-tag type="info">最近更新</el-tag>
        <el-button type="primary" size="small" style="float:right" @click="handleExport">导出数据</el-button>
      </div>
      <el-table 
        :data="jobs" 
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="position" label="职位" width="220" />
        <el-table-column prop="company" label="公司" width="220" />
        <el-table-column label="薪资" width="150">
          <template #default="{ row }">
            {{ formatSalary(row.min_salary, row.max_salary) }}
          </template>
        </el-table-column>
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column label="要求" >
          <template #default="{ row }">
            {{ row.education }} | {{ row.experience }}
          </template>
        </el-table-column>
        <el-table-column prop="benefits" label="公司福利" width="380" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { exportJobs } from '../api'

const metrics = ref([
  { title: '总职位数', value: '加载中...' },
  { title: '覆盖城市', value: '加载中...' },
  { title: '最高薪资', value: '加载中...' },
  { title: '最低薪资', value: '加载中...' }
])

const jobs = ref([])
const loading = ref(true)

// 格式化薪资显示
const formatSalary = (min, max) => {
  return `¥${(min/1000).toFixed(1)}k-¥${(max/1000).toFixed(1)}k`
}

// 获取统计数据
const fetchMetrics = async () => {
  try {
    const res = await axios.get('/api/datacount') // 假设有独立统计接口
    metrics.value = [
      { title: '总职位数', value: res.data.jobs_count },
      { title: '覆盖城市', value: res.data.cities_count },
      { title: '最高平均薪资', value: `¥${(res.data.max_salary).toFixed(1)}` },
      { title: '最低平均薪资', value: `¥${(res.data.min_salary).toFixed(1)}` }
    ]
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取最新职位
const fetchJobs = async () => {
  try {
    const res = await axios.get('/api/jobs_new', {
      params: {
        limit: 5,
        order_by: '-created_at' // 按创建时间倒序
      }
    })
    jobs.value = res.data.results.map(job => ({
      ...job,
      avg_salary: (job.min_salary + job.max_salary) / 2
    }))
  } catch (error) {
    console.error('获取职位数据失败:', error)
    ElMessage.error('数据加载失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await Promise.all([fetchMetrics(), fetchJobs()])
})

const handleExport = async () => {
  try {
    const res = await exportJobs();
    const blob = new Blob([res.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'jobs_export.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    alert('导出失败: ' + (e?.message || '未知错误'));
  }
}
</script>

<style scoped>
/* 新增卡片尺寸样式 */
.metric-card {
  height: 120px;  /* 固定高度 */
  margin-bottom: 20px;  /* 底部间距 */
}

.metric-content {
  padding: 1%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.card-header {
    line-height: 80px;
    height: 80px;
    text-align: center;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .metric-card {
    height: auto;
    min-height: 100px;
  }
  
  .metric-title {
    font-size: 14px;
  }
  
  .metric-value {
    font-size: 20px;
  }
}

/* 原有样式优化 */
.metric-title {
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.4;
}

.metric-value {
  font-size: 24px;
  font-weight: 600;
  color: #409eff;
  line-height: 1.2;
}
</style>