<template>
  <form-wizard @on-complete="$parent.close()" title="" subtitle="" step-size="xs">
    <tab-content title="Date et heure">
      My first tab content
    </tab-content>
    <tab-content title="Identification grossière">
      My second tab content
    </tab-content>
    <tab-content title="Coordonnées">
      Yuhuuu! This seems pretty damn simple
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
  }
}
</script>
