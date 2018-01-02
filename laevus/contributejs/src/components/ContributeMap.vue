<template>
  <v-map ref="map" :zoom="zoom" :center="center" @l-click="transmitClick"
         @l-layeradd="zoomOnPerimeter" class="locate">
    <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                 attribution="OpenStreetMap contributors"></v-tilelayer>
    <v-geojson-layer ref="perimeter" :geojson="perimeter" :options="options"></v-geojson-layer>
  </v-map>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

export default {
  name: 'ContributeMap',
  data () {
    return {
      isReady: false,
      perimeter: null,
      options: {
        style: function () {
          return {
            weight: 2,
            color: '#ECEFF1',
            opacity: 1,
            fillColor: '#e4ce7f',
            fillOpacity: 1,
            className: 'perimeter'
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
    zoomOnPerimeter (ev) {
      if (this.isReady) return
      const perimeterBounds = this.$refs.perimeter.getBounds()
      if (perimeterBounds.hasOwnProperty('_southWest')) {
        this.$refs.map.fitBounds(perimeterBounds)
        this.isReady = true
      }
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
  cursor: not-allowed;
}
.perimeter {
  cursor: crosshair;
}
</style>
