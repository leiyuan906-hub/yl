<template>
  <el-container class="layout-container-demo" style="height: 760px">
    <el-aside width="180px">
      <el-menu
        :router="true"
        :default-active="route?.path || '/overview'"
        class="el-menu-vertical-demo"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item index="/overview">
          <el-icon><IconMenu /></el-icon>
          <template #title>职位总览</template>
        </el-menu-item>
        
        <el-menu-item index="/search">
          <el-icon><Document /></el-icon>
          <template #title>职位搜索</template>
        </el-menu-item>

        <el-sub-menu index="1">
          <template #title>
            <el-icon><Location /></el-icon>
            <span>数据可视化</span>
          </template>
          <el-menu-item index="/visual/education-salary">教育背景与薪资</el-menu-item>
          <el-menu-item index="/visual/industry-salary">行业薪资分布</el-menu-item>
          <el-menu-item index="/visual/major-salary">专业/关键词薪资</el-menu-item>
          <el-menu-item index="/visual/china-map">中国地图热力图</el-menu-item>
          <el-menu-item index="/visual/recruit-ratio">招聘数量分布图</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>招聘数据分析平台</el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { Document, Menu as IconMenu, Location } from '@element-plus/icons-vue'

const route = useRoute()
</script>
<style>
.el-container {
  height: 100%;
}

.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color:#545c64;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

.el-menu {
  background-color: #d3dce6;
}

</style>