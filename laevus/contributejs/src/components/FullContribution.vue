<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <div class="container is-fluid">
        <div class="columns">
          <div class="column is-centered">
            <full-contribution-table></full-contribution-table>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import FullContributionTable from './FullContributionTable'

export default {
  name: 'FullContribution',
  components: {
    FullContributionTable
  }
}
</script>
