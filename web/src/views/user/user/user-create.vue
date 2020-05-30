<template>
  <div class="app-container" style="width: 100%">
    <el-card style="margin-left:250px;width:50%">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        :status-icon="status_icon"
        label-width="100px"
        style="margin-top: 20px;margin-left:30px;width: 60%"
      >
        <el-form-item label="用户名：" prop="username">
          <el-input v-model="form.username" placeholder="3-24位长度" />
        </el-form-item>
        <el-form-item label="密码：" prop="password">
          <el-input v-model="form.password" placeholder="6-24位长度" type="password" />
        </el-form-item>
        <el-form-item label="确认密码：" prop="re_password">
          <el-input v-model="form.re_password" placeholder="6-24位长度" type="password" />
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
          <el-button type="primary" @click="onCreateUser">创建</el-button>
          <el-button style="margin-left: 60px" @click="onReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import { createUser, getRoles } from '@/api/user'
import { Message } from 'element-ui'

export default {
  name: 'UserCreate',
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
    var validate_re_password = (rule, value, callback) => {
      if (value.length < 6 || value.length > 24) {
        callback(new Error('请输入正确的密码'))
      } else if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致!'))
      }
      callback()
    }
    return {
      roleValue: '',
      roleIdVaule: '',
      roleIdOptinos: [],
      form: {
        username: '',
        password: '',
        re_password: '',
        role_id: '',
        phone: '',
        email: ''
      },
      status_icon: true,
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 24, message: '长度在 3 到 24 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 24, message: '长度在 3 到 24 个字符', trigger: 'blur' }
        ],
        re_password: [
          { validator: validate_re_password, trigger: 'blur' }
        ],
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
  created() {
    // 组件创建完后获取数据，
    this.getRoleList()
  },
  methods: {
    getRoleList() {
      getRoles().then(response => {
        var roleList = response.data.rows
        roleList.forEach(data => {
          // this.roleNameInfo[data.role] = data.roleName
          this.roleIdOptinos.push({
            value: data.id,
            label: data.roleName
          })
        })
      })
    },
    onCreateUser() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.form.role_id = this.roleIdVaule
          createUser(this.form).then(
            res => {
              if (res.success) {
                Message({
                  type: 'success',
                  message: '创建成功!',
                  duration: 1500
                })
                this.onReset()
              }
            }
          )
        } else {
          return false
        }
      })
    },
    onReset() {
      this.$refs['form'].resetFields()
    }
  }
}
</script>
