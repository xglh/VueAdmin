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
export function getUsers() {
  return request({
    url: '/api/user/users',
    method: 'get'
  })
}

export function getInfo(token) {
  return request({
    url: '/vue-element-admin/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-element-admin/user/logout',
    method: 'post'
  })
}

export function getUser(userName) {
  return request({
    url: '/user/' + userName,
    method: 'get'
  })
}
