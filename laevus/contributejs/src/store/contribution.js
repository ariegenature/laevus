export default {
  namespaced: true,
  state () {
    return {
      latLng: null,
      dateTime: null,
      groupId: null,
      groupHasParent: false,
      specieId: null,
      canTellSpecies: true,
      countAccuracyId: '=',
      count: 1,
      isAlive: false,
      comments: null,
      firstName: null,
      surname: null,
      email: null
    }
  },
  getters: {
    latLng: (state) => state.latLng,
    date: (state) => state.dateTime,
    time: (state) => state.dateTime,
    groupId: state => state.groupId,
    groupHasParent: state => state.groupHasParent,
    specieId: state => state.specieId,
    canTellSpecies: state => state.canTellSpecies,
    countAccuracyId: state => state.countAccuracyId,
    count: state => state.count,
    isAlive: state => state.isAlive,
    comments: state => state.comments,
    firstName: state => state.firstName,
    surname: state => state.surname,
    email: state => state.email
  },
  mutations: {
    latLng: (state, latLng) => {
      state.latLng = latLng
    },
    dateTime: (state, dt) => {
      state.dateTime = dt
    },
    groupId: (state, groupId) => {
      state.groupId = groupId
    },
    groupHasParent: (state, groupHasParent) => {
      state.groupHasParent = groupHasParent
    },
    specieId: (state, specieId) => {
      state.specieId = specieId
    },
    canTellSpecies: (state, canTellSpecies) => {
      state.canTellSpecies = canTellSpecies
    },
    countAccuracyId: (state, accuracyId) => {
      state.countAccuracyId = accuracyId
    },
    count: (state, count) => {
      state.count = Number(count)
    },
    toggleAlive: (state) => {
      state.isAlive = !state.isAlive
    },
    comments: (state, comments) => {
      state.comments = comments
    },
    firstName: (state, firstName) => {
      state.firstName = firstName
    },
    surname: (state, surname) => {
      state.surname = surname
    },
    email: (state, email) => {
      state.email = email
    }
  },
  actions: {
    updateLatLng: ({ commit, state }, latLng) => {
      commit('latLng', latLng)
    },
    updateDateTimeDate: ({ commit, state }, date) => {
      var dt = state.dateTime ? state.dateTime : new Date()
      var year = date.getFullYear()
      var month = date.getMonth()
      var day = date.getDate()
      var hours = dt.getHours()
      var minutes = dt.getMinutes()
      commit('dateTime', new Date(year, month, day, hours, minutes))
    },
    updateDateTimeTime: ({ commit, state }, time) => {
      var dt = state.dateTime ? state.dateTime : new Date()
      var year = dt.getFullYear()
      var month = dt.getMonth()
      var day = dt.getDate()
      var hours = time.getHours()
      var minutes = time.getMinutes()
      commit('dateTime', new Date(year, month, day, hours, minutes))
    },
    updateGroupId: ({ commit }, groupId) => {
      commit('groupId', groupId)
    },
    updateGroupHasParent: ({ commit }, groupHasParent) => {
      commit('groupHasParent', groupHasParent)
    },
    updateSpecieId: ({ commit }, specieId) => {
      commit('specieId', specieId)
    },
    updateCanTellSpecies: ({ commit }, canTellSpecies) => {
      commit('canTellSpecies', canTellSpecies)
    },
    updateCountAccuracyId: ({ commit }, accuracyId) => {
      commit('countAccuracyId', accuracyId)
    },
    updateCount: ({ commit }, count) => {
      commit('count', count)
    },
    toggleAlive: ({ commit }) => {
      commit('toggleAlive')
    },
    updateComments: ({ commit }, comments) => {
      commit('comments', comments)
    },
    updateFirstName: ({ commit }, firstName) => {
      commit('firstName', firstName)
    },
    updateSurname: ({ commit }, surname) => {
      commit('surname', surname)
    },
    updateEmail: ({ commit }, email) => {
      commit('email', email)
    }
  }
}
