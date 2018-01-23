<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
    <b-loading :active.sync="isLoading" :canCancel="false"></b-loading>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import Navbar from './components/Navbar'

export default {
  name: 'app',
  components: {
    Navbar
  },
  computed: mapGetters([
    'isLoading'
  ]),
  methods: mapActions([
    'syncCurrentUser'
  ]),
  created () {
    this.syncCurrentUser()
  }
}
</script>
