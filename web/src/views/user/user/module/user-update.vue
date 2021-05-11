<template>
  <div class="app-container" style="width: 100%">
    <el-card style="margin-left:250px;width:50%">
      <el-form ref="form" :model="form" :rules="rules" :status-icon="status_icon" label-width="80px" style="margin-top: 20px;margin-left:30px;width: 60%">
        <el-form-item label="用户名：">
          {{ username_update }}
        </el-form-item>
        <el-form-item label="角色：" prop="role">
          <el-select v-model="roleIdVaule" placeholder="请选择" style="width: 100%">
            <el-option
              v-for="item in roleIdOptinos"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号：" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱：" prop="email">
          <el-input v-model="form.email" />
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
import { getUserInfo, updateUserInfo, getRoles } from '@/api/user'
import { Message } from 'element-ui'

export default {
  name: 'UserUpdate',
  data() {
    // 自定义phone校验
    var validate_role = (rule, value, callback) => {
      if (this.roleIdVaule === '') {
        callback(new Error('请选中角色'))
      }
      callback()
    }
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
    return {
      username_update: '',
      form: {
        role_id: '',
        phone: '',
        email: ''
      },
      roleIdVaule: '',
      roleIdOptinos: [
      ],
      roleNameInfo: {},
      status_icon: true,
      rules: {
        role: [
          { validator: validate_role, trigger: 'blur' }
        ],
        phone: [
          { validator: validate_phone, trigger: 'blur' }
        ],
        email: [
          { validator: validate_email, trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    // 如果路由有变化，会再次执行该方法
    // '$route': 'fetchData'
  },
  created() {
    // 组件创建完后获取数据，
    // 此时 data 已经被 observed 了
    this.fetchData()
  },
  methods: {
    fetchData: async function() {
      await getRoles().then(response => {
        var roleList = response.data.rows
        roleList.forEach(data => {
          this.roleNameInfo[data.role] = data.id
          this.roleIdOptinos.push({
            value: data.id,
            label: data.roleName
          })
        })
      })

      const username_update = this.$route.params.username
      this.username_update = username_update
      // replace getPost with your data fetching util / API wrapper
      getUserInfo(username_update).then(
        res => {
          const data = res.data
          this.form.phone = data.phone
          this.form.email = data.email
          this.roleIdVaule = this.roleNameInfo[data.roles[0]]
        }
      )
    },
    onUpdateUser() {
      this.form.role_id = this.roleIdVaule
      updateUserInfo(this.username_update, this.form).then(
        res => {
          if (res.success) {
            Message({
              type: 'success',
              message: '修改成功!',
              duration: 1500
            })
            this.roleIdOptinos = []
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
