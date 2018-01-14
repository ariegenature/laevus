<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <div id="container-map" class="container">
        <div id="columns-map" class="columns">
          <div  id="column-map"class="column is-four-fifths">
            <div id="map">
              <contribute-map @perimeter-click="handleMapClick"></contribute-map>
            </div>
          </div>
          <div class="column">
            <div class="content">
              <h3 class="is-size-5">Comment utiliser la carte ?</h3>
              <h2 class="is-size-6">Ajouter une observation</h2>
              <p class="is-size-7"><b-taglist attached>
                <b-tag class="is-dark">niveau de zoom</b-tag>
                <b-tag :class="[tagClass]">{{ tagText }}</b-tag>
              </b-taglist>
              <p class="is-size-7">Pour saisir une nouvelle observation, il suffit de cliquer à
              l'endroit où vous avez observé un animal.</p>
              <p class="is-size-7">Afin de garantir un minimum de précision, le niveau de zoom de
              la carte doit être suffisant.</p>
              </p>
              <h2 class="is-size-6">Voir les observations</h2>
              <p class="is-size-7">Sur la carte apparaissent les observations
              <em>déjà saisies</em> sour forme de points.</p>
              <p class="is-size-7">Cliquez sur un point pour voir le détail.</p>
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

export default {
  name: 'Home',
  components: {
    ContributeForm,
    ContributeMap
  },
  data () {
    return {
      isFormActive: false
    }
  },
  computed: {
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
    ...mapActions(['setGroups'])
  },
  async created () {
    try {
      const response = await axios.get('api/child-group')
      this.setGroups(response.data)
    } catch (e) {
      console.log(e)
    }
  }
}
</script>

<style>
#hero-map, #container-map, #columns-map, #column-map {
  height: 100%;
}
#map {
  height: 90%;
}
.modal {
  z-index: 1000 !important;
}
.modal-content {
  background-color: rgba(245, 245, 245, 1);
}
.leaflet-container.locate {
  cursor: crosshair;
}
</style>
