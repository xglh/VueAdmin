<template>
  <div class="app-container" style="width: 100%">
    <el-card style="margin-left:250px;width:50%">
    <el-form ref="form" :model="form" :rules="rules" :status-icon="status_icon" label-width="80px" style="margin-top: 20px;margin-left:30px;width: 60%">
      <el-form-item label="用户名：">
        {{ username }}
      </el-form-item>
      <el-form-item label="角色：">
        {{ roleName }}
      </el-form-item>
      <el-form-item label="手机号：" prop="phone">
        <el-input v-model="form.phone" />
      </el-form-item>
      <el-form-item label="邮箱：" prop="email">
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item label="头像：" prop="avatar">
        <el-input v-model="form.avatar" placeholder="请输入头像链接"/>
      </el-form-item>
      <el-form-item style="margin-left: 20px">
        <el-button type="primary" @click="onUpdateUser">保存</el-button>
        <el-button style="margin-left: 60px" @click="onReset">取消</el-button>
      </el-form-item>
    </el-form>
    </el-card>
  </div>
</template>
<script>
import { getRoleInfo, getUserInfo, updateUserInfo } from '@/api/user'
import { Message } from 'element-ui'
import store from '@/store'
export default {
  name: 'UserInfo',
  data() {
    var validate_phone = (rule, value, callback) => {
      if (value.length > 0 && value.length !== 11) {
        callback(new Error('请输入11位手机号'))
      }
      callback()
    }
    var validate_email = (rule, value, callback) => {
      var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
      if (!reg.test(value)) {
        callback(new Error('请输入正确的邮箱'))
      }
      callback()
    }
    var validate_avatar = (rule, value, callback) => {
      var reg = /^https?:.*/
      if (value.length > 0 && !reg.test(value)) {
        callback(new Error('请输入正确的链接'))
      }
      callback()
    }
    return {
      username: store.getters.username,
      role: '',
      roleName: '',
      form: {
        phone: '',
        email: '',
        avatar: ''
      },
      status_icon: true,
      rules: {
        phone: [
          { validator: validate_phone, trigger: 'blur' }
        ],
        email: [
          { validator: validate_email, trigger: 'blur' }
        ],
        avatar: [
          { validator: validate_avatar, trigger: 'blur' }
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
    fetchData: async function() {
      await getUserInfo(this.username).then(
        res => {
          const data = res.data
          this.role = data.roles[0]
          this.form.phone = data.phone
          this.form.email = data.email
          this.form.avatar = data.avatar
        }
      )
      getRoleInfo(this.role).then(
        res => {
          const data = res.data
          this.roleName = data.roleName
        }
      )
    },
    onUpdateUser() {
      updateUserInfo(this.username, this.form).then(
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
