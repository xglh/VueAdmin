import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },

  {
    path: '/profile',
    component: Layout,
    // redirect: '/profile/index',
    hidden: true,
    meta: { title: '个人信息' },
    children: [
      {
        path: 'user-info',
        component: () => import('@/views/profile/user-info'),
        name: 'user-info',
        meta: { title: '个人信息' }
      },
      {
        path: 'update-password',
        component: () => import('@/views/profile/update-password'),
        name: 'update-password',
        meta: { title: '修改密码' }
      }
    ]
  },
  {
    path: '/',
    component: Layout,
    redirect: '/index',
    rank: 10,
    children: [
      {
        path: 'index',
        component: () => import('@/views/index/index'),
        name: 'index',
        meta: { title: '首页', icon: 'dashboard', affix: true }
      }
    ]
  },
  {
    path: '/mdm',
    component: Layout,
    meta: { title: '基础数据测试中心', icon: 'chart' },
    rank: 30,
    children: [
      {
        path: 'mdm-dashbord',
        component: () => import('@/views/mdm/dashboard'),
        name: 'mdm-dashbord',
        meta: { title: 'dashbord' }
      },
      {
        path: 'mdm-test-data',
        component: () => import('@/views/mdm/test-data'),
        name: 'mdm-test-data',
        meta: { title: '测试数据' }
      },
      {
        path: 'mdm-trans-data',
        component: () => import('@/views/mdm/trans-data'),
        name: 'mdm-trans-data',
        meta: { title: '译码数据' }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [

  {
    path: '/user',
    component: Layout,
    redirect: '/user/index',
    meta: { title: '用户管理', icon: 'peoples', roles: ['admin'] },
    rank: 20,
    children: [
      {
        path: 'role',
        component: () => import('@/views/user/role/index'),
        name: 'role',
        meta: { title: '角色管理', roles: ['admin'] }
      },
      {
        path: 'user',
        component: () => import('@/views/user/user/index'),
        name: 'user',
        meta: { title: '账号管理', roles: ['admin'] }
      },
      {
        path: 'role-create',
        component: () => import('@/views/user/role/role-create'),
        name: 'role-create',
        hidden: true,
        props: true,
        meta: { title: '新增角色', roles: ['admin'] }
      },
      {
        path: 'role-update/:role',
        component: () => import('@/views/user/role/role-update'),
        name: 'role-update',
        hidden: true,
        props: true,
        meta: { title: '编辑角色', roles: ['admin'] }
      },
      {
        path: 'user-create',
        component: () => import('@/views/user/user/user-create'),
        name: 'user-create',
        hidden: true,
        props: true,
        meta: { title: '新增用户', roles: ['admin'] }
      },
      {
        path: 'user-update/:username',
        component: () => import('@/views/user/user/user-update'),
        name: 'user-update',
        hidden: true,
        props: true,
        meta: { title: '编辑用户', roles: ['admin'] }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
