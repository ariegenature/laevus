<template>
  <div class="hero">
    <div class="hero-body">
      <div class="container">
        <form action="">
          <form-wizard ref="wizard" @on-complete="$parent.close()" title="" subtitle="" step-size="xs">
            <tab-content title="Date et heure">
              <b-field grouped group-multiline>
                <b-field label="Date">
                  <b-datepicker placeholder="Cliquer pour choisir une date"
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
                  <a href="#" @click="nextTab(group.id)">
                    <figure class="image is-64x64 block-center">
                      <img :alt="group.name" :src="group.icon">
                    </figure>
                    <p class="is-size-7">{{ group.name }}</p>
                  </a>
                </div>
              </div>
            </tab-content>
            <tab-content title="Identification précise">
              <b-field label="Espèce">
                <b-autocomplete expanded icon="magnify"
                                placeholder="Commencer à écrire pour chercher"
                                v-model="inputSpecies" :data="filteredSpecies" field="name"
                                @select="selectSpecies"></b-autocomplete>
              </b-field>
              <b-field grouped group-multiline>
                <b-field label="Nombre d'individus" expanded>
                  <b-field>
                    <b-select>
                      <option>=</option>
                      <option>&cong;</option>
                      <option>&ge;</option>
                    </b-select>
                    <b-input icon="magnify" type="number" placeholder="Combien d'individus ?"></b-input>
                  </b-field>
                </b-field>
                <b-field label="Vivant ou mort ?">
                  <b-switch true-value="Vivant" false-value="Mort">
                    Vivant ?
                  </b-switch>
                </b-field>
              </b-field>
              <b-field label="Commentaires">
                <b-input type="textarea" placeholder="Vous pouvez apporter des précisions ou des remarques"></b-input>
              </b-field>
            </tab-content>
            <tab-content title="Coordonnées">
              <b-field grouped group-multiline>
                <b-field label="Votre prénom" expanded>
                  <b-input expanded></b-input>
                </b-field>
                <b-field label="Votre nom" expanded>
                  <b-input expanded></b-input>
                </b-field>
              </b-field>
              <b-field label="Votre adresse électronique" expanded>
                <b-input type="email "placeholder="prenom.nom@example.org"></b-input>
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
    ...mapGetters('contribution', [
      'date',
      'time',
      'groupId',
      'specieId',
      'count',
      'isAlive',
      'comments',
      'firstName',
      'surname',
      'email'
    ]),
    ...mapGetters([
      'groups',
      'speciesGroups'
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
        var species = this.species.filter(obj => obj.taxrefId === this.specieId)
        this.inputSpecies = species ? species[0].name : ''
      } else {
        this.inputSpecies = ''
      }
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
    }
  },
  mounted () {
    this.selectedDate = this.date ? this.date : new Date()
    this.selectedTime = this.time ? this.time : new Date()
    this.updateSpeciesList(this.groupId)
    this.updateInputSpecies(this.specieId)
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
