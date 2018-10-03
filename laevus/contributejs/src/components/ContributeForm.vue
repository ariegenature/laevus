<template>
  <form id="contribute-form" method="POST" accept-charset="UTF-8"
        v-on:submit.prevent>
    <form-wizard ref="wizard" @on-change="handleStepChange"
                 title="" subtitle="" step-size="xs"
                 next-button-text="Suivant" back-button-text="Retour"
                 finish-button-text="Terminer" @on-complete="submitForm">
      <tab-content title="Date et heure">
        <div class="columns is-centered">
          <div class="column is-narrow has-text-centered">
            <b-field grouped group-multiline>
              <b-field label="Date">
                <b-datepicker ref="firstFieldInTab0" inline size="is-small"
                              :readonly="false" :date-parser="parseFrenchDate"
                              v-model="selectedDate"></b-datepicker>
              </b-field>
              <b-field label="Heure">
                <b-timepicker inline size="is-small" :readonly="false"
                              v-model="selectedTime"></b-timepicker>
              </b-field>
            </b-field>
          </div>
        </div>
      </tab-content>
      <tab-content title="Identification" :before-change="checkGroupNotNull">
        <b-field v-if="groupHasParent">
          <div class="control">
            <button class="button is-small" @click="resetGroups">
              <b-icon icon="level-up"></b-icon>
              <span>Remonter</span>
            </button>
          </div>
        </b-field>
        <div id="groups" class="columns is-multiline is-centered">
          <div class="column is-one-third has-text-centered" v-for="group in groups" :key="group.id">
            <b-radio href="#" :value="groupId" @input="browseGroups(group.id)"
                     size="is-small" :native-value="group.id">
              <figure class="image is-64x64 block-center">
                <img :alt="group.name" :src="group.icon">
              </figure>
              <p class="is-size-7">
              {{ group.name }}
              </p>
            </b-radio>
            <v-popover container="#groups" popover-base-class="v-tooltip popover"
                       popover-class="column is-one-third" v-if="group.html_description">
              <b-icon icon="question-circle" custom-class="tooltip-target" size="is-small"></b-icon>
              <template slot="popover">
                <span v-html="group.html_description" class="is-size-7"></span>
              </template>
            </v-popover>
          </div>
          <div class="column is-one-third has-text-centered" v-if="groupHasParent">
            <b-radio href="#" :value="groupId" @input="browseGroups(null)" size="is-small"
                     native-value="unknown">
              <figure class="image is-64x64 block-center">
                <img alt="Intérrogation" src="static/question.png">
              </figure>
              <p class="is-size-7">Je ne sais pas</p>
            </b-radio>
          </div>
        </div>
      </tab-content>
      <tab-content title="Détails" :before-change="checkCountAndSpecies">
        <b-field label="Espèce" v-if="hasOneSpecies">
          <div class="control">
            <input class="input is-static" :value="oneSpecies" readonly>
          </div>
        </b-field>
        <b-field v-if="hasMultipleSpecies">
          <b-switch :value="canTellSpecies" @input="updateCanTellSpecies">
            {{ canTellSpeciesString }}
          </b-switch>
        </b-field>
        <b-field label="Espèce" v-if="hasMultipleSpecies && canTellSpecies">
          <b-autocomplete expanded icon="magnify" ref="firstFieldInTab2"
                          placeholder="Commencer à écrire pour chercher" keep-first
                          v-model="inputSpecies" :data="filteredSpecies" field="name"
                          @select="selectSpecies"></b-autocomplete>
        </b-field>
        <b-field grouped group-multiline>
          <b-field label="Nombre d'individus" :message="selectedAccuracy" expanded>
            <b-field>
              <b-select :value="countAccuracyId" @input="updateCountAccuracy">
                <option v-for="accuracy in accuracies"
                        :value="accuracy.id" :key="accuracy.id"
                        v-html="accuracy.id">
                </option>
              </b-select>
              <b-input icon="magnify" type="number" placeholder="Combien d'individus ?"
                       :value="count" @input="updateCount" min="1"></b-input>
            </b-field>
          </b-field>
          <b-field label="Vivant ou mort ?">
            <b-switch true-value="Vivant" false-value="Mort" v-model="selectedAlive">
              {{ aliveString }}
            </b-switch>
          </b-field>
        </b-field>
        <b-field label="Commentaires">
          <b-input type="textarea"
                   placeholder="Vous pouvez apporter des précisions ou des remarques"
                   :value="comments" @input="updateComments"></b-input>
        </b-field>
      </tab-content>
      <tab-content title="Coordonnées" :before-change="checkCompleteContact">
        <b-message title="Erreur" type="is-danger" :active.sync="hasServerErrors">
          {{ errorMsg }}
        </b-message>
        <b-field grouped group-multiline>
          <b-field label="Votre prénom" expanded>
            <b-input expanded id="first-name" :value="firstName" @input="updateFirstName"
                     ref="firstFieldInTab3" autocomplete="given-name"
                     @keyup.native.enter="giveFocusToField('surname')"></b-input>
          </b-field>
          <b-field label="Votre nom" expanded>
            <b-input expanded id="surname" :value="surname" @input="updateSurname"
                     ref="surname" autocomplete="family-name"
                     @keyup.native.enter="giveFocusToField('email')"></b-input>
          </b-field>
        </b-field>
        <b-field label="Votre adresse électronique" expanded>
          <b-input type="email" id="email" placeholder="prenom.nom@example.org"
                   ref="email" autocomplete="email" :value="email" @input="updateEmail"></b-input>
        </b-field>
        <div class="field">
          <div class="control">
            <input type="hidden" name="csrf_token" value="«« csrf_token() »»">
          </div>
        </div>
      </tab-content>
    </form-wizard>
  </form>
