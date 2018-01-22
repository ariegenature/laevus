<template>
  <b-table :data="rows" :bordered="false" :striped="false" :narrowed="true"
           :hoverable="false" :mobile-cards="true">
    <template slot-scope="props">
      <b-table-column label="id" :visible="false">
        {{ props.row.id }}
      </b-table-column>
      <b-table-column label="Date" numeric>
        {{ new Date(props.row.dateTime).toLocaleString() }}
      </b-table-column>
      <b-table-column label="Groupe">
        {{ props.row.groupName }}
      </b-table-column>
      <b-table-column label="Id. Taxref">
        {{ props.row.taxrefId }}
      </b-table-column>
      <b-table-column label="Nom scientifique">
        {{ props.row.scientificName }}
      </b-table-column>
      <b-table-column label="Noms communs" v-html="props.row.commonNames">
      </b-table-column>
      <b-table-column label="Nb." v-html="displayCount(props.row.countAccuracy, props.row.count)"
                      numeric>
      </b-table-column>
      <b-table-column label="Vivant ?" centered>
        <b-icon :icon="boolIcon(props.row.isAlive)" :type="boolClass(props.row.isAlive)"></b-icon>
      </b-table-column>
      <b-table-column label="Commentaires">
        {{ props.row.comments }}
      </b-table-column>
      <b-table-column label="Prénom">
        {{ props.row.firstName }}
      </b-table-column>
      <b-table-column label="Nom">
        {{ props.row.surname }}
      </b-table-column>
      <b-table-column label="Courriel">
        {{ props.row.email }}
      </b-table-column>
    </template>
  </b-table>
</template>

<script>
import axios from 'axios'

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
    }
  },
  async created () {
    try {
      const response = await axios.get('/api/full-contribution')
      this.contributions = response.data
    } catch (e) {
      console.log(e)
    }
  }
}
</script>
