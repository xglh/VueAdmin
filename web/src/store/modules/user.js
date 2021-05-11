import { login, logout, getUser } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { getUserId, setUserId, removeUserId } from '@/utils/auth'
import { getUserName, setUserName, removeUserName } from '@/utils/auth'
import { getUserNameUpdate, setUserNameUpdate } from '@/utils/user-update'
import router, { resetRouter } from '@/router'

const state = {
  token: getToken(),
  userId: 0,
  username: '',
  avatar: '',
  roles: [],
  username_update: getUserNameUpdate()
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_USERID: (state, userId) => {
    state.userId = userId
  },
  SET_USERNAME: (state, username) => {
    state.username = username
  },
  SET_USERNAME_UPDATE: (state, username_update) => {
    state.username_update = username_update
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        const { userId, username, token } = data
        commit('SET_TOKEN', token)
        commit('SET_USERID', userId)
        commit('SET_USERNAME', username)
        setToken(token)
        setUserId(userId)
        setUserName(username)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getUser(getUserId()).then(response => {
        const { data } = response

        if (!data) {
          reject('Verification failed, please Login again.')
        }

        const { username, roles, avatar } = data
        // roles must be a non-empty array
        if (!roles || roles.length <= 0) {
          reject('getInfo: roles must be a non-null array!')
        }
        commit('SET_ROLES', roles)
        commit('SET_AVATAR', avatar)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      logout().then(() => {
        commit('SET_TOKEN', '')
        commit('SET_USERID', 0)
        commit('SET_USERNAME', '')
        commit('SET_ROLES', [])
        removeToken()
        removeUserId()
        removeUserName()
        resetRouter()
        // reset visited views and cached views
        // to fixed https://github.com/PanJiaChen/vue-element-admin/issues/2485
        dispatch('tagsView/delAllViews', null, { root: true })

        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      commit('SET_USERID', 0)
      commit('SET_USERNAME', '')
      removeToken()
      removeUserId()
      removeUserName()
      resolve()
    })
  },

  // dynamically modify permissions
  changeRoles({ commit, dispatch }, role) {
    return new Promise(async resolve => {
      const token = role + '-token'

      commit('SET_TOKEN', token)
      setToken(token)
      const { roles } = await dispatch('getInfo')
      resetRouter()

      // generate accessible routes map based on roles
      const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })

      // dynamically add accessible routes
      router.addRoutes(accessRoutes)

      // reset visited views and cached views
      dispatch('tagsView/delAllViews', null, { root: true })

      resolve()
    })
  },

  saveUserNameUpdate({ commit }, usernameUpdate) {
    return new Promise(resolve => {
      commit('SET_USERNAME_UPDATE', usernameUpdate)
      setUserNameUpdate(usernameUpdate)
      resolve()
    })
  }

}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
