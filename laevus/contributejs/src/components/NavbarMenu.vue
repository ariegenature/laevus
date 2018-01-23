<template>
  <div class="navbar-menu">
    <div class="navbar-start">
      <router-link :to="{ name: 'home' }" class="navbar-item">
        Les contributions&nbsp;<b-icon icon="map-marker"></b-icon>
      </router-link>
      <router-link :to="{ name: 'full-contribution' }" class="navbar-item" v-if="isAuthenticated">
        Tableau détaillé&nbsp;<b-icon icon="lock"></b-icon>
      </router-link>
    </div>
    <div class="navbar-end">
      <router-link :to="{ name: 'login' }" class="navbar-item" v-if="!isAuthenticated">
        Connexion&nbsp;<b-icon icon="sign-in"></b-icon>
      </router-link>
      <span class="navbar-item" v-if="isAuthenticated">{{ displayName }}</span>
      <a  href="/logout" class="navbar-item" v-if="isAuthenticated">
        Déconnexion&nbsp;<b-icon icon="sign-out"></b-icon>
      </a>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'NavbarMenu',
  computed: {
    displayName () {
      return this.currentUser.name
    },
    ...mapGetters([
      'currentUser',
      'isAuthenticated'
    ])
  }
}
</script>
