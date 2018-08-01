import axios from 'axios'
import introJs from 'intro.js'
import Vue from 'vue'
import Vuex from 'vuex'

import contribution from './contribution'
import map from './map'

Vue.use(Vuex)

export default new Vuex.Store({
  state () {
    return {
      perimeterUrl: window.location.origin + '/static/perimeter.geojson',
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
      mapReady: false,
      groups: null,
      speciesGroups: null,
      contributions: null,
      isLoading: false,
      currentUser: null,
      intro: introJs(),
      isHelpShown: false,
      selectedFeatureId: null
    }
  },
  getters: {
    perimeterUrl: (state) => state.perimeterUrl,
    groups: (state) => state.groups,
    speciesGroups: (state) => state.speciesGroups,
    accuracies: (state) => state.accuracies,
    mapReady: (state) => state.mapReady,
    contributions: (state) => state.contributions,
    isLoading: (state) => state.isLoading,
    currentUser: (state) => state.currentUser,
    intro: (state) => state.intro,
    isAuthenticated: (state) => state.currentUser !== null,
    isHelpShown: (state) => state.isHelpShown,
    selectedFeatureId: (state) => state.selectedFeatureId
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
    mapReady: (state) => {
      state.mapReady = true
    },
    ready: (state) => {
      state.isLoading = false
    },
    currentUser: (state, user) => {
      state.currentUser = user
    },
    isHelpShown: (state, bool) => {
      state.isHelpShown = bool
    },
    selectedFeatureId: (state, id) => {
      state.selectedFeatureId = id
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
    setMapReady: ({ commit }) => {
      commit('mapReady')
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
    },
    updateSelectedFeatureId: ({ commit }, id) => {
      commit('selectedFeatureId', id)
    }
  },
  modules: {
    contribution,
    map
  }
})
