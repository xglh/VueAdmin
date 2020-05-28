<template>
  <div class="app-container" style="width: 100%">
    <el-card style="margin-left:250px;width:50%">
    <el-form ref="form" :model="form" :rules="rules" :status-icon="status_icon" label-width="80px" style="margin-top: 20px;margin-left:30px;width: 60%">
      <el-form-item label="角色：">
        {{ role_update }}
      </el-form-item>
      <el-form-item label="名称：" prop="roleName">
        <el-input v-model="form.roleName" />
      </el-form-item>
      <el-form-item style="margin-left: 20px">
        <el-button type="primary" @click="onUpdateRole">保存</el-button>
        <el-button style="margin-left: 60px" @click="onReset">取消</el-button>
      </el-form-item>
    </el-form>
    </el-card>
  </div>
</template>
<script>
import { getRoleInfo, updateRoleInfo } from '@/api/user'
import { Message } from 'element-ui'

export default {
  name: 'RoleUpdate',
  data() {
    return {
      role_update: '',
      form: {
        roleName: ''
      },
      status_icon: true,
      rules: {
        roleName: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 3, max: 24, message: '长度在 3 到 24 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    '$route': 'fetchData'
  },
  created() {
    // 组件创建完后获取数据，
    // 此时 data 已经被 observed 了
    this.fetchData()
  },
  methods: {
    fetchData() {
      const role_update = this.$route.params.role
      this.role_update = role_update
      // replace getPost with your data fetching util / API wrapper
      getRoleInfo(role_update).then(
        res => {
          const data = res.data
          this.form.roleName = data.roleName
        }
      )
    },
    onUpdateRole() {
      this.form.role = this.roleTypeVaule
      updateRoleInfo(this.role_update, this.form).then(
        res => {
          if (res.success) {
            Message({
              type: 'success',
              message: '修改成功!',
              duration: 1500
            })
            this.fetchData()
          }
        }
      )
    },
    // 返回上级页面
    onReset() {
      this.$store.dispatch('tagsView/delVisitedView', this.$route)
      this.$router.go(-1)
    }
  }
}
</script>
