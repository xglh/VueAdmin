<template>
  <div class="app-container" style="margin-top: 100px;margin-left:400px;width: 50%">
    <el-form ref="form" :model="form" :rules="rules" label-width="100px" style="width: 50%">
      <el-form-item label="角色：" prop="role">
        <el-input v-model="form.role" placeholder="3-24位长度" />
      </el-form-item>
      <el-form-item label="名称：" prop="roleName">
        <el-input v-model="form.roleName" placeholder="3-24位长度"/>
      </el-form-item>
      <el-form-item style="margin-left: 30px">
        <el-button type="primary" @click="onCreateUser">创建</el-button>
        <el-button style="margin-left: 60px" @click="onReset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { createRole } from '@/api/user'
import { Message } from 'element-ui'
export default {
  name: 'UserCreate',
  data() {
    return {
      loading: false,
      form: {
        role: '',
        roleName: ''
      },

      rules: {
        role: [
          { required: true, message: '请输入角色', trigger: 'blur' },
          { min: 3, max: 24, message: '长度在 3 到 24 个字符', trigger: 'blur' }
        ],
        roleName: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 3, max: 24, message: '长度在 3 到 24 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    // 组件创建完后获取数据，
  },
  methods: {
    onCreateUser() {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          createRole(this.form).then(
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
