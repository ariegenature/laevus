export default {
  namespaced: true,
  state () {
    return {
      latLng: null,
      dateTime: null,
      groupId: null,
      specieId: null,
      count: 1,
      isAlive: false,
      comments: null,
      firstName: null,
      surname: null,
      email: null
    }
  },
  getters: {
    date: (state) => state.dateTime,
    time: (state) => state.dateTime,
    groupId: state => state.groupId,
    specieId: state => state.specieId,
    count: state => state.count,
    isAlive: state => state.isAlive,
    comments: state => state.comments,
    firstName: state => state.firstName,
    surname: state => state.surname,
    email: state => state.email
  },
  mutations: {
    dateTime: (state, dt) => {
      state.dateTime = dt
    },
    groupId: (state, groupId) => {
      state.groupId = groupId
    },
    specieId: (state, specieId) => {
      state.specieId = specieId
    },
    count: (state, count) => {
      state.count = count
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
    updateSpecieId: ({ commit }, specieId) => {
      commit('specieId', specieId)
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
