<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <navbar-brand :menu-active="menuActive" @burger-click="toggleBurger"></navbar-brand>
    <navbar-menu :menu-active="menuActive"></navbar-menu>
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
      console.log(this.menuActive)
      this.menuActive = !this.menuActive
    }
  }
}
</script>
