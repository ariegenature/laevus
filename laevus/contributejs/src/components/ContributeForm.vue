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
                <b-input icon="magnify" type="search" placeholder="Commencer à écrire pour chercher"></b-input>
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
      selectedTime: null
    }
  },
  computed: {
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
      'groups'
    ])
  },
  methods: {
    nextTab (groupId) {
      this.updateGroupId(groupId)
      this.$refs.wizard.nextTab()
    },
    parseFrenchDate (strValue) {
      var dateArray = strValue.split('/').reverse()
      return new Date(dateArray[0], dateArray[1] - 1, dateArray[2])
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
    this.selectedDate = new Date()
    this.selectedTime = new Date()
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
