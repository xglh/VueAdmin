import request from '@/utils/request'

// 用户登陆
export function login(data) {
  return request({
    url: '/api/user/login',
    method: 'post',
    data
  })
}

// 获取用户列表
export function getUsers(page, size) {
  return request({
    url: '/api/user/users',
    method: 'get',
    params: {
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
export function updateUserInfo(data) {
  return request({
    url: '/api/user/user',
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

// 用户登出
export function logout() {
  return request({
    url: '/api/user/logout',
    method: 'put'
  })
}