</template>

<script>
import axios from 'axios'
import {FormWizard, TabContent} from 'vue-form-wizard'
import {mapActions, mapGetters} from 'vuex'
import 'vue-form-wizard/dist/vue-form-wizard.min.css'

export default {
  name: 'ContributeForm',
  components: {
    FormWizard,
    TabContent
  },
  data () {
    return {
      selectedDate: null,
      selectedTime: null,
      selectedAlive: false,
      selectedAccuracy: '',
      inputSpecies: '',
      species: [],
      parentGroupId: null,
      errorMsg: '',
      emailRegExp: /^([a-zA-Z0-9.+-]+@[a-zA-Z\d-]+(\.[a-zA-Z\d-]+)+)$/
    }
  },
  computed: {
    filteredSpecies () {
      return this.species.filter((obj) => {
        return obj.name.toString().toLowerCase().indexOf(this.inputSpecies.toLowerCase()) >= 0
      })
    },
    aliveString () {
      return this.isAlive ? 'Vivant' : 'Mort'
    },
    canTellSpeciesString () {
      return this.canTellSpecies ? "Je peux identifier l'espèce précise" : "Je ne sais pas identifier l'espèce précise"
    },
    hasServerErrors () {
      return Boolean(this.errorMsg)
    },
    hasOneSpecies () {
      return this.species.length === 1
    },
    oneSpecies () {
      return this.species.length === 1 ? this.species[0] : null
    },
    hasMultipleSpecies () {
      return this.species.length > 1
    },
    ...mapGetters('contribution', [
      'latLng',
      'date',
      'time',
      'groupId',
      'groupHasParent',
      'specieId',
      'canTellSpecies',
      'countAccuracyId',
      'count',
      'isAlive',
      'comments',
      'firstName',
      'surname',
      'email'
    ]),
    ...mapGetters([
      'groups',
      'speciesGroups',
      'accuracies'
    ])
  },
  methods: {
    async browseGroups (groupId) {
      if (groupId && groupId !== this.groupId) {
        this.parentGroupId = this.groupId
        this.updateGroupId(groupId)
        this.updateSpecieId(null)
        this.updateInputSpecies('')
        this.updateSpeciesList(null)
        this.setPageLoading()
        try {
          const childGroups = await axios.get(`api/child-group/${groupId}`)
          if (childGroups.data && childGroups.data.length) {
            this.setGroups(childGroups.data)
            this.updateGroupHasParent(true)
          } else {
            this.updateSpeciesList(groupId)
            this.$refs.wizard.nextTab()
          }
        } catch (e) {
          console.log(e)
        }
        this.setPageReady()
      } else if (groupId === null && this.groupId !== null) {
        this.updateGroupId(this.parentGroupId ? this.parentGroupId : this.groupId)
        this.updateSpecieId(null)
        this.updateInputSpecies('')
        this.updateSpeciesList(null)
        this.$refs.wizard.nextTab()
      }
    },
    async resetGroups () {
      this.parentGroupId = null
      this.updateGroupId(null)
      this.updateSpecieId(null)
      this.updateInputSpecies('')
      this.updateSpeciesList(null)
      this.updateGroupHasParent(false)
      this.setPageLoading()
      try {
        const childGroups = await axios.get(`api/child-group`)
        this.setGroups(childGroups.data)
      } catch (e) {
        console.log(e)
      }
      this.setPageReady()
    },
    checkGroupNotNull () {
      if (this.groupId === null) {
        this.$toast.open({
          message: 'Veuillez choisir une catégorie',
          duration: 3000,
          type: 'is-danger'
        })
        return false
      } else {
        return true
      }
    },
    checkCompleteContact () {
      if (!this.firstName || !this.surname || !this.email) {
        this.$toast.open({
          message: 'Veuillez saisir tous les champs',
          duration: 3000,
          type: 'is-danger'
        })
        return false
      } else if (!this.email.match(this.emailRegExp)) {
        this.$toast.open({
          message: 'Veuillez saisir une adresse électronique valide',
          duration: 3000,
          type: 'is-danger'
        })
      } else {
        return true
      }
    },
    checkCountAndSpecies () {
      if (this.count < 1) {
        this.$toast.open({
          message: 'Veuillez saisir un entier ≥ 1',
          duration: 3000,
          type: 'is-danger'
        })
        return false
      } else if (this.canTellSpecies && this.specieId === null) {
        this.$toast.open({
          message: "Veuillez saisir une espèce ou indiquer que vous savez pas l'identifier",
          duration: 3000,
          type: 'is-danger'
        })
        return false
      } else {
        return true
      }
    },
    parseFrenchDate (strValue) {
      var dateArray = strValue.split('/').reverse()
      return new Date(dateArray[0], dateArray[1] - 1, dateArray[2])
    },
    handleStepChange (prevIndex, nextIndex) {
      this.giveFocusToFirstField(nextIndex)
    },
    giveFocusToFirstField (tabIndex) {
      var firstField = this.$refs[`firstFieldInTab${tabIndex}`]
      if (firstField && firstField.hasOwnProperty('focus')) {
        firstField.focus()
      }
    },
    giveFocusToField (ref) {
      var field = this.$refs[ref]
      if (field && field.hasOwnProperty('focus')) {
        field.focus()
      }
    },
    async updateSpeciesList (groupId) {
      if (groupId) {
        this.setPageLoading()
        try {
          const species = await axios.get(`api/taxon/${groupId}`)
          this.species = species.data.species
        } catch (e) {
          console.log(e)
        }
        this.setPageReady()
      } else {
        this.species = []
      }
    },
    updateInputSpecies (specieId) {
      if (specieId) {
        var species = this.species.filter(obj => obj.taxrefId === specieId)
        this.inputSpecies = species.length ? species[0].name : ''
      } else {
        this.inputSpecies = ''
      }
    },
    updateSelectedAccuracy (accuracyId) {
      var accuracies = this.accuracies.filter(obj => obj.id === accuracyId)
      this.selectedAccuracy = accuracies ? accuracies[0].title : ''
    },
    updateCountAccuracy (accuracyId) {
      this.updateSelectedAccuracy(accuracyId)
      this.updateCountAccuracyId(accuracyId)
    },
    selectSpecies (value) {
      if (value) {
        this.updateSpecieId(value.taxrefId)
      }
    },
    async submitForm (ev) {
      const firstName = this.firstName ? this.firstName : ''
      const surname = this.surname ? this.surname : ''
      const email = this.email ? this.email : ''
      var contributeData = new FormData()
      contributeData.append('geometry', `SRID=4326;POINT(${this.latLng.lng} ${this.latLng.lat})`)
      contributeData.append('date_time', this.date.toISOString())
      contributeData.append('group_id', this.groupId ? this.groupId : '')
      if (this.specieId) {
        contributeData.append('specie_id', this.specieId)
      }
      contributeData.append('count_accuracy_id', this.countAccuracyId)
      contributeData.append('count', this.count)
      contributeData.append('is_alive', this.isAlive)
      contributeData.append('comments', this.comments ? this.comments : '')
      contributeData.append('first_name', firstName)
      contributeData.append('surname', surname)
      contributeData.append('email', email)
      localStorage.setItem('firstName', firstName)
      localStorage.setItem('surname', surname)
      localStorage.setItem('email', email)
      this.setPageLoading()
      try {
        await axios.post('', contributeData, {
          headers: {
            'X-CSRFToken': '«« csrf_token() »»'
          }
        })
        this.resetGroups()
        this.updateLatLng(null)
        this.$parent.close()
      } catch (e) {
        this.errorMsg = e.response.data.message
      }
      this.setPageReady()
      this.setPageLoading()
      try {
        const response = await axios.get('api/contribution')
        this.setContributions(response.data)
      } catch (e) {
        console.log(e)
      }
      this.setPageReady()
    },
    ...mapActions('contribution', [
      'updateLatLng',
      'updateDateTimeDate',
      'updateDateTimeTime',
      'updateGroupId',
      'updateGroupHasParent',
      'updateSpecieId',
      'updateCanTellSpecies',
      'updateCountAccuracyId',
      'updateCount',
      'toggleAlive',
      'updateComments',
      'updateFirstName',
      'updateSurname',
      'updateEmail'
    ]),
    ...mapActions([
      'setGroups',
      'setContributions',
      'setPageLoading',
      'setPageReady'
    ])
  },
  watch: {
    selectedDate: function (value) {
      this.updateDateTimeDate(value)
    },
    selectedTime: function (value) {
      this.updateDateTimeTime(value)
    },
    selectedAlive: function (value) {
      this.toggleAlive()
    },
    canTellSpecies: function (value) {
      if (!value) {
        this.updateSpecieId(null)
        this.updateInputSpecies('')
      }
    }
  },
  mounted () {
    this.selectedDate = this.date ? this.date : new Date()
    this.selectedTime = this.time ? this.time : new Date()
    this.updateFirstName(localStorage.getItem('firstName') || '')
    this.updateSurname(localStorage.getItem('surname') || '')
    this.updateEmail(localStorage.getItem('email') || '')
    this.updateSpeciesList(this.groupId)
    this.updateInputSpecies(this.specieId)
    this.updateSelectedAccuracy(this.countAccuracyId)
    this.selectedAlive = this.isAlive
    this.giveFocusToFirstField(0)
  }
}
</script>

<style>
.block-center {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
@media screen and (max-width: 767px) {
  #contribute-form .vue-form-wizard .wizard-nav > li,
  .wizard-progress-with-circle {
    display: none
  }
  #contribute-form .vue-form-wizard .wizard-nav > li.active {
    display: block
  }
}
.popover-inner {
  background: #0f77ea;
  color: white;
  padding: 6px;
  border-radius: 3px;
  box-shadow: 0 5px 30px rgba(black, .1);
}
.popover-arrow {
  border-color: #0f77ea;
}
.popover-inner ul {
  list-style: '- ' inside;
}
</style>
