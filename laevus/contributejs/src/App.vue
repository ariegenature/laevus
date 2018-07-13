<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
    <site-footer></site-footer>
    <b-loading :active="isLoading" :canCancel="false"></b-loading>
    <b-modal :active="isHelpShown" :onCancel="closeHelp" has-modal-card>
      <help></help>
    </b-modal>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import SiteFooter from './components/SiteFooter'

import Help from './components/Help'
import Navbar from './components/Navbar'

export default {
  name: 'app',
  components: {
    Help,
    Navbar,
    SiteFooter
  },
  computed: mapGetters([
    'isHelpShown',
    'isLoading'
  ]),
  methods: {
    closeHelp () {
      if (this.isHelpShown) {
        this.toggleHelp()
      }
    },
    ...mapActions([
      'syncCurrentUser',
      'toggleHelp'
    ])
  },
  created () {
    this.syncCurrentUser()
  }
}
</script>
