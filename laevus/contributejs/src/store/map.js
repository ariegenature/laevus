export default {
  namespaced: true,
  state () {
    return {
      center: {
        lat: 0,
        lng: 0
      },
      zoom: 1
    }
  },
  getters: {
    center: (state) => {
      return [state.center.lng, state.center.lat]
    },
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
