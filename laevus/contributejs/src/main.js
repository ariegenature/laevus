// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import App from './App'
import Buefy from 'buefy'
import VTooltip from 'v-tooltip'
import Vue from 'vue'
import Vue2Leaflet from 'vue2-leaflet'
import VueFormWizard from 'vue-form-wizard'
import router from './router'
import store from './store'
import 'buefy/lib/buefy.css'

Vue.config.productionTip = false

Vue.component('l-map', Vue2Leaflet.LMap)
Vue.component('l-control-layers', Vue2Leaflet.LControlLayers)
Vue.component('l-tile-layer', Vue2Leaflet.LTileLayer)
Vue.component('l-marker', Vue2Leaflet.LMarker)
Vue.component('l-geojson', Vue2Leaflet.LGeoJson)

Vue.use(Buefy, {
  defaultIconPack: 'fa'
})
Vue.use(VueFormWizard)
Vue.use(VTooltip)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  store
})
