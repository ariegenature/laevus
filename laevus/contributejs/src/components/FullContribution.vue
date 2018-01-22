<template>
  <section class="hero is-fullheight">
    <div id="hero-map" class="hero-body">
      <full-contribution-table></full-contribution-table>
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
