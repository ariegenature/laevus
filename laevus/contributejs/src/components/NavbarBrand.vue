<template>
  <div class="navbar-brand">
    <a class="navbar-item" href="/">
      <img src="static/logo.png" alt="Faune sauvage et réseau routier en Ariège"
      title="Faune sauvage et réseau routier en Ariège" height="48">
      <div style="margin-left: .5rem;">
        <h1 class="title is-6">Faune et routes d'Ariège</h1>
        <h2 class="subtitle is-7">Observatoire participatif</h2>
      </div>
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
