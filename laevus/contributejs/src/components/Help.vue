<template>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Guide d'utilisation</p>
    </header>
    <section class="modal-card-body">
      <div class="content">
        <h2 class="title is-5">Ajouter une observation</h2>
        <p>Pour saisir une nouvelle observation, il vous suffit de cliquer sur
        le bouton <b-icon icon="map-marker"></b-icon> de la carte puis de
        placer le jalon à l'endroit où vous avez observé un animal sauvage près
        d'une route.</p>
        <p><strong>Note&nbsp;:</strong> le niveau de zoom sur la carte doit
        être suffisant pour pouvoir placer le jalon.</p>
        <p>Laissez-vous ensuite guider pour les détails de votre
        observation.</p>
        <h2 class="title is-5">Si vous êtes sur place&nbsp;: localisation automatique</h2>
        <p>Sur un téléphone avec GPS activé, vous pouvez aussi être localisé
        automatiquement&nbsp;: cliquez sur le bouton <b-icon
            icon="bullseye"></b-icon> de la carte. Acceptez de partager la
          localisation si cela vous est demandé. Un jalon apparaît alors à
          l'endroit où vous avec été localisé&nbsp;; il vous suffit de cliquer
          dessus pour commencer à saisir votre observation.</p>
        <p><strong>Attention&nbsp;:</strong> ne <strong>jamais</strong>
        utiliser votre téléphone pendant que vous conduisez&nbsp;!</p>
        <h2 class="title is-5">Voir les observations</h2>
        <p>Sur la carte apparaissent les observations <em>déjà saisies</em> sous forme de
        points.</p>
        <p>Cliquez sur un point pour voir le détail.</p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Help'
}
</script>
