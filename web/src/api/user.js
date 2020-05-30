import request from '@/utils/request'

// 用户登陆
export function login(data) {
  return request({
    url: '/api/user/login',
    method: 'post',
    data
  })
}
// 用户登出
export function logout() {
  return request({
    url: '/api/user/logout',
    method: 'put'
  })
}

// 获取角色列表
export function getRoles(page, size) {
  return request({
    url: '/api/user/roles',
    method: 'get',
    params: {
      page: page || 1,
      size: size || 100
    }
  })
}

// 批量删除角色
export function deleteRoles(userNameList) {
  return request({
    url: '/api/user/roles',
    method: 'delete',
    data: userNameList

  })
}

// 获取角色信息
export function getRoleInfo(role) {
  return request({
    url: '/api/user/role/' + role,
    method: 'get'
  })
}

// 新增角色
export function createRole(data) {
  return request({
    url: '/api/user/role',
    method: 'post',
    data
  })
}

// 修改角色信息
export function updateRoleInfo(role, data) {
  return request({
    url: '/api/user/role/' + role,
    method: 'put',
    data
  })
}

// 删除角色
export function deleteRole(role) {
  return request({
    url: '/api/user/role/' + role,
    method: 'delete'
  })
}

// 获取用户列表
export function getUsers(roleId, page, size) {
  return request({
    url: '/api/user/users',
    method: 'get',
    params: {
      roleId: roleId,
      page: page,
      size: size || 20
    }
  })
}

// 批量删除用户
export function deleteUsers(userNameList) {
  return request({
    url: '/api/user/users',
    method: 'delete',
    data: userNameList

  })
}

// 获取用户信息
export function getUserInfo(username) {
  return request({
    url: '/api/user/user/' + username,
    method: 'get'
  })
}

// 新增用户
export function createUser(data) {
  return request({
    url: '/api/user/user',
    method: 'post',
    data
  })
}

// 修改用户信息
export function updateUserInfo(userName, data) {
  return request({
    url: '/api/user/user/' + userName,
    method: 'put',
    data
  })
}

// 删除用户
export function deleteUser(userName) {
  return request({
    url: '/api/user/user/' + userName,
    method: 'delete'
  })
}
