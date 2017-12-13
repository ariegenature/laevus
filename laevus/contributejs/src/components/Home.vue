<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <div id="container-map" class="container">
        <div id="map">
          <v-map :zoom="13" :center="[47.413220, -1.219482]">
            <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                         attribution="OpenStreetMap contributors"></v-tilelayer>
            <v-marker :lat-lng="[47.413220, -1.219482]"></v-marker>
          </v-map>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Home',
  data () {
  }
}
</script>

<style>
#hero-map, #container-map {
  height: 100%;
}
#map {
  height: 90%;
}
</style>
