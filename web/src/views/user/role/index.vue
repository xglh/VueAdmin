<template>
  <div class="app-container">
    <RoleIndexHeader :list-query="listQuery" :delete-role-list="deleteRoleList" />

    <el-table
      v-loading="listLoading"
      :data="roleList"
      border
      highlight-current-row
      style="width: 100%;margin-top: 15px;"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        type="selection"
        width="40"
      />
      <el-table-column label="ID" type="index" align="center" width="40" />
      <el-table-column label="角色" prop="role" align="center" />
      <el-table-column label="名称" prop="roleName" align="center" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="primary" @click="handleUpdateRole(row)">
            编辑
          </el-button>
          <el-button size="mini" type="danger" @click="handleDeleteRole(row.id)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <RoleUpdateForm :update-dialog-form-visible.sync="updateDialogFormVisible" :update-role-info="updateRoleInfo" />
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.size"
      @pagination="fetchData"
    />
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { getRoles, deleteRole } from '@/api/user'
import { Message } from 'element-ui'
import RoleIndexHeader from './module/index-header'
import RoleUpdateForm from './module/role-update-form'
export default {
  name: 'RoleList',
  components: { Pagination, RoleIndexHeader, RoleUpdateForm },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      roleList: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        size: 10,
        search: '',
        ordering: ''
      },
      deleteRoleList: [],
      updateDialogFormVisible: false,
      updateRoleInfo: this.getInitUpdateRoleInfo()
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      setTimeout(() => {
        this.listLoading = false
      }, 3 * 1000)
      getRoles(this.listQuery.page, this.listQuery.size, this.listQuery.search, this.listQuery.ordering).then(response => {
        this.roleList = response.data.rows
        this.total = response.data.total
        this.listLoading = false
      })
    },
    handleUpdateRole(row) {
      this.updateRoleInfo = {
        roleId: row.id,
        role: row.role,
        roleName: row.roleName
      }

      this.updateDialogFormVisible = true
    },
    handleDeleteRole(roleId) {
      this.$confirm('确认删除角色?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteRole(roleId).then(
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
      this.deleteRoleList = val
    },
    getInitUpdateRoleInfo() {
      return {
        roleId: 0,
        role: '',
        roleName: ''
      }
    }
  }
}
</script>
