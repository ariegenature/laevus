<template>
  <b-table :data="rows" :bordered="false" :striped="false" :narrowed="true"
           :hoverable="false" :mobile-cards="true">
    <b-table-column label="id" :visible="false" v-slot="props">
      {{ props.row.id }}
    </b-table-column>
    <b-table-column label="Date" numeric v-slot="props">
      {{ new Date(props.row.dateTime).toLocaleString() }}
    </b-table-column>
    <b-table-column label="Groupe" v-slot="props">
      {{ props.row.groupName }}
    </b-table-column>
    <b-table-column label="Id. Taxref" v-slot="props">
      {{ props.row.taxrefId }}
    </b-table-column>
    <b-table-column label="Nom scientifique" v-slot="props">
      {{ props.row.scientificName }}
    </b-table-column>
    <b-table-column label="Noms communs" v-slot="props">
      <span v-html="props.row.commonNames"></span>
    </b-table-column>
    <b-table-column label="Nb." numeric v-slot="props">
      <span v-html="displayCount(props.row.countAccuracy, props.row.count)"></span>
    </b-table-column>
    <b-table-column label="Vivant ?" centered v-slot="props">
      <b-icon :icon="boolIcon(props.row.isAlive)" :type="boolClass(props.row.isAlive)"></b-icon>
    </b-table-column>
    <b-table-column label="Commentaires" v-slot="props">
      {{ props.row.comments }}
    </b-table-column>
    <b-table-column label="Prénom" v-slot="props">
      {{ props.row.firstName }}
    </b-table-column>
    <b-table-column label="Nom" v-slot="props">
      {{ props.row.surname }}
    </b-table-column>
    <b-table-column label="Courriel" v-slot="props">
      {{ props.row.email }}
    </b-table-column>
  </b-table>
</template>

<script>
import axios from 'axios'
import { mapActions } from 'vuex'

export default {
  name: 'FullContributionTable',
  data () {
    return {
      contributions: []
    }
  },
  computed: {
    rows () {
      return this.contributions
    }
  },
  methods: {
    displayCount (accuracy, count) {
      if (accuracy === '=') {
        return count
      } else {
        return `${accuracy} ${count}`
      }
    },
    boolIcon (bool) {
      return bool ? 'check' : 'times'
    },
    boolClass (bool) {
      return bool ? 'is-success' : 'is-danger'
    },
    ...mapActions([
      'setPageLoading',
      'setPageReady'
    ])
  },
  async created () {
    try {
      this.setPageLoading()
      const response = await axios.get('/api/full-contribution')
      this.contributions = response.data
      this.setPageReady()
    } catch (e) {
      console.log(e)
    }
  }
}
</script>
