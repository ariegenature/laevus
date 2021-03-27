import axios from 'axios'

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
    addTileProvider: (state, obj) => {
      state.tileProviders.push(obj)
    },
    center: (state, center) => {
      state.center = center
    },
    zoom: (state, zoom) => {
      state.zoom = zoom
    }
  },
  actions: {
    loadTileProviders: async ({ commit }) => {
      try {
        var response = await axios.get('api/map-layer')
        response.data.layers.sort((a, b) => {
          return a.order - b.order
        })
        response.data.layers.forEach((provider) => {
          provider.visible = false
          commit('addTileProvider', provider)
        })
      } catch (e) {
        console.warn(e)
      }
    },
    updateCenter: ({ commit }, center) => {
      commit('center', center)
    },
    updateZoom: ({ commit }, zoom) => {
      commit('zoom', zoom)
    }
  }
}
