<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '350px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions(this.chartData)
    },
    setOptions({ autoTransPercent, assistTransPercent, transDataPercent, transFailPercent, transCorrectPercent } = {}) {
      this.chart.setOption({
        xAxis: {
          data: ['2019-01-01', '2019-02-01', '2019-03-01', '2019-04-01', '2019-05-01', '2019-06-01', '2019-07-01', '2019-08-01', '2019-09-01', '2019-10-01'],
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 10,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        legend: {
          data: ['自动译码率', '辅助译码率', '译出率', '译码失败率', '译码正确率']
        },
        series: [{
          name: '自动译码率', itemStyle: {
            normal: {
              color: '#FF005A',
              lineStyle: {
                color: '#FF005A',
                width: 2
              }
            }
          },
          smooth: true,
          type: 'line',
          data: autoTransPercent,
          animationDuration: 2800,
          animationEasing: 'cubicInOut'
        },
        {
          name: '辅助译码率',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: assistTransPercent,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '译出率',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#FFFF00',
              lineStyle: {
                color: '#FFFF00',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: transDataPercent,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '译码失败率',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#FF99FF',
              lineStyle: {
                color: '#FF99FF',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: transFailPercent,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: '译码正确率',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#66FFFF',
              lineStyle: {
                color: '#66FFFF',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data: transCorrectPercent,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        }]
      })
    }
  }
}
</script>
