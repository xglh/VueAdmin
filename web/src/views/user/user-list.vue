<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"
        icon="el-icon-edit"
        size="mini"
        @click="handleRoleCreate"
      >
        新增账号
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="danger"
        icon="el-icon-delete"
        size="mini"
        @click="handleBatchRoleDel"
      >
        批量删除
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="userInfoList"
      border
      fit
      highlight-current-row
      style="width: 60%;"
      :default-sort="{prop: 'roleName', order: 'descending'}"
      @selection-change="handleBatchRoleDelSelectionChange"
    >
      <el-table-column
        v-model="delRoleList"
        type="selection"
        width="55"
      />
      <el-table-column
        prop="id"
        label="ID"
        type="index"
        width="55"
      />

      <el-table-column prop="username" label="用户名" width="200px" min-width="100px" align="left" sortable />
      <el-table-column prop="role" label="角色" width="200px" min-width="100px" align="left" sortable />
      <el-table-column prop="phone" label="手机" min-width="100px" />
      <el-table-column prop="email" label="邮箱" min-width="100px" />
      <el-table-column label="操作" align="center" width="300px" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" style="width: 70px;text-align: center" @click="handleRoleUpdate(row)">
            编辑
          </el-button>
          <el-button type="danger" size="mini" @click="handleRoleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.size"
      @pagination="getRoleList"
    />
    <UserRoleinfoEditDialog
      :temp="temp"
      :dialog-form-visible.sync="dialogRoleFormVisible"
      :dialog-status="dialogRoleStatus"
    />

  </div>
</template>

<script>
import { getUsers } from '@/api/user'
import UserRoleinfoEditDialog from './components/user-info-dialog'

export default {
  name: 'UserAccount',
  components: { UserRoleinfoEditDialog },
  data() {
    return {
      userInfoList: this.getUserInfoList()
    }
  },
  methods: {
    getUserInfoList() {
      getUsers().then(response => {
        const res = response.data
        const userInfoList = res.data
        return userInfoList
      })
    }
  }
}
</script>

<style scoped>

</style>
