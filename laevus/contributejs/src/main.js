// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import App from './App'
import Buefy from 'buefy'
import Vue from 'vue'
import Vue2Leaflet from 'vue2-leaflet'
import VueFormWizard from 'vue-form-wizard'
import router from './router'
import store from './store'
import 'buefy/lib/buefy.css'

Vue.config.productionTip = false

Vue.component('v-map', Vue2Leaflet.Map)
Vue.component('v-tilelayer', Vue2Leaflet.TileLayer)
Vue.component('v-marker', Vue2Leaflet.Marker)
Vue.component('v-geojson-layer', Vue2Leaflet.GeoJSON)

Vue.use(Buefy, {
  defaultIconPack: 'fa'
})
Vue.use(VueFormWizard)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  store
})
