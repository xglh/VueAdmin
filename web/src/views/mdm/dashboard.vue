<template>
  <div class="dashboard-editor-container">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <div style="text-align: center">译码数据</div>
      <div style="margin-left: 40px;margin-top: 10px">
        <span>选择品牌：</span>
        <el-select v-model="brandOptionValue" placeholder="选择品牌" clearable style="width: 120px;margin-left: 0px" class="filter-item">
          <el-option v-for="item in brandOptions" :key="item.key" :label="item.label" :value="item.value" />
        </el-select>
        <span style="margin-left: 30px">选择日期：</span>
        <el-date-picker
          v-model="value1"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        />
      </div>
      <line-chart :chart-data="lineChartData" style="margin-top: 10px" />
    </el-row>

  </div>
</template>

<script>
import LineChart from './components/LineChart'

const lineChartData = {
  transLineData: {
    autoTransPercent: [100, 120, 161, 134, 105, 160, 165, 100, 120, 161],
    assistTransPercent: [120, 82, 91, 154, 162, 140, 145, 120, 82, 91, 154],
    transDataPercent: [90, 110, 151, 114, 95, 150, 155, 90, 110, 151],
    transFailPercent: [115, 77, 86, 149, 157, 135, 140, 115, 77, 86, 139],
    transCorrectPercent: [80, 100, 141, 114, 85, 140, 145, 80, 100, 141]
  }
  // messages: {
  //   expectedData: [200, 192, 120, 144, 160, 130, 140],
  //   actualData: [180, 160, 151, 106, 145, 150, 130]
  // },
  // purchases: {
  //   expectedData: [80, 100, 121, 104, 105, 90, 100],
  //   actualData: [120, 90, 100, 138, 142, 130, 130]
  // },
  // shoppings: {
  //   expectedData: [130, 140, 141, 142, 145, 150, 160],
  //   actualData: [120, 82, 91, 154, 162, 140, 130]
  // }
}

export default {
  name: 'DashboardAdmin',
  components: {
    LineChart
  },
  data() {
    return {
      lineChartData: lineChartData.transLineData,
      brandOptionValue: '',
      brandOptions: [
        {
          value: '',
          label: '全部'
        }, {
          value: '宝马',
          label: '宝马'
        }

      ]
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type]
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
