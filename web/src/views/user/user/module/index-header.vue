<template>
  <div class="head-container">
    <!-- 搜索 -->
    <el-input
      v-model="listQuery.search"
      clearable
      placeholder="输入名称搜索"
      style="width: 250px;"
      class="filter-item"
      @keyup.enter.native="handleQueryUsers"
    />
    <el-button
      class="filter-item"
      type="primary"
      icon="el-icon-search"
      style="margin-left: 10px"
      @click="handleQueryUsers"
    >搜索
    </el-button>

    <el-button
      class="filter-item"
      type="primary"
      icon="el-icon-plus"
      style="margin-left: 10px"
      @click="handleShowCreateDialog"
    >新增用户
    </el-button>
    <!-- 新增 -->
    <el-button
      class="filter-item"
      type="danger"
      icon="el-icon-delete"
      style="margin-left: 10px"
      @click="handleDeleteUsers"
    >删除用户
    </el-button>
    <el-button
      class="filter-item"
      type="primary"
      icon="el-icon-refresh"
      style="margin-left: 10px"
      @click="handleRefresh"
    >刷新
    </el-button>
    <el-dialog title="新增用户" :visible="dialogFormVisible" :before-close="dialogFormClose">
      <el-form
        ref="form"
        v-loading="formLoading"
        :model="form"
        :rules="rules"
        label-width="120px"
        style="width: 500px; margin-left:50px;"
        :status-icon="status_icon"
      >

        <el-form-item label="用户名：" prop="username">
          <el-input v-model="form.username" placeholder="3-24位长度" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="密码：" prop="password">
          <el-input v-model="form.password" placeholder="6-24位长度" type="password" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="确认密码：" prop="re_password">
          <el-input v-model="form.re_password" placeholder="6-24位长度" type="password" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="角色：" prop="role">
          <el-select v-model="roleIdVaule" placeholder="请选择" style="width: 300px" @change="onRoleChange">
            <el-option
              v-for="item in roleIdOptinos"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号：" prop="phone">
          <el-input v-model="form.phone" style="width: 300px;" />
        </el-form-item>
        <el-form-item label="邮箱：" prop="email">
          <el-input v-model="form.email" style="width: 300px;" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button style="margin-left: 30px" @click="dialogFormClose">取 消
        </el-button>
        <el-button type="primary" @click="handleCreateUser">确 定
        </el-button>

      </div>

    </el-dialog>
  </div>
</template>

<script>
import { createUser, getRoles } from '@/api/user'
import { Message } from 'element-ui'

export default {
  name: 'UserCreateHeader',
  props: {
    listQuery: {
      type: Object,
      required: true
    },
    deleteUserList: {
      type: Array,
      required: true
    }
  },
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
      if (value && !reg.test(value)) {
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
      dialogFormVisible: false,
      formLoading: false,
      roleValue: '',
      roleIdVaule: '',
      roleIdOptinos: [],
      form: this.getInitFormData(),
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
  watch: {
    dialogFormVisible(val) {
      if (val === true) {
        this.getRoleList()
      }
      this.roleIdVaule = ''
      this.roleIdOptinos = []
      this.form = this.getInitFormData()
    }
  },
  created() {
  },
  methods: {
    getRoleList() {
      this.formLoading = true
      setTimeout(() => {
        this.formLoading = false
      }, 5 * 1000)
      getRoles().then(response => {
        var roleList = response.data.rows
        roleList.forEach(data => {
          // this.roleNameInfo[data.role] = data.roleName
          this.roleIdOptinos.push({
            value: data.id,
            label: data.roleName
          })
          this.formLoading = false
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
    getInitFormData() {
      return {
        username: '',
        password: '',
        re_password: '',
        role_id: '',
        phone: '',
        email: ''
      }
    },
    handleShowCreateDialog() {
      this.dialogFormVisible = true
    },
    handleQueryUsers() {
      this.$parent.page = 1
      this.$parent.fetchData()
    },
    handleDeleteUsers() {},
    dialogFormClose() {
      this.dialogFormVisible = false
    },
    onRoleChange(val) {
      this.roleIdVaule = val
    },
    handleCreateUser() {
      this.$refs['form'].validate(
        (valid) => {
          if (valid) {
            this.form.role_id = this.roleIdVaule
            createUser(this.form).then(
              res => {
                if (res.success) {
                  this.$message(
                    {
                      type: 'success',
                      message: '创建成功!',
                      duration: 1500
                    }
                  )
                  this.dialogFormVisible = false
                  this.$parent.fetchData()
                }
              }
            ).catch()
          } else {
            return false
          }
        }
      )
    },
    handleRefresh() {
      this.$parent.fetchData()
    }
  }
}
</script>
