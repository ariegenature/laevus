<template>
  <div class="navbar-menu" :class="{ 'is-active': menuActive }">
    <div class="navbar-start">
      <router-link :to="{ name: 'home' }" class="navbar-item" active-class="is-active"
                   v-if="isAuthenticated" @click.native="emitMenuClick">
        <b-icon icon="map-marker"></b-icon>&nbsp;Les contributions
      </router-link>
      <router-link :to="{ name: 'full-contribution' }" class="navbar-item" active-class="is-active"
                   v-if="isAuthenticated" @click.native="emitMenuClick">
        <b-icon icon="table"></b-icon>&nbsp;Tableau détaillé
      </router-link>
    </div>
    <div class="navbar-end">
      <router-link :to="{ name: 'login' }" class="navbar-item" v-if="!isAuthenticated"
                   @click.native="emitMenuClick">
        <b-icon icon="sign-in"></b-icon>&nbsp;Connexion
      </router-link>
      <span class="navbar-item" v-if="isAuthenticated">{{ displayName }}</span>
      <a  href="/logout" class="navbar-item" v-if="isAuthenticated" @click.native="emitMenuClick">
        <b-icon icon="sign-out"></b-icon>&nbsp;Déconnexion
      </a>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'NavbarMenu',
  props: ['menuActive'],
  computed: {
    displayName () {
      return this.currentUser.name
    },
    ...mapGetters([
      'currentUser',
      'isAuthenticated'
    ])
  },
  methods: {
    emitMenuClick (ev) {
      this.$emit('menu-click')
    }
  }
}
</script>
