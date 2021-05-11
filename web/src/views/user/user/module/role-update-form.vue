<template>
  <el-dialog title="编辑角色" :visible="updateDialogFormVisible" :before-close="dialogFormClose">
    <el-form
      ref="form"
      :model="form"
      :rules="rules"
      :status-icon="status_icon"
      label-width="80px"
      style="margin-top: 20px;margin-left:30px;width: 60%"
    >
      <el-form-item label="角色：">
        {{ updateRoleInfo.role }}
      </el-form-item>
      <el-form-item label="名称：" prop="roleName">
        <el-input v-model="form.roleName" />
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button style="margin-left: 60px" @click="dialogFormClose">取消</el-button>
      <el-button type="primary" @click="onUpdateRole">确定</el-button>

    </div>
  </el-dialog>
</template>
<script>
import { updateRole } from '@/api/user'
import { Message } from 'element-ui'

export default {
  name: 'RoleUpdateForm',
  props: {
    updateDialogFormVisible: {
      type: Boolean,
      required: false
    },
    updateRoleInfo: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      form: this.getInitFormData(),
      status_icon: true,
      rules: {
        roleName: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 3, max: 24, message: '长度在 3 到 24 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    updateDialogFormVisible(val) {
      this.form = this.getInitFormData()
      if (val === true) {
        this.fetchData()
      }
    }
  },
  created() {
  },
  methods: {
    getInitFormData() {
      return {
        roleName: this.updateRoleInfo.roleName
      }
    },
    fetchData() {
      // replace getPost with your data fetching util / API wrapper
    },
    onUpdateRole() {
      updateRole(this.updateRoleInfo.roleId, this.form).then(
        res => {
          if (res.success) {
            Message({
              type: 'success',
              message: '修改成功!',
              duration: 1500
            })
            this.dialogFormClose()
            this.$parent.fetchData()
          }
        }
      )
    },

    dialogFormClose() {
      this.$emit('update:updateDialogFormVisible', false)
    }
  }
}
</script>
