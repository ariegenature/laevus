<template>
  <v-map :zoom="zoom" :center="center" @l-click="transmitClick"
    class="locate">
    <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                 attribution="OpenStreetMap contributors"></v-tilelayer>
    <v-geojson-layer :geojson="perimeter" :options="options"></v-geojson-layer>
  </v-map>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

export default {
  name: 'ContributeMap',
  data () {
    return {
      perimeter: null,
      options: {
        style: function () {
          return {
            weight: 2,
            color: '#ECEFF1',
            opacity: 1,
            fillColor: '#e4ce7f',
            fillOpacity: 1
          }
        }
      }
    }
  },
  computed: {
    ...mapGetters('map', [
      'center',
      'zoom'
    ]),
    ...mapGetters([
      'perimeterUrl'
    ])
  },
  methods: {
    transmitClick (ev) {
      this.$emit('l-click')
    },
    ...mapActions('map', [
      'updateCenter',
      'updateZoom'
    ])
  },
  async created () {
    try {
      const response = await fetch(this.perimeterUrl)
      if (response.ok) {
        this.perimeter = await response.json()
      } else {
        throw new Error('Cannot fetch data perimeter')
      }
    } catch (e) {
      this.error = e
    }
  }
}
</script>

<style>
.leaflet-container.locate {
  cursor: crosshair;
}
</style>
