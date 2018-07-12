<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet.locatecontrol'
import 'leaflet.locatecontrol/dist/L.Control.Locate.css'

export default {
  name: 'LeafletLocateControl',
  mounted () {
    this.mapObject = new L.Control.Locate()
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
