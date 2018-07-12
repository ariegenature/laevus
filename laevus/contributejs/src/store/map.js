export default {
  namespaced: true,
  state () {
    return {
      center: {
        lat: 0,
        lng: 0
      },
      tileProviders: [
        {
          name: 'OpenStreetMap Standard',
          visible: true,
          attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
          url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        },
        {
          name: 'Cartes IGN',
          visible: false,
          attribution: '&copy; <a target="_blank" href="http://ign.fr/">IGN</a>',
          url: 'http://mapproxy.priv.ariegenature.fr/mapproxy/service/?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ign_maps_3857&STYLE=default&FORMAT=image/png&TILEMATRIXSET=GLOBAL_WEBMERCATOR&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}'
        },
        {
          name: 'Orthophoto IGN',
          visible: false,
          attribution: '&copy; <a target="_blank" href="http://ign.fr/">IGN</a>',
          url: 'http://mapproxy.priv.ariegenature.fr/mapproxy/service/?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=bdortho_3857&STYLE=default&FORMAT=image/png&TILEMATRIXSET=GLOBAL_WEBMERCATOR&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}'
        }
      ],
      zoom: 1
    }
  },
  getters: {
    center: (state) => {
      return [state.center.lat, state.center.lng]
    },
    tileProviders: (state) => state.tileProviders,
    zoom: (state) => state.zoom
  },
  mutations: {
    center: (state, center) => {
      state.center = center
    },
    zoom: (state, zoom) => {
      state.zoom = zoom
    }
  },
  actions: {
    updateCenter: ({ commit }, center) => {
      commit('center', center)
    },
    updateZoom: ({ commit }, zoom) => {
      commit('zoom', zoom)
    }
  }
}
