<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <navbar-brand :menu-active="menuActive" @burger-click="toggleBurger"></navbar-brand>
    <navbar-menu :menu-active="menuActive" @menu-click="closeMenu"></navbar-menu>
  </nav>
</template>

<script>
import NavbarBrand from './NavbarBrand'
import NavbarMenu from './NavbarMenu'

export default {
  name: 'Navbar',
  components: {
    NavbarBrand,
    NavbarMenu
  },
  data () {
    return {
      menuActive: false
    }
  },
  methods: {
    toggleBurger () {
      this.menuActive = !this.menuActive
    },
    closeMenu () {
      this.menuActive = false
    }
  }
}
</script>

<style>
#app a.navbar-item.is-active {
  color: #714dd2;
}
</style>
