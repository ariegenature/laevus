<template>
  <v-map :zoom="zoom" :center="center" @l-click="transmitClick"
    class="locate">
    <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                 attribution="OpenStreetMap contributors"></v-tilelayer>
    <v-marker :lat-lng="[47.413220, -1.219482]"></v-marker>
  </v-map>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

export default {
  name: 'ContributeMap',
  data () {
    return {
    }
  },
  computed: mapGetters('map', [
    'center',
    'zoom'
  ]),
  methods: {
    transmitClick (ev) {
      this.$emit('l-click')
    },
    ...mapActions('map', [
      'updateCenter',
      'updateZoom'
    ])
  }
}
</script>

<style>
.leaflet-container.locate {
  cursor: crosshair;
}
</style>
