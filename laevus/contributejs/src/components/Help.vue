<template>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Comment utiliser la carte ?</p>
    </header>
    <section class="modal-card-body">
      <div class="content">
        <h2>Ajouter une observation</h2>
        <p>Pour saisir une nouvelle observation, il suffit de cliquer à l'endroit où vous avez
        observé un animal.</p>
        <p>Afin de garantir un minimum de précision, le niveau de zoom de la carte doit être
        suffisant.</p>
        <h2>Voir les observations</h2>
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
