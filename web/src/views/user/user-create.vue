<template>
  <div class="app-container" style="margin-top: 20px;margin-left:50px;width: 50%">
    <el-form ref="form" :model="formData" label-width="80px" size="mini" style="width: 50%">
      <el-form-item label="用户名：">
        <el-input v-model="formData.username" />
      </el-form-item>
      <el-form-item label="角色：">
        <el-select v-model="roleTypeVaule" placeholder="请选择" style="width: 100%">
          <el-option
            v-for="item in roleTypeOptinos"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="手机号：">
        <el-input v-model="formData.phone" />
      </el-form-item>
      <el-form-item label="邮箱：">
        <el-input v-model="formData.email" />
      </el-form-item>
      <el-form-item size="mini" style="margin-left: 30px">
        <el-button type="primary" @click="onCreateUser">创建</el-button>
        <el-button style="margin-left: 20px" @click="onReset">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
export default {
  name: 'UserCreate',
  data() {
    return {
      loading: false,
      formData: {
        username: '',
        role: '',
        phone: '',
        email: ''
      },
      roleValue: '',
      roleTypeVaule: '',
      roleTypeOptinos: [
        {
          value: 'admin',
          label: '管理员'
        },
        {
          value: 'editor',
          label: '普通用户'
        }
      ]
    }
  },
  created() {
    // 组件创建完后获取数据，
  },
  methods: {
    onCreateUser() {},
    onReset() {}
  }
}
</script>
