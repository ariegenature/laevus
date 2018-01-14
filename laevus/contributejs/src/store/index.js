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
      speciesGroups: [
        {
          groupId: 'large-mammal',
          species: [
            {
              taxrefId: 60981,
              name: 'Sanglier [Sus scrofa Linnaeus, 1758]'
            },
            {
              taxrefId: 61057,
              name: 'Chevreuil européen [Capreolus capreolus (Linnaeus, 1758)]'
            },
            {
              taxrefId: 61057,
              name: 'Chevreuil européen [Capreolus capreolus (Linnaeus, 1758)]'
            },
            {
              taxrefId: 61000,
              name: 'Cerf élaphe [Cervus elaphus Linnaeus, 1758]'
            },
            {
              taxrefId: 61128,
              name: 'Isard [Rupicapra pyrenaica Bonaparte, 1845]'
            },
            {
              taxrefId: 61028,
              name: 'Daim européen [Rupicapra pyrenaica Bonaparte, 1845]'
            },
            {
              taxrefId: 199194,
              name: 'Mouflon [Ovis gmelinii musimon (Pallas, 1811)]'
            }
          ]
        },
        {
          groupId: 'small-mammal',
          species: [
          ]
        },
        {
          groupId: 'reptile',
          species: [
          ]
        },
        {
          groupId: 'amphibian',
          species: [
          ]
        },
        {
          groupId: 'bat',
          species: [
          ]
        },
        {
          groupId: 'bird',
          species: [
          ]
        }
      ]
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
