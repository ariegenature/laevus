<template>
  <div class="hero">
    <div class="hero-body">
      <div class="container">
        <form action="">
          <form-wizard ref="wizard" @on-complete="$parent.close()" @on-change="handleStepChange"
                       title="" subtitle="" step-size="xs"
                       next-button-text="Suivant" back-button-text="Retour"
                       finish-button-text="Terminer">
            <tab-content title="Date et heure">
              <b-field grouped group-multiline>
                <b-field label="Date">
                  <b-datepicker ref="firstFieldInTab0" placeholder="Cliquer pour choisir une date"
                                icon="calendar" :readonly="false" :date-parser="parseFrenchDate"
                                v-model="selectedDate"></b-datepicker>
                </b-field>
                <b-field label="Heure">
                  <b-timepicker placeholder="Cliquer pour indiquer un horaire"
                                icon="clock-o" :readonly="false"
                                v-model="selectedTime"></b-timepicker>
                </b-field>
              </b-field>
            </tab-content>
            <tab-content title="Identification grossière">
              <div class="columns is-centered">
                <div class="column has-text-centered" v-for="group in groups">
                  <b-radio href="#" :value="groupId" @input="nextTab(group.id)"
                           size="is-small" :native-value="group.id">
                    <figure class="image is-64x64 block-center">
                      <img :alt="group.name" :src="group.icon">
                    </figure>
                    <p class="is-size-7">{{ group.name }}</p>
                  </b-radio>
                </div>
              </div>
            </tab-content>
            <tab-content title="Identification précise">
              <b-field label="Espèce">
                <b-autocomplete expanded icon="magnify" ref="firstFieldInTab2"
                                placeholder="Commencer à écrire pour chercher"
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
                      :value="count" @input="updateCount"></b-input>
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
            <tab-content title="Coordonnées">
              <b-field grouped group-multiline>
                <b-field label="Votre prénom" expanded>
                  <b-input expanded :value="firstName" @input="updateFirstName"
                    ref="firstFieldInTab3"></b-input>
                </b-field>
                <b-field label="Votre nom" expanded>
                  <b-input expanded :value="surname" @input="updateSurname"></b-input>
                </b-field>
              </b-field>
              <b-field label="Votre adresse électronique" expanded>
                <b-input type="email "placeholder="prenom.nom@example.org"
                         :value="email" @input="updateEmail"></b-input>
              </b-field>
            </tab-content>
          </form-wizard>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
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
      species: []
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
    ...mapGetters('contribution', [
      'date',
      'time',
      'groupId',
      'specieId',
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
    nextTab (groupId) {
      if (groupId !== this.groupId) {
        this.updateGroupId(groupId)
        this.updateSpecieId(null)
        this.updateInputSpecies('')
        this.updateSpeciesList(groupId)
      }
      this.$refs.wizard.nextTab()
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
    updateSpeciesList (groupId) {
      if (groupId) {
        var speciesGroup = this.speciesGroups.filter(obj => obj.groupId === groupId)
        this.species = speciesGroup ? speciesGroup[0].species : []
      } else {
        this.species = []
      }
    },
    updateInputSpecies (specieId) {
      if (specieId) {
        var species = this.species.filter(obj => obj.taxrefId === specieId)
        this.inputSpecies = species ? species[0].name : ''
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
    ...mapActions('contribution', [
      'updateDateTimeDate',
      'updateDateTimeTime',
      'updateGroupId',
      'updateSpecieId',
      'updateCountAccuracyId',
      'updateCount',
      'toggleAlive',
      'updateComments',
      'updateFirstName',
      'updateSurname',
      'updateEmail'
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
    }
  },
  mounted () {
    this.selectedDate = this.date ? this.date : new Date()
    this.selectedTime = this.time ? this.time : new Date()
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
  .vue-form-wizard .wizard-nav-pills li,
  .wizard-progress-with-circle {
    display: none
  }
  .vue-form-wizard .wizard-nav-pills li.active {
    display: block
  }
}
</style>
