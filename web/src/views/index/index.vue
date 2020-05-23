<template>
  <div>
    <h1>这是首页,当前用户:{{ username }} </h1>
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
