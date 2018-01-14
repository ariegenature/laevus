import Vue from 'vue'
import Vuex from 'vuex'

import contribution from './contribution'
import map from './map'

Vue.use(Vuex)

export default new Vuex.Store({
  state () {
    return {
      perimeterUrl: window.location.origin + '/static/perimetre_pnr.geojson',
      accuracies: [
        {
          id: '=',
          title: 'exactement'
        },
        {
          id: '&cong;',
          title: 'environ'
        },
        {
          id: '&ge;',
          title: 'au moins'
        }
      ],
      groups: [],
      speciesGroups: []
    }
  },
  getters: {
    perimeterUrl: (state) => state.perimeterUrl,
    groups: (state) => state.groups,
    speciesGroups: (state) => state.speciesGroups,
    accuracies: (state) => state.accuracies
  },
  mutations: {
    groups: (state, groups) => {
      state.groups = groups
    }
  },
  actions: {
    setGroups: ({ commit, state }, groups) => {
      commit('groups', groups)
    }
  },
  modules: {
    contribution,
    map
  }
})
