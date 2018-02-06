<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'

const props = {
  position: {
    type: String,
    default: 'topleft'
  },
  polyline: {
    type: Boolean,
    default: true
  },
  polygon: {
    type: Boolean,
    default: true
  },
  rectangle: {
    type: Boolean,
    default: true
  },
  circle: {
    type: Boolean,
    default: true
  },
  marker: {
    type: Boolean,
    default: true
  },
  circleMarker: {
    type: Boolean,
    default: true
  },
  polylineOptions: {
    type: Object,
    default: () => ({})
  },
  polygonOptions: {
    type: Object,
    default: () => ({})
  },
  rectangleOptions: {
    type: Object,
    default: () => ({})
  },
  circleOptions: {
    type: Object,
    default: () => ({})
  },
  markerOptions: {
    type: Object,
    default: () => ({})
  },
  circleMarkerOptions: {
    type: Object,
    default: () => ({})
  }
}

export default {
  name: 'LeafletDraw',
  props: props,
  mounted () {
    var drawOptions = {}
    Object.assign(drawOptions, {
      polyline: this.polyline ? this.polylineOptions : false,
      polygon: this.polygon ? this.polylgonOptions : false,
      rectangle: this.rectangle ? this.rectangleOptions : false,
      circle: this.circle ? this.circleOptions : false,
      marker: this.marker ? this.markerOptions : false,
      circlemarker: this.circleMarker ? this.circleMarkerOptions : false
    })
    var options = {
      position: this.position,
      draw: drawOptions
    }
    this.mapObject = new L.Control.Draw(options)
    if (this.$parent._isMounted) {
      this.deferredMountedTo(this.$parent.mapObject)
    }
  },
  methods: {
    deferredMountedTo (parent) {
      this.parent = parent
      parent.addControl(this.mapObject)
    }
  }
}
</script>
