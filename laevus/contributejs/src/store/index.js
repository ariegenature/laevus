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
      groups: null,
      speciesGroups: null,
      contributions: null,
      isLoading: false
    }
  },
  getters: {
    perimeterUrl: (state) => state.perimeterUrl,
    groups: (state) => state.groups,
    speciesGroups: (state) => state.speciesGroups,
    accuracies: (state) => state.accuracies,
    contributions: (state) => state.contributions,
    isLoading: (state) => state.isLoading
  },
  mutations: {
    groups: (state, groups) => {
      state.groups = groups
    },
    contributions: (state, contributions) => {
      state.contributions = contributions
    },
    loading: (state) => {
      console.log('loading')
      state.isLoading = true
    },
    ready: (state) => {
      console.log('ready')
      state.isLoading = false
    }
  },
  actions: {
    setGroups: ({ commit, state }, groups) => {
      commit('groups', groups)
    },
    setContributions: ({ commit, state }, contributions) => {
      commit('contributions', contributions)
    },
    setPageLoading: ({ commit }) => {
      commit('loading')
    },
    setPageReady: ({ commit }) => {
      commit('ready')
    }
  },
  modules: {
    contribution,
    map
  }
})
