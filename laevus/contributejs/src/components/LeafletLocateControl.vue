<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet.locatecontrol'
import 'leaflet.locatecontrol/dist/L.Control.Locate.css'

const props = {
  position: {
    type: String,
    default: 'topleft'
  },
  markerClass: {
    type: Function,
    default: L.CircleMarker
  },
  icon: {
    type: String,
    default: 'fa fa-bullseye'
  },
  showPopup: {
    type: Boolean,
    default: true
  },
  controlHelp: {
    type: String,
    default: 'Où suis-je ?'
  },
  metersUnit: {
    type: String,
    default: 'mètres'
  },
  feetUnit: {
    type: String,
    default: 'pieds'
  },
  popupMessage: {
    type: String,
    default: 'Vous êtes à {distance} {unit} de ce point'
  },
  outsideMapBoundsMsg: {
    type: String,
    default: 'Votre position semble être en dehors des limites de la carte'
  }
}

export default {
  name: 'LeafletLocateControl',
  props,
  mounted () {
    var locateOptions = {}
    Object.assign(locateOptions, {
      position: this.position,
      markerClass: this.markerClass,
      icon: this.icon,
      showPopup: this.showPopup,
      strings: {
        title: this.controlHelp,
        metersUnit: this.metersUnit,
        feetUnit: this.feetUnit,
        popup: this.popupMessage,
        outsideMapBoundsMsg: this.outsideMapBoundsMsg
      }
    })
    this.mapObject = new L.Control.Locate(locateOptions)
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
