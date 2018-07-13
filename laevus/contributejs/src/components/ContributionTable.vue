<template>
  <b-table id="species" :data="data" :bordered="false" :striped="false" :narrowed="true"
           :hoverable="true" :mobile-cards="true" paginated :per-page="10" :current-page.sync="currentPage"
           pagination-size="is-small" :selected.sync="selectedFeature" focusable>
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
    <template slot="bottom-left">
        <h6 class="title is-6">Observations récentes</h6>
    </template>
  </b-table>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'ContributionTable',
  data () {
    return {
      currentPage: 1,
      selectedFeature: null
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
      'contributions',
      'selectedFeatureId'
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
    },
    ...mapActions([
      'updateSelectedFeatureId'
    ])
  },
  watch: {
    selectedFeature: {
      handler (val, oldVal) {
        if (val === null) {
          this.updateSelectedFeatureId(null)
        } else {
          this.updateSelectedFeatureId(val.id)
        }
      }
    },
    selectedFeatureId: {
      handler (val, oldVal) {
        if (val === null) {
          this.selectedFeature = null
        } else {
          this.selectedFeature = this.data.find((feature) => feature.id === val)
        }
      }
    }
  }
}
</script>

<style>
#species {
  height: 70vh;
}
</style>
