import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
});


export const getDataStatus = () => api.get('/data_status');
export const getStatistics = () => api.get('/statistics');
export const industryResponse = () => api.get('/industry_distribution');
export const getCityjobcount = () => api.get('/citi_job_count');
export const getEducationSalary = () => api.get('/education_salary');
export const getCitySalary = () => api.get('/city_salary');
export const getIndustrySalary = () => api.get('/industry_salary');
export const getMajorSalary = () => api.get('/major_salary');
export const getProvinceStats = () => api.get('/province_stats');
export const getRecruitRatio = () => api.get('/recruit_ratio');
export const exportJobs = () => api.get('/export_jobs', { responseType: 'blob' });
