import Vue from 'vue'
import Vuex from 'vuex'

import contribution from './contribution'

Vue.use(Vuex)

export default new Vuex.Store({
  state () {
    return {
      groups: [
        {
          id: 'large-mammal',
          name: 'Grand mammifère',
          icon: 'static/deer.png'
        },
        {
          id: 'small-mammal',
          name: 'Petit mammifère',
          icon: 'assets/deer.png'
        },
        {
          id: 'reptile',
          name: 'Reptile',
          icon: 'assets/deer.png'
        },
        {
          id: 'amphibian',
          name: 'Amphibien',
          icon: 'assets/deer.png'
        },
        {
          id: 'bat',
          name: 'Chauve-souris',
          icon: 'assets/deer.png'
        },
        {
          id: 'bird',
          name: 'Oiseau',
          icon: 'assets/deer.png'
        }
      ]
    }
  },
  getters: {
    groups: (state) => state.groups
  },
  modules: {
    contribution
  }
})
