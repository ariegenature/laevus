<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'

const mapEvents = [
  L.Draw.Event.CREATED,
  L.Draw.Event.EDITED,
  L.Draw.Event.DELETED,
  L.Draw.Event.DRAWSTART,
  L.Draw.Event.DRAWSTOP,
  L.Draw.Event.DRAWVERTEX,
  L.Draw.Event.EDITSTART,
  L.Draw.Event.EDITMOVE,
  L.Draw.Event.EDITRESIZE,
  L.Draw.Event.EDITVERTEX,
  L.Draw.Event.EDITSTOP,
  L.Draw.Event.DELETESTART,
  L.Draw.Event.DELETESTOP
]

const toolbarEvents = [
  L.Draw.Event.TOOLBAROPENED,
  L.Draw.Event.TOOLBARCLOSED
]

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
      for (var drawEvent of mapEvents) {
        parent.on(drawEvent, (ev) => {
          this.$parent.$emit(`l-${ev.type.replace(/:/g, '-')}`, ev)
        })
      }
      for (drawEvent of toolbarEvents) {
        parent.on(drawEvent, (ev) => {
          this.$emit(`l-${ev.type.replace(/:/g, '-')}`, ev)
        })
      }
    }
  }
}
</script>
