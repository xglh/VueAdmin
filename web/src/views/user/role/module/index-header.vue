<template>
  <div class="head-container">
    <!-- 搜索 -->
    <el-input
      v-model="listQuery.search"
      clearable
      placeholder="输入名称搜索"
      style="width: 250px;"
      class="filter-item"
      @keyup.enter.native="handleQueryRoles"
    />
    <el-button
      class="filter-item"
      type="primary"
      icon="el-icon-search"
      style="margin-left: 10px"
      @click="handleQueryRoles"
    >搜索
    </el-button>

    <el-button
      class="filter-item"
      type="primary"
      icon="el-icon-plus"
      style="margin-left: 10px"
      @click="handleShowCreateDialog"
    >新增角色
    </el-button>
    <!-- 新增 -->
    <el-button
      class="filter-item"
      type="danger"
      icon="el-icon-delete"
      style="margin-left: 10px"
      @click="handleDeleteRoles"
    >删除角色
    </el-button>
    <el-button
      class="filter-item"
      type="primary"
      icon="el-icon-refresh"
      style="margin-left: 10px"
      @click="handleRefresh"
    >刷新
    </el-button>
    <el-dialog title="新增角色" :visible="dialogFormVisible" :before-close="dialogFormClose">
      <el-form
        ref="form"
        v-loading="formLoading"
        :model="form"
        :rules="rules"
        label-width="120px"
        style="width: 400px; margin-left:50px;"
        :status-icon="status_icon"
      >

        <el-form-item label="角色：" prop="role">
          <el-input v-model="form.role" placeholder="3-24位长度" style="width: 300px" />
        </el-form-item>
        <el-form-item label="名称：" prop="roleName">
          <el-input v-model="form.roleName" placeholder="3-24位长度" style="width: 300px" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button style="margin-left: 30px" @click="dialogFormVisible = false;resetForm()">取 消
        </el-button>
        <el-button type="primary" @click="handleCreateRole">确 定
        </el-button>

      </div>

    </el-dialog>
  </div>
</template>

<script>
import { Message } from 'element-ui'
import { createRole, deleteRoles } from '@/api/user'

export default {
  name: 'RoleIndexHeader',
  props: {
    listQuery: {
      type: Object,
      required: true
    },
    deleteRoleList: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      dialogFormVisible: false,
      formLoading: false,
      form: this.getInitFormData(),
      status_icon: true,
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
  watch: {
    dialogFormVisible() {
      this.form = this.getInitFormData()
    }
  },
  created() {
  },
  methods: {

    getInitFormData() {
      return {
        role: '',
        roleName: ''
      }
    },

    handleQueryRoles() {
      this.$parent.page = 1
      this.$parent.fetchData()
    },
    handleShowCreateDialog() {
      this.dialogFormVisible = true
    },
    handleCreateRole() {
      this.$refs['form'].validate(
        (valid) => {
          if (valid) {
            createRole(this.form).then(
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
                this.resetForm()
              }
            ).catch(err => {
              this.$message(
                {
                  type: 'error',
                  message: err.msg || '创建失败！',
                  duration: 1500
                }
              )
            })
          } else {
            return false
          }
        }
      )
    },
    resetForm() {
      this.$refs.form.resetFields()
    },
    handleDeleteRoles() {
      var targetDeleteRoleList = []
      this.deleteRoleList.forEach(data => {
        targetDeleteRoleList.push(data.id)
      })
      if (targetDeleteRoleList.length === 0) {
        Message({
          showClose: true,
          message: '请至少选中一条记录',
          duration: 1500,
          type: 'error'
        })
      } else {
        this.$confirm('确认删除选中角色?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteRoles(targetDeleteRoleList).then(
            res => {
              if (res.success) {
                Message({
                  type: 'success',
                  message: '删除成功!',
                  duration: 1500
                })
                this.handleRefresh()
              }
            }
          )
        }).catch(() => {
        })
      }
    },
    dialogFormClose() {
      this.dialogFormVisible = false
    },
    handleRefresh() {
      this.$parent.fetchData()
    }
  }
}
</script>
