<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <div id="container-map" class="container is-fluid is-marginless">
        <div class="columns">
          <div class="column is-three-fifths is-paddingless">
            <div id="map">
              <contribute-map @perimeter-click="handleMapClick"></contribute-map>
            </div>
          </div>
          <div class="column is-paddingless">
            <div class="content">
              <p class="is-size-7"><b-taglist attached>
                <b-tag class="is-dark">niveau de zoom</b-tag>
                <b-tag :class="[tagClass]">{{ tagText }}</b-tag>
              </b-taglist>
            </div>
            <contribution-table></contribution-table>
          </div>
        </div>
      </div>
    </div>
    <b-modal id="modal-form" :active.sync="isFormActive">
        <contribute-form></contribute-form>
    </b-modal>
  </section>
</template>

<script>
import axios from 'axios'
import { mapActions, mapGetters } from 'vuex'

import ContributeForm from './ContributeForm'
import ContributeMap from './ContributeMap'
import ContributionTable from './ContributionTable'

export default {
  name: 'Home',
  components: {
    ContributeForm,
    ContributeMap,
    ContributionTable
  },
  data () {
    return {
      isFormActive: false
    }
  },
  computed: {
    caret () {
      return this.isHelpShown ? 'caret-up' : 'caret-down'
    },
    tagClass () {
      return this.zoom >= 14 ? 'is-success' : 'is-danger'
    },
    tagText () {
      return this.zoom >= 14 ? 'suffisant' : `insuffisant (${this.zoom - 14})`
    },
    ...mapGetters('map', ['zoom'])
  },
  methods: {
    handleMapClick (ev) {
      this.isFormActive = true
    },
    ...mapActions([
      'setContributions',
      'setGroups',
      'setPageLoading',
      'setPageReady'
    ])
  },
  async created () {
    this.setPageLoading()
    try {
      const response = await axios.get('api/contribution')
      this.setContributions(response.data)
    } catch (e) {
      console.log(e)
    }
    try {
      const response = await axios.get('api/child-group')
      this.setGroups(response.data)
    } catch (e) {
      console.log(e)
    }
    this.setPageReady()
  }
}
</script>

<style>
#hero-map, #container-map {
  height: 100%;
}
#map {
  height: 80vh;
}
.modal {
  z-index: 1000 !important;
}
.loading-overlay {
  z-index: 2000 !important;
}
.modal-content {
  background-color: rgba(245, 245, 245, 1);
}
.leaflet-container.locate {
  cursor: crosshair;
}
#modal-form .modal-content {
  max-height: calc(100vh - 40px);
}
</style>
