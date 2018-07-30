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
