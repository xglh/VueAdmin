<template>
  <div class="app-container" style="width: 100%">
     <el-card style="margin-left:250px;width:50%">
    <el-form ref="form" :model="form" :rules="rules" :status-icon="status_icon" label-width="100px" style="margin-top: 20px;margin-left:30px;width: 60%">
      <el-form-item label="密码：" prop="password">
        <el-input v-model="form.password" placeholder="6-24位长度" type="password" />
      </el-form-item>
      <el-form-item label="确认密码：" prop="re_password">
        <el-input v-model="form.re_password" placeholder="6-24位长度" type="password" />
      </el-form-item>
      <el-form-item style="margin-left: 20px">
        <el-button type="primary" @click="onUpdatePassword">保存</el-button>
        <el-button style="margin-left: 30px" @click="onReset">重置</el-button>
      </el-form-item>
    </el-form>
     </el-card>
  </div>
</template>
<script>
import { updateUserInfo } from '@/api/user'
import { Message } from 'element-ui'
import store from '@/store'

export default {
  name: 'ProfileUpdatePassword',
  data() {
    var validate_re_password = (rule, value, callback) => {
      if (value.length < 6 || value.length > 24) {
        callback(new Error('请输入正确的密码'))
      } else if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致!'))
      }
      callback()
    }
    return {
      form: {
        password: '',
        re_password: ''
      },
      status_icon: true,
      rules: {
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 24, message: '长度在 3 到 24 个字符', trigger: 'blur' }
        ],
        re_password: [
          { validator: validate_re_password, trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    // 组件创建完后获取数据，
  },
  methods: {
    onUpdatePassword() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          updateUserInfo(store.getters.username, this.form).then(
            res => {
              if (res.success) {
                Message({
                  type: 'success',
                  message: '修改成功!',
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
