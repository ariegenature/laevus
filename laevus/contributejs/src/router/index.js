import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import FullContribution from '@/components/FullContribution'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/contribute',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/full-contribution',
      name: 'full-contribution',
      component: FullContribution
    },
    {
      path: '/',
      redirect: '/contribute'
    }
  ]
})
