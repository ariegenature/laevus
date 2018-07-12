<template>
  <l-map ref="map" :zoom="zoom" :center="center" @contextmenu="transmitClick"
         @zoom="updateZoomFromMap" @layeradd="zoomOnPerimeter" class="locate">
    <leaflet-locate-control :show-popup="false"></leaflet-locate-control>
    <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                 attribution="OpenStreetMap contributors"></l-tile-layer>
    <l-geojson ref="perimeter" :geojson="perimeter"
               :options="perimeterOptions"></l-geojson>
    <l-geojson ref="contribution" :geojson="contributions"
               :options="contributionOptions"></l-geojson>
    <l-marker :lat-lng="latLng" v-if="hasLatLng" @click="reEmitClick"></l-marker>
  </l-map>
</template>

<script>
import L from 'leaflet'
import axios from 'axios'
import {mapActions, mapGetters} from 'vuex'
import LeafletLocateControl from './LeafletLocateControl'

export default {
  name: 'ContributeMap',
  components: {
    LeafletLocateControl
  },
  data () {
    return {
      isReady: false,
      perimeter: null,
      perimeterOptions: {
        style: function () {
          return {
            weight: 2,
            color: '#4C5D71',
            opacity: 1,
            fillColor: '#FFFFFF',
            fillOpacity: 0,
            className: 'perimeter'
          }
        }
      },
      contributionOptions: {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, {
            radius: 4,
            weight: 1,
            color: '#7A3432',
            opacity: 1,
            fillColor: '#FA6B67',
            fillOpacity: 1,
            className: 'contribution'
          })
        },
        onEachFeature: function (feature, layer) {
          layer.bindPopup(`<div class="media">
            <div class="media-content">
            <div class="content">
            <p>
            <strong>${feature.properties.group}</strong>
            <br>
            <small>
            <span class="has-text-info">${feature.properties.date_time}&nbsp;</span>
            <span class="has-text-grey">&ndash;&nbsp;</span>
            <span class="has-text-grey">nombre&nbsp;:&nbsp;</span>
            <span class="has-text-info">
            ${feature.properties.accuracy}&nbsp;${feature.properties.count}
            </span>
            </p>
            </div>
            </div>
            </div>`)
        }
      }
    }
  },
  computed: {
    hasLatLng () {
      return this.latLng !== null
    },
    ...mapGetters('contribution', [
      'latLng'
    ]),
    ...mapGetters('map', [
      'center',
      'zoom'
    ]),
    ...mapGetters([
      'perimeterUrl',
      'contributions'
    ])
  },
  methods: {
    transmitClick (ev) {
      if (ev.originalEvent.target.classList.contains('perimeter') &&
        this.zoom >= 14) {
        this.updateLatLng(ev.latlng)
        this.$emit('perimeter-click')
      } else if (ev.originalEvent.target.classList.contains('perimeter') &&
        this.zoom < 14) {
        this.$toast.open({
          duration: 3000,
          message: 'Zoom insuffisant',
          type: 'is-danger'
        })
      }
    },
    reEmitClick (ev) {
      this.$emit('perimeter-click')
    },
    zoomOnPerimeter (ev) {
      if (this.isReady) return
      if (!this.$refs.perimeter.mapObject) return
      const perimeterBounds = this.$refs.perimeter.getBounds()
      if (perimeterBounds.hasOwnProperty('_southWest')) {
        this.$refs.map.fitBounds(perimeterBounds)
        this.isReady = true
      }
    },
    updateZoomFromMap (ev) {
      this.updateZoom(this.$refs.map.mapObject.getZoom())
    },
    ...mapActions('contribution', [
      'updateLatLng'
    ]),
    ...mapActions('map', [
      'updateZoom'
    ])
  },
  async created () {
    try {
      const response = await axios.get(this.perimeterUrl)
      this.perimeter = response.data
    } catch (e) {
      console.log(e)
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
