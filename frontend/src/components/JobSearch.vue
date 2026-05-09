<template>
  <div class="job-container">
    <!-- 搜索框 -->
    <div class="search-box">
      <input
        v-model="searchKeyword"
        @keyup.enter="loadJobs"
        placeholder="输入职位、公司或技能..."
        class="search-input"
      />
      <button @click="loadJobs" class="search-button">
        <span class="icon">🔍</span> 搜索
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 数据表格 -->
    <div v-else class="table-wrapper">
      <!-- 空状态 -->
      <div v-if="jobs.length === 0" class="empty">暂无职位信息</div>

      <!-- 表格容器 -->
      <table v-else class="job-table">
        <thead>
          <tr>
            <th>职位</th>
            <th>城市</th>
            <th>公司</th>
            <th>薪资范围</th>
            <th>经验</th>
            <th>学历</th>
            <th>行业</th>
            <th>技能要求</th>
            <th>福利</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id">
            <td>{{ job.position || '-' }}</td>
            <td>{{ job.city || '-' }}</td>
            <td class="company-cell">{{ job.company || '-' }}</td>
            <td>
              <span v-if="job.min_salary || job.max_salary">
                ¥{{ job.min_salary || '面议' }} - ¥{{ job.max_salary || '面议' }}
              </span>
              <span v-else>{{ job.salary || '面议' }}</span>
            </td>
            <td>{{ job.experience || '不限' }}</td>
            <td>{{ job.education || '不限' }}</td>
            <td>{{ job.industry || '-' }}</td>
            <td>
              <div class="tags">
                <span 
                  v-for="(skill, index) in formatSkills(job.skills)" 
                  :key="index" 
                  class="tag skill-tag"
                >
                  {{ skill }}
                </span>
              </div>
            </td>
            <td>
              <div class="tags">
                <span 
                  v-for="(benefit, index) in formatBenefits(job.benefits)" 
                  :key="index" 
                  class="tag benefit-tag"
                >
                  {{ benefit }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页控件 -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1" class="pagination-button">
          上一页
        </button>
        <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
        <button @click="nextPage" :disabled="currentPage >= totalPages" class="pagination-button">
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue';

const jobs = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const searchKeyword = ref('');
const loading = ref(false);

// 初始化加载
onMounted(() => {
  loadJobs();
});

// 加载数据
const loadJobs = async () => {
  try {
    loading.value = true;
    const response = await fetch(
      `/api/jobs?page=${currentPage.value}&per_page=20&keyword=${encodeURIComponent(searchKeyword.value)}`
    );
    if (!response.ok) throw new Error('请求失败');
    const data = await response.json();
    
    jobs.value = data.jobs;
    totalPages.value = Math.max(data.total_pages || 1, 1);
    currentPage.value = data.current_page;
  } catch (error) {
    console.error('加载失败:', error);
    alert('数据加载失败，请稍后重试！');
  } finally {
    loading.value = false;
  }
};

// 格式化技能字段（假设 skills 存储为逗号分隔的字符串）
const formatSkills = (skills) => {
  return skills ? skills.split(',').filter(s => s.trim()) : [];
};

// 格式化福利字段
const formatBenefits = (benefits) => {
  return benefits ? benefits.split(',').filter(b => b.trim()) : [];
};

// 分页操作
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    loadJobs();
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    loadJobs();
  }
};
</script>

<style scoped>
/* 基础容器 */
.job-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

/* 搜索框样式 */
.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.search-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #007bff;
  outline: none;
}

.search-button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
}

.search-button:hover {
  background: #0056b3;
}

.icon {
  font-size: 16px;
}

/* 表格样式 */
.table-wrapper {
  overflow-x: auto;
  border-radius: 6px;
  background: #fff;
  line-height: 20px;
  
}

.job-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}

.job-table th,
.job-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  text-align: left;
  min-width: 20px;
  max-height: 20px;
}

.job-table th {
  background: #f8f9fa;
  color: #333;
  font-weight: 6px;
  white-space: nowrap;
}

.job-table tbody tr:hover {

  background: #f5f6fa;
}


/* 分页样式 */
.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.pagination-button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.pagination-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 14px;
}

/* 空状态与加载状态 */
.empty, .loading {
  padding: 40px;
  text-align: center;
  color: #888;
  font-size: 16px;
  background: #f8f9fa;
  border-radius: 6px;
}
</style>