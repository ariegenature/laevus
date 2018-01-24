<template>
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <img src="static/logo.png" alt="laevus" width="144" height="48">
    </a>
    <div class="button navbar-burger" :class="{ 'is-active': menuActive }"
         @click="emitBurgerClick">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavbarBrand',
  props: ['menuActive'],
  methods: {
    emitBurgerClick (ev) {
      this.$emit('burger-click')
    }
  }
}
</script>
