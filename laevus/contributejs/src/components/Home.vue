<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <div id="container-map" class="container">
        <div id="map">
          <v-map :zoom="13" :center="[47.413220, -1.219482]" @l-click="handleMapClick">
            <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                         attribution="OpenStreetMap contributors"></v-tilelayer>
            <v-marker :lat-lng="[47.413220, -1.219482]"></v-marker>
          </v-map>
        </div>
      </div>
    </div>
    <b-modal :active.sync="isFormActive">
        <contribute-form></contribute-form>
    </b-modal>
  </section>
</template>

<script>
import ContributeForm from './ContributeForm'

export default {
  name: 'Home',
  components: {
    ContributeForm
  },
  data () {
    return {
      isFormActive: false
    }
  },
  methods: {
    handleMapClick (ev) {
      this.isFormActive = true
    }
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
.modal {
  z-index: 1000;
}
.modal-content {
  background-color: rgba(245, 245, 245, 1);
}
</style>
