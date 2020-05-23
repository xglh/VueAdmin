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

export function getUserInfo(username) {
  return request({
    url: '/api/user/user' + username,
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/api/user/logout',
    method: 'post'
  })
}
