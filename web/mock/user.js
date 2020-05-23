export default [
  // user login
  {
    url: '/api/user/login',
    type: 'post',
    response: config => {
      return {
        code: 200,
        success: true,
        message: 'success',
        data: {
          token: 'c5c50929ba89b241e69b86c65cbf9e1e366abdbc'
        }
      }
    }
  },

  // get user info
  {
    url: '/api/user/users',
    type: 'get',
    response: config => {
      return {
        code: 200,
        success: true,
        message: 'success',
        data: {
          total: 1,
          rows: [
            {
              roles: ['admin'],
              avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
              username: 'admin',
              email: '131863361@qq.com',
              phone: '13242034299',
              nickName: '刘辉'
            }
          ]
        }
      }
    }
  },
  // get user info
  {
    url: '/api/user/user\.*',
    type: 'get',
    response: config => {
      return {
        code: 200,
        success: true,
        message: 'success',
        data: {
          roles: ['admin'],
          avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
          username: 'admin',
          email: '131863361@qq.com',
          phone: '13242034299',
          nickName: '刘辉'
        }
      }
    }
  },
  // user logout
  {
    url: '/api/user/logout',
    type: 'post',
    response: _ => {
      return {
        code: 200,
        data: 'success'
      }
    }
  }
]
