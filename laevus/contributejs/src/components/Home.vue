<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <div id="container-map" class="container is-fluid">
        <div id="columns-map" class="columns">
          <div  id="column-map"class="column is-three-fifths">
            <div id="map">
              <contribute-map @perimeter-click="handleMapClick"></contribute-map>
            </div>
            <b-collapse class="card is-small" :open.sync="isHelpShown">
              <div slot="trigger" class="card-header">
                <p class="card-header-title is-size-7">Comment utiliser la carte ?</p>
                <a class="card-header-icon"><b-icon :icon="caret"></b-icon></a>
              </div>
              <div class="card-content">
                <div class="content">
                  <p class="subtitle is-6 has-text-weight-bold">Ajouter une observation</p>
                  <p class="is-size-7">Pour saisir une nouvelle observation, il suffit de cliquer à
                  l'endroit où vous avez observé un animal.</p>
                  <p class="is-size-7">Afin de garantir un minimum de précision, le niveau de zoom
                  de la carte doit être suffisant.</p>
                  <p class="subtitle is-6 has-text-weight-bold">Voir les observations</p>
                  <p class="is-size-7">Sur la carte apparaissent les observations
                  <em>déjà saisies</em> sous forme de points.</p>
                  <p class="is-size-7">Cliquez sur un point pour voir le détail.</p>
                </div>
              </div>
            </b-collapse>
          </div>
          <div class="column">
            <div class="content">
              <p class="is-size-7"><b-taglist attached>
                <b-tag class="is-dark">niveau de zoom</b-tag>
                <b-tag :class="[tagClass]">{{ tagText }}</b-tag>
              </b-taglist>
              <p class="title is-6">Observations récentes</p>
              <contribution-table></contribution-table>
            </div>
          </div>
        </div>
      </div>
    </div>
    <b-modal :active.sync="isFormActive">
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
      isFormActive: false,
      isHelpShown: false
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
#hero-map, #container-map, #columns-map, #column-map {
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
</style>
