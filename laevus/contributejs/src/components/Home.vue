<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <div id="container-map" class="container">
        <div id="map">
          <contribute-map @perimeter-click="handleMapClick"></contribute-map>
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
  z-index: 1000 !important;
}
.modal-content {
  background-color: rgba(245, 245, 245, 1);
}
.leaflet-container.locate {
  cursor: crosshair;
}
</style>
