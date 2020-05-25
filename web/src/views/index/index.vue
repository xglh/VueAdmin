<template>
  <div class="app-container" style="margin-top: 20px;margin-left:50px;width: 50%">
    <div class="page-header">
  <h1>这是首页,当前用户:{{ username }}</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
      username: this.getUserName()
    }
  },
  methods: {
    getUserName() {
      return this.$store.getters.username
    }

  }
}
</script>

<style scoped>

</style>
