import Cookies from 'js-cookie'

const UserNameUpdateKey = 'UserNameUpdate'

export function getUserNameUpdate() {
  return Cookies.get(UserNameUpdateKey)
}

export function setUserNameUpdate(UserNameUpdate) {
  return Cookies.set(UserNameUpdateKey, UserNameUpdate)
}

export function removeUserNameUpdate() {
  return Cookies.remove(UserNameUpdateKey)
}
