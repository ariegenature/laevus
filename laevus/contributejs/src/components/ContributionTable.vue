<template>
  <b-table id="species" :data="data" :bordered="false" :striped="false" :narrowed="true"
           :hoverable="true" :mobile-cards="true" paginated :per-page="10" :current-page.sync="currentPage"
           pagination-size="is-small">
    <template slot-scope="props">
      <b-table-column label="id" :visible="false">
        {{ props.row.id }}
      </b-table-column>
      <b-table-column label="Date" numeric>
        {{ new Date(props.row.date).toLocaleDateString() }}
      </b-table-column>
      <b-table-column label="Groupe">
        {{ props.row.group }}
      </b-table-column>
      <b-table-column label="Nb." v-html="displayCount(props.row.accuracy, props.row.count)"
                      numeric>
      </b-table-column>
      <b-table-column label="Vivant ?" centered>
        <b-icon :icon="boolIcon(props.row.isAlive)" :type="boolClass(props.row.isAlive)"></b-icon>
      </b-table-column>
    </template>
  </b-table>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ContributionTable',
  data () {
    return {
      currentPage: 1
    }
  },
  computed: {
    data () {
      if (!this.contributions || !this.contributions.features) {
        return []
      }
      var res = []
      this.contributions.features.forEach((feature) => {
        res.push({
          id: feature.id,
          date: feature.properties.date_time,
          group: feature.properties.group,
          accuracy: feature.properties.accuracy,
          count: feature.properties.count,
          isAlive: feature.properties['is_alive']
        })
      })
      return res
    },
    ...mapGetters([
      'contributions'
    ])
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
  }
}
</script>

<style>
#species {
  height: 70vh;
  overflow: scroll;
}
</style>
