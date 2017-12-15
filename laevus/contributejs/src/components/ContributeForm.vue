<template>
  <form-wizard ref="wizard" @on-complete="$parent.close()" title="" subtitle="" step-size="xs">
    <tab-content title="Date et heure">
      <b-field label="Date">
        <b-datepicker placeholder="Cliquer pour choisir une date"
                      icon="calendar" :readonly="false"></b-datepicker>
      </b-field>
      <b-field label="Heure">
        <b-timepicker placeholder="Cliquer pour indiquer un horaire"
                      icon="clock-o" :readonly="false"></b-timepicker>
      </b-field>
    </tab-content>
    <tab-content title="Identification grossière">
      <div class="columns is-centered">
        <div class="column is-one-third has-text-centered">
          <a href="#" @click="nextTab">
            <figure class="image is-64x64 block-center">
              <img alt="Grands herbivores" src="../assets/deer.png">
            </figure>
            <p class="is-size-7">Grands herbivores</p>
          </a>
        </div>
        <div class="column is-one-third has-text-centered">
          <a href="#" @click="nextTab">
            <figure class="image is-64x64 block-center">
              <img alt="Petits mammifères" src="../assets/rabbit.png">
            </figure>
            <p class="is-size-7">Petits mammifères</p>
          </a>
        </div>
        <div class="column is-one-third has-text-centered">
          <a href="#" @click="nextTab">
            <figure class="image is-64x64 block-center">
              <img alt="Reptiles" src="../assets/snake.png">
            </figure>
            <p class="is-size-7">Reptiles</p>
          </a>
        </div>
      </div>
      <div class="columns is-centered">
        <div class="column is-one-third has-text-centered">
          <a href="#" @click="nextTab">
            <figure class="image is-64x64 block-center">
              <img alt="Amphibiens" src="../assets/frog.png">
            </figure>
            <p class="is-size-7">Amphibiens</p>
          </a>
        </div>
        <div class="column is-one-third has-text-centered">
          <a href="#" @click="nextTab">
            <figure class="image is-64x64 block-center">
              <img alt="Chauves-souris" src="../assets/bat.png">
            </figure>
            <p class="is-size-7">Chauves-souris</p>
          </a>
        </div>
        <div class="column is-one-third has-text-centered">
          <a href="#" @click="nextTab">
            <figure class="image is-64x64 block-center">
              <img alt="Oiseaux" src="../assets/bird.png">
            </figure>
            <p class="is-size-7">Oiseaux</p>
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
        <b-field label="Votre nom" expanded>
          <b-field>
            <b-input expanded placeholder="Prénom"></b-input>
            <b-input expanded placeholder="Nom"></b-input>
          </b-field>
        </b-field>
      </b-field>
      <b-field label="Votre adresse électronique" expanded>
        <b-input type="email "placeholder="prenom.nom@example.org"></b-input>
      </b-field>
    </tab-content>
  </form-wizard>
</template>

<script>
import {FormWizard, TabContent} from 'vue-form-wizard'
import 'vue-form-wizard/dist/vue-form-wizard.min.css'

export default {
  name: 'ContributeForm',
  components: {
    FormWizard,
    TabContent
  },
  data () {
    return {
    }
  },
  methods: {
    nextTab (ev) {
      this.$refs.wizard.nextTab()
    }
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
