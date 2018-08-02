<template>
  <footer class="footer is-size-7 has-text-centered has-text-weight-light has-text-grey-darker">
    <div class="container is-fluid">
      <div class="columns">
        <div class="column is-two-third vcenter">
          <div class="content">
            <p>Observatoire participatif réalisé dans le cadre du contrat de restauration de la biodiversité (CRB).</p>
            <img src="static/logo-region-europeen-feder.jpg"
                 border="0" alt="Logo FEDER" title="Fond européen de développement régional"
                 style="height: 116px; width: auto;">
            <h6 class="title is-6">Partenaires</h6>
            <div class="columns is-centered is-multiline">
              <div class="column is-one-third vcenter">
                <div class="image" style="display: inline-block;">
                  <a href="http://www.parc-pyrenees-ariegeoises.fr/" target="_blank">
                    <img src="static/logo-pnr-pa.jpg"
                         border="0" alt="Logo PNR PA" title="Parc naturel régional des Pyrénées Ariégeoises"
                         style="height: 64px; width: auto;">
                  </a>
                </div>
              </div>
              <div class="column is-one-third vcenter">
                <div class="image" style="display: inline-block;">
                  <a href="https://ariegenature.fr" target="_blank">
                    <img src="static/logo-ana.png"
                         border="0" alt="Logo ANA" title="Association des naturalistes de l'Ariège"
                         style="height: 64px; width: auto;">
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="column is-one-third vcenter">
          <div class="content">
            <div>
              <div class="image" style="display: inline-block;">
                <a href="http://flask.pocoo.org/" target="_blank">
                  <img src="static/logo-flask.png"
                       border="0" alt="Logo Flask" title="Propulsé par Flask"
                       style="height: 16px; width: auto;">
                </a>
              </div>&nbsp;
              <div class="image is-16x16" style="display: inline-block;">
                <a href="https://vuejs.org" target="_blank">
                  <img src="static/logo-vuejs.png"
                       boroder="0" alt="Logo Vue.js" title="Propulsé par Vue.js">
                </a>
              </div>
            </div>
            <p>Réalisé avec
            <a href="http://flask.pocoo.org" target="_blank" title="Flask">Flask</a>
            et
            <a href="https://vuejs.org" target="_blank" title="Vue.js">Vue.js</a>.</p>
            <p>Réalisation ANA.</p>
            <p>Copyright © PNR PA 2018.</p>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'SiteFooter'
}
</script>

<style>
.vcenter {
  margin-top: auto;
  margin-bottom: auto;
}
</style>
