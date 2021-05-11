<template>
  <div class="app-container">
    <UserCreateHeader :list-query="listQuery" :delete-user-list="deleteUserList" />
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="userList"
      border
      fit
      highlight-current-row
      style="width: 100%;margin-top: 15px;"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        width="40"
      />
      <el-table-column label="ID" type="index" align="center" width="40" />
      <el-table-column label="用户名" prop="username" align="center" />
      <el-table-column label="角色" align="center">
        <template slot-scope="{row}">
          <span v-if="row.roles[0]==='admin'"><el-tag>管理员</el-tag></span>
          <span v-else>{{ getRoleName(row.roles[0]) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="邮箱" prop="email" align="center" width="300" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width" width="240">
        <template slot-scope="{row}">
          <el-button size="mini" type="primary" @click="handleUpdateUser(row.username)">
            编辑
          </el-button>
          <el-button size="mini" type="success" @click="handleUpdatePassword(row.username)">
            重置密码
          </el-button>
          <el-button size="mini" type="danger" @click="handleDeleteUser(row.username)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.size"
      @pagination="getUserInfoList"
    />
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { getUsers, deleteUser, deleteUsers, getRoles, updateUserInfo } from '@/api/user'
import { Message } from 'element-ui'
import UserCreateHeader from './module/index-header'
export default {
  name: 'UserList',
  components: { Pagination, UserCreateHeader },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      userList: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 10,
        search: '',
        ordering: ''
      },
      roleIdVaule: '',
      roleIdOptinos: [
        {
          value: '',
          label: '全部'
        }
      ],
      deleteUserList: [],
      roleNameInfo: {}
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData: async function() {
      this.listLoading = true
      setTimeout(() => {
        this.listLoading = false
      }, 5 * 1000)
      await this.getRoleList()
      this.getUserInfoList()
    },
    getRoleList() {
      getRoles().then(response => {
        var roleList = response.data.rows
        roleList.forEach(data => {
          this.roleNameInfo[data.role] = data.roleName
          this.roleIdOptinos.push({
            value: data.id,
            label: data.roleName
          })
        })
      })
    },
    getUserInfoList() {
      getUsers(this.roleIdVaule, this.listQuery.page, this.listQuery.size).then(response => {
        this.userList = response.data.rows
        this.total = response.data.total
        this.listLoading = false
      })
    },
    getRoleName(role) {
      return this.roleNameInfo[role]
    },
    handleRoleTypeFilter() {
      this.listQuery.page = 1
      this.getUserInfoList()
    },
    handleDeleteUsers() {
      var deleteUserNameList = []
      this.deleteUserList.forEach(data => {
        deleteUserNameList.push(data.username)
      })
      if (deleteUserNameList.length === 0) {
        Message({
          showClose: true,
          message: '请至少选中一条记录',
          duration: 1500,
          type: 'error'
        })
      } else {
        this.$confirm('确认删除选中用户?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deleteUsers(deleteUserNameList).then(
            res => {
              console.log(res)
              if (res.success) {
                Message({
                  type: 'success',
                  message: '删除成功!',
                  duration: 1500
                })
                this.fetchData()
              }
            }
          )
        }).catch(() => {
        })
      }
    },
    handleDeleteUser(username) {
      this.$confirm('确认删除选中用户?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteUser(username).then(
          res => {
            if (res.success) {
              Message({
                type: 'success',
                message: '删除成功!',
                duration: 1500
              })
              this.fetchData()
            }
          }
        )
      }).catch(() => {
      })
    },
    handleSelectionChange(val) {
      this.deleteUserList = val
    },
    handleUpdatePassword(username) {
      this.$prompt('请输入密码：', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPlaceholder: '请输入6-24位密码',
        inputPattern: /^.{6,24}$/,
        inputErrorMessage: '请输入6-24位密码'
      }).then(({ value }) => {
        if (value.length < 6 || value.length > 24) {
          this.$message({
            type: 'error',
            message: '请输入6-24位密码'
          })
        } else {
          var data = {
            password: value
          }
          updateUserInfo(username, data).then(
            res => {
              if (res.success) {
                this.$message({
                  type: 'success',
                  message: '密码重置为:' + value
                })
              }
            }
          )
        }
      }).catch(() => {
      })
    }
  }
}
</script>
