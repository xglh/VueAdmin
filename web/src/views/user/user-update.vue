<template>
  <div class="app-container" style="margin-top: 20px;margin-left:50px;width: 50%">
    <el-form ref="form" :model="formData" label-width="80px" size="mini" style="width: 50%">
      <el-form-item label="用户名：">
        {{ username_update }}
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
        <el-button type="primary" @click="onUpdateUser">保存</el-button>
        <el-button style="margin-left: 20px" @click="onReset">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { getUserInfo } from '@/api/user'
// import { getUserNameUpdate, setUserNameUpdate } from '@/utils/user-update'
import store from '@/store'

export default {
  name: 'UserUpdate',
  data() {
    return {
      loading: false,
      username_update: '',
      formData: {
        role: '',
        phone: '',
        email: ''
      },
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
  watch: {
    // 如果路由有变化，会再次执行该方法
    '$route': 'fetchData'
  },
  created() {
    // 组件创建完后获取数据，
    // 此时 data 已经被 observed 了
    this.fetchData()
  },
  methods: {
    fetchData() {
      let username_update = this.$route.params.username
      const username_update_store = store.getters.username_update
      username_update = username_update || username_update_store
      store.dispatch('user/saveUserNameUpdate', username_update)
      this.username_update = username_update
      this.loading = true
      // replace getPost with your data fetching util / API wrapper
      getUserInfo(username_update).then(
        res => {
          this.loading = false
          const data = res.data
          this.formData.role = data.roles[0]
          this.formData.phone = data.phone
          this.formData.email = data.email
          this.roleTypeVaule = data.roles[0]
        }
      )
    },
    onUpdateUser() {},
    onReset() {}
  }
}
</script>
