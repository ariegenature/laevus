<template>
  <l-map ref="map" :zoom="zoom" :center="center" @l-draw-created="transmitClick"
         @zoom="updateZoomFromMap" @layeradd="zoomOnPerimeter"
         @locationfound="updateMarker" @popupopen="selectFeature" @popupclose="unselectFeature">
    <l-marker :lat-lng="latLng" v-if="hasLatLng" @click="reEmitClick"></l-marker>
    <l-geojson ref="contribution" :geojson="contributions"
               :options="contributionOptions"></l-geojson>
    <l-geojson ref="perimeter" :geojson="perimeter"
               :options="perimeterOptions"></l-geojson>
    <leaflet-draw :marker="true" :polyline="false" :polygon="false" :rectangle="false"
                  :circle="false" :circle-marker="false" :edit="false"
                  :remove="false"></leaflet-draw>
    <leaflet-locate-control ref="geolocation"
                            :show-popup="false"></leaflet-locate-control>
    <l-control-layers></l-control-layers>
    <l-tile-layer v-for="tileProvider in tileProviders" :key="tileProvider.name" layerType="base"
                  :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url"
                  :attribution="tileProvider.attribution"></l-tile-layer>
  </l-map>
</template>

<script>
import L from 'leaflet'
import axios from 'axios'
import {mapActions, mapGetters} from 'vuex'
import LeafletDraw from './LeafletDraw'
import LeafletLocateControl from './LeafletLocateControl'

export default {
  name: 'ContributeMap',
  components: {
    LeafletDraw,
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
      'tileProviders',
      'zoom'
    ]),
    ...mapGetters([
      'perimeterUrl',
      'contributions',
      'selectedFeatureId'
    ])
  },
  methods: {
    transmitClick (ev) {
      if (this.zoom >= 14) {
        this.$refs.geolocation.mapObject.stop()
        this.updateLatLng(ev.layer._latlng)
        this.$emit('perimeter-click')
      } else {
        this.$toast.open({
          duration: 3000,
          message: 'Zoom insuffisant',
          type: 'is-danger'
        })
      }
    },
    updateMarker (ev) {
      this.updateLatLng(ev.latlng)
    },
    reEmitClick (ev) {
      this.$emit('perimeter-click')
    },
    selectFeature (ev) {
      this.$refs.contribution.mapObject.eachLayer((layer) => {
        if (layer.isPopupOpen()) {
          this.updateSelectedFeatureId(layer.feature.id)
        }
      })
    },
    unselectFeature (ev) {
      this.updateSelectedFeatureId(null)
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
    ]),
    ...mapActions([
      'updateSelectedFeatureId'
    ])
  },
  async created () {
    try {
      const response = await axios.get(this.perimeterUrl)
      this.perimeter = response.data
    } catch (e) {
      console.log(e)
    }
  },
  watch: {
    selectedFeatureId: {
      handler (val, oldVal) {
        this.$refs.contribution.mapObject.eachLayer((layer) => {
          if (layer.feature.id === val) {
            layer.openPopup()
          }
        })
      }
    }
  }
}
</script>

<style>
.perimeter {
  cursor: grab;
}
</style>
