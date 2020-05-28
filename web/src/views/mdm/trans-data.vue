<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button
        v-waves
        class="filter-item"
        type="primary"
        style="margin-left: 10px;"
        icon="el-icon-plus"
        @click="handleCreateRole"
      >
        新增角色
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="danger"
        icon="el-icon-delete"
        @click="handleDeleteRoles"
      >
        删除角色
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="roleList"
      border
      fit
      highlight-current-row
      style="width: 40%;"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        width="40"
      />
      <el-table-column label="ID" type="index" align="center" />
      <el-table-column label="角色" prop="role" align="center" />
      <el-table-column label="名称" prop="roleName" align="center">
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="primary" @click="handleUpdateRole(row.role)">
            编辑
          </el-button>
          <el-button size="mini" type="danger" @click="handleDeleteRole(row.role)">
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
import { getRoles, deleteRole, deleteRoles } from '@/api/user'
import { Message } from 'element-ui'

export default {
  name: 'MdmTransData',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      roleList: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 20
      },
      deleteRoleList: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getRoles(this.listQuery.page, this.listQuery.size).then(response => {
        this.roleList = response.data.rows
        this.total = response.data.total
        this.listLoading = false
      })
    },
    handleRoleTypeFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreateRole() {
      this.$router.push({ name: 'role-create' })
    },
    handleDeleteRoles() {
      var targetDeleteRoleList = []
      this.deleteRoleList.forEach(data => {
        targetDeleteRoleList.push(data.role)
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
                this.getList()
              }
            }
          )
        }).catch(() => {
        })
      }
    },
    handleUpdateRole(role) {
      this.$router.push({ name: 'role-update', params: { role: role }})
    },
    handleDeleteRole(role) {
      this.$confirm('确认删除角色?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteRole(role).then(
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
      this.deleteRoleList = val
    }
  }
}
</script>
