<template>
  <div class="app-container">
    <div class="filter-container">
      角色类型：
      <el-select
        v-model="roleTypeVaule"
        labal=""
        style="width: 140px"
        class="filter-item"
        placeholder="角色类型"
        @change="handleRoleTypeFilter"
      >
        <el-option v-for="item in roleTypeOptinos" :key="item.key" :label="item.label" :value="item.value" />
      </el-select>
      <el-button
        v-waves
        class="filter-item"
        type="primary"
        style="margin-left: 10px;"
        icon="el-icon-plus"
        @click="handleCreateUser"
      >
        新增用户
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="danger"
        icon="el-icon-delete"
        @click="handleDeleteUsers"
      >
        删除用户
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="userList"
      border
      fit
      highlight-current-row
      style="width: 70%;"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        width="40"
      />
      <el-table-column label="ID" type="index" align="center" />
      <el-table-column label="用户名" prop="username" align="center" />
      <el-table-column label="角色" align="center">
        <template slot-scope="{row}">
          <span>{{ row.roles[0] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="邮箱" prop="email" align="center" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="primary" @click="handleUpdateUser(row.username)">
            编辑
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
      @pagination="getList"
    />
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { getUsers, deleteUser, deleteUsers } from '@/api/user'
import { Message } from 'element-ui'

export default {
  name: 'UserList',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      userList: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 20
      },
      roleTypeVaule: '',
      roleTypeOptinos: [
        {
          value: '',
          label: '全部'
        },
        {
          value: 'admin',
          label: '管理员'
        },
        {
          value: 'editor',
          label: '普通用户'
        }
      ],
      deleteUserList: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getUsers(this.listQuery.page, this.listQuery.size).then(response => {
        this.userList = response.data.rows
        this.total = response.data.total
        this.listLoading = false
      })
    },
    handleRoleTypeFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreateUser() {
      this.$router.push({ name: 'user-create' })
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
                this.getList()
              }
            }
          )
        }).catch(() => {
        })
      }
    },
    handleUpdateUser(username) {
      this.$router.push({ name: 'user-update', params: { username: username }})
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
              this.getList()
            }
          }
        )
      }).catch(() => {
      })
    },
    handleSelectionChange(val) {
      this.deleteUserList = val
    }
  }
}
</script>
