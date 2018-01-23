<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

import Navbar from './components/Navbar'

export default {
  name: 'app',
  components: {
    Navbar
  },
  methods: mapActions([
    'syncCurrentUser'
  ]),
  created () {
    this.syncCurrentUser()
  }
}
</script>
