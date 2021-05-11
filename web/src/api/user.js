import request from '@/utils/request'

// 用户登陆
export function login(data) {
  return request({
    url: '/api/user/login/',
    method: 'post',
    data
  })
}

// 用户登出
export function logout() {
  return request({
    url: '/api/user/logout/',
    method: 'put'
  })
}

// 获取角色列表
export function getRoles(page, size, search, ordering) {
  return request({
    url: '/api/user/roles/',
    method: 'get',
    params: {
      page: page || 1,
      size: size || 20,
      search: search || '',
      ordering: ordering || ''
    }
  })
}

// 获取所有
export function getRolesAll() {
  return request({
    url: '/api/user/roles/all/',
    method: 'get'
  })
}

// 批量删除角色
export function deleteRoles(roleIds) {
  return request({
    url: '/api/user/roles/del/',
    method: 'delete',
    data: roleIds
  })
}

// 获取角色信息
export function getRole(roleId) {
  return request({
    url: '/api/user/roles/' + roleId + '/',
    method: 'get'
  })
}

// 新增角色
export function createRole(data) {
  return request({
    url: '/api/user/roles/',
    method: 'post',
    data
  })
}

// 修改角色信息
export function updateRole(roleId, data) {
  return request({
    url: '/api/user/roles/' + roleId + '/',
    method: 'put',
    data
  })
}

// 删除角色
export function deleteRole(roleId) {
  return request({
    url: '/api/user/roles/' + roleId + '/',
    method: 'delete'
  })
}

// 获取用户列表
export function getUsers(roleId, page, size, search, ordering) {
  return request({
    url: '/api/user/users/',
    method: 'get',
    params: {
      roleId: roleId,
      page: page || 1,
      size: size || 20,
      search: search || '',
      ordering: ordering || ''
    }
  })
}

// 获取用户信息
export function getUser(userId) {
  return request({
    url: '/api/user/users/' + userId + '/',
    method: 'get'
  })
}

// 新增用户
export function createUser(data) {
  return request({
    url: '/api/user/users/',
    method: 'post',
    data
  })
}

// 修改用户信息
export function updateUser(userId, data) {
  return request({
    url: '/api/user/users/' + userId + '/',
    method: 'put',
    data
  })
}

// 删除用户
export function deleteUser(userId) {
  return request({
    url: '/api/user/users/' + userId + '/',
    method: 'delete'
  })
}

// 批量删除用户
export function deleteUsers(userIds) {
  return request({
    url: '/api/user/users/del/',
    method: 'delete',
    data: userIds
  })
}
