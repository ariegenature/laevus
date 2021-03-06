<template>
  <b-table id="species" :data="data" :bordered="false" :striped="false" :narrowed="true"
           :hoverable="true" :mobile-cards="true" paginated :per-page="10" :current-page.sync="currentPage"
           pagination-size="is-small" :selected.sync="selectedFeature" focusable>
    <b-table-column label="id" :visible="false" v-slot="props">
      {{ props.row.id }}
    </b-table-column>
    <b-table-column label="Date" numeric v-slot="props">
      {{ new Date(props.row.date).toLocaleDateString() }}
    </b-table-column>
    <b-table-column label="Groupe" v-slot="props">
      {{ props.row.group }}
    </b-table-column>
    <b-table-column label="Nb." numeric v-slot="props">
      <span v-html="displayCount(props.row.accuracy, props.row.count)"></span>
    </b-table-column>
    <b-table-column label="Vivant ?" centered v-slot="props">
      <b-icon :icon="boolIcon(props.row.isAlive)" :type="boolClass(props.row.isAlive)"></b-icon>
    </b-table-column>
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
  height: 75vh;
}
</style>
