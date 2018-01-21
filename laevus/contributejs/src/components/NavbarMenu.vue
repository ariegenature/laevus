<template>
  <div class="navbar-menu">
    <div class="navbar-start">
    </div>
    <div class="navbar-end">
      <router-link :to="{ name: 'login' }" class="navbar-item">Connexion</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavbarMenu'
}
</script>
