<template>
  <div class="navbar-menu" :class="{ 'is-active': menuActive }">
    <div class="navbar-start">
      <router-link :to="{ name: 'home' }" class="navbar-item" active-class="is-active"
                   @click.native="emitMenuClick">
        <b-icon icon="map-marker"></b-icon>&nbsp;Les contributions
      </router-link>
      <router-link :to="{ name: 'presentation' }" class="navbar-item" active-class="is-active"
                   @click.native="emitMenuClick">
        <b-icon icon="info-circle"></b-icon>&nbsp;Présentation
      </router-link>
      <router-link :to="{ name: 'full-contribution' }" class="navbar-item" active-class="is-active"
                   v-if="isAuthenticated" @click.native="emitMenuClick">
        <b-icon icon="table"></b-icon>&nbsp;Tableau détaillé
      </router-link>
    </div>
    <div class="navbar-end">
      <a id="help" class="navbar-item" @click="clickHelp">
        <b-icon icon="question-circle"></b-icon>&nbsp;Aide
      </a>
      <router-link :to="{ name: 'login' }" class="navbar-item" v-if="!isAuthenticated"
                   @click.native="emitMenuClick">
        <b-icon icon="sign-in"></b-icon>&nbsp;Connexion
      </router-link>
      <a href="/logout" class="navbar-item" title="Déconnexion" v-if="isAuthenticated"
         @click.native="emitMenuClick">
        <b-icon icon="sign-out"></b-icon>&nbsp;{{ displayName }}
      </a>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
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
    },
    clickHelp (ev) {
      this.$emit('menu-click')
      this.toggleHelp()
    },
    ...mapActions([
      'toggleHelp'
    ])
  }
}
</script>
