import axios from 'axios'
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
      isLoading: false,
      currentUser: null,
      isHelpShown: false
    }
  },
  getters: {
    perimeterUrl: (state) => state.perimeterUrl,
    groups: (state) => state.groups,
    speciesGroups: (state) => state.speciesGroups,
    accuracies: (state) => state.accuracies,
    contributions: (state) => state.contributions,
    isLoading: (state) => state.isLoading,
    currentUser: (state) => state.currentUser,
    isAuthenticated: (state) => state.currentUser !== null,
    isHelpShown: (state) => state.isHelpShown
  },
  mutations: {
    groups: (state, groups) => {
      state.groups = groups
    },
    contributions: (state, contributions) => {
      state.contributions = contributions
    },
    loading: (state) => {
      state.isLoading = true
    },
    ready: (state) => {
      state.isLoading = false
    },
    currentUser: (state, user) => {
      state.currentUser = user
    },
    isHelpShown: (state, bool) => {
      state.isHelpShown = bool
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
    },
    syncCurrentUser: async ({ commit }, user) => {
      try {
        const response = await axios.get('api/current-user')
        commit('currentUser', response.data)
      } catch (e) {
        console.log(e)
      }
    },
    toggleHelp: ({ commit, state }) => {
      commit('isHelpShown', !state.isHelpShown)
    }
  },
  modules: {
    contribution,
    map
  }
})
