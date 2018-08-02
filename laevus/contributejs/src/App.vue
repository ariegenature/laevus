<template>
  <div id="app" ref="app">
    <navbar></navbar>
    <router-view/>
    <site-footer></site-footer>
    <b-loading :active="isLoading" :canCancel="false"></b-loading>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import SiteFooter from './components/SiteFooter'
import 'intro.js/introjs.css'

import Navbar from './components/Navbar'

export default {
  name: 'app',
  components: {
    Navbar,
    SiteFooter
  },
  computed: mapGetters([
    'intro',
    'isHelpShown',
    'isLoading'
  ]),
  methods: mapActions([
    'syncCurrentUser',
    'toggleHelp'
  ]),
  created () {
    this.syncCurrentUser()
  },
  mounted () {
    var firstTime = localStorage.getItem('firstTime')
    firstTime = firstTime === null ? true : firstTime
    if (firstTime === true) {
      this.toggleHelp()
      localStorage.setItem('firstTime', false)
    }
  },
  watch: {
    isHelpShown: {
      handler (val, oldVal) {
        if (val === false) return
        this.$router.replace({ name: 'home' })
        this.$nextTick(() => {
          this.intro.setOptions({
            skipLabel: 'Sortir',
            doneLabel: 'Sortir',
            nextLabel: 'Suivant',
            prevLabel: 'Précédent',
            showStepNumbers: false,
            steps: [
              {
                intro: `
                <div class="content">
                <h6 class="title is-6">Faune et routes d'Ariège</h6>
                <p class="is-size-7">Bienvenue&nbsp;! Voici quelques conseils pour saisir vos observations&hellip;</p>
                <p class="is-size-7">Vous pouvez quitter cette présentation à tout moment en cliquant sur
                <kbd>Sortir</kbd>.</p>
                </div>
                `
              },
              {
                element: this.$refs.app.querySelectorAll('#map .leaflet-draw-draw-marker')[0],
                intro: `
                <div class="content">
                <p class="is-size-7">Pour saisir une observation, cliquez sur ce bouton.
                Cliquez ensuite sur la carte, à l'endroit <em>précis</em> de l'observation, et laissez-vous guider.</p>
                </div>
                `
              },
              {
                element: this.$refs.app.querySelectorAll('#tag .tags')[0],
                intro: `
                <div class="content">
                <p class="is-size-7">Pour que la localisation soit précise, la saisie n'est possible qui si le niveau
                de zoom est suffisant. Zoomez sur la carte jusqu'à ce que ce badge devienne
                <span class="has-text-sucess">vert</span>.</p>
                </div>
                `
              },
              {
                element: this.$refs.app.querySelectorAll('#map .leaflet-control-locate')[0],
                intro: `
                <div class="content">
                <p class="is-size-7">Si vous êtes sur place avec un téléphone &mdash;GPS activé&mdash; vous pouvez
                aussi cliquer sur ce bouton pour être localisé automatiquement.</p>
                <p class="is-size-7">Acceptez de partager la localisation si cela vous est demandé ; puis, cliquez sur
                le jalon apparu et laissez-vous guider.</p>
                <p class="is-size-7"><strong>Attention&nbsp;!</strong>&nbsp;Ne jamais utiliser un téléphone en
                conduisant&nbsp;!</p>
                </div>
                `
              },
              {
                element: this.$refs.app.querySelectorAll('#help')[0],
                intro: `
                <div class="content">
                <p class="is-size-7">Par la suite, vous pourrez afficher à nouveau cette présentation en cliquant sur
                ce lien.</p>
                </div>
                `
              },
              {
                intro: `
                <div class="content">
                <p class="is-size-7">Cette introduction est maintenant terminée. Cliquez sur <kbd>Sortir</kbd> pour
                afficher la page principale.</p>
                </div>
                `
              }
            ]
          })
          this.intro.start()
          this.toggleHelp()
        })
      }
    }
  }
}
</script>
