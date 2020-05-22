<template>
  <el-dialog :key="textMap[dialogStatus]" :title="textMap[dialogStatus]" :visible="dialogFormVisible" :before-close="disableDialog" center>
    <el-form
      ref="dataForm"
      :rules="rules"
      :model="temp"
      label-position="left"
      label-width="90px"
      style="width: 400px; margin:10px 250px;"
    >
      <el-form-item label="角色名称:" prop="roleName">
        <el-input v-model="temp.roleName" />
      </el-form-item>
      <el-form-item label="备  注:">
        <el-input v-model="temp.remark" />
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="dialogStatus==='create'?createRole():updateRoleData()">
        确定
      </el-button>
      <el-button @click="disableDialog">
        取消
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
import { addUserRole, updateUserRole } from '@/api/user'
export default {
  name: 'UserRoleinfoEditDialog',
  // 父组件传值参数
  props: {
    temp: Object,
    dialogStatus: String,
    dialogFormVisible: Boolean
  },
  data() {
    return {
      role: this.temp,
      textMap: {
        update: '编辑角色',
        create: '新增角色'
      },
      rules: {
        roleName: [{ required: true, message: '角色名称不能为空', trigger: 'blur' }]
      }
    }
  },
  methods: {
    // 新增用户
    createRole() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          addUserRole(this.role).then(() => {
            this.roleList.unshift(this.role)
            this.disableDialog()
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    // 更新role数据
    updateRoleData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.role)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateUserRole(tempData).then(() => {
            for (const v of this.roleList) {
              if (v.id === this.role.id) {
                const index = this.roleList.indexOf(v)
                this.roleList.splice(index, 1, this.role)
                break
              }
            }
            this.disableDialog()
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    // 双向数据绑定
    disableDialog() {
      this.$emit('update:dialogFormVisible', false)
    }
  }
}

</script>

<style scoped>

</style>
