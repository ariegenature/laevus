<template>
  <v-map :zoom="13" :center="[47.413220, -1.219482]" @l-click="transmitClick"
    class="locate">
    <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                 attribution="OpenStreetMap contributors"></v-tilelayer>
    <v-marker :lat-lng="[47.413220, -1.219482]"></v-marker>
  </v-map>
</template>

<script>
export default {
  name: 'ContributeMap',
  data () {
    return {
    }
  },
  methods: {
    transmitClick (ev) {
      this.$emit('l-click')
    }
  }
}
</script>

<style>
.leaflet-container.locate {
  cursor: crosshair;
}
</style>
