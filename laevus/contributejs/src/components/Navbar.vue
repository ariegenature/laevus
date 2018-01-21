<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <navbar-brand></navbar-brand>
    <navbar-menu></navbar-menu>
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
  }
}
</script>
