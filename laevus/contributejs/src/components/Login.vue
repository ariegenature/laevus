<template>
  <section class="hero is-fullheight">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-one-third">
            <div class="card">
              <div class="card-header">
                <p class="card-header-title">Connectez-vous</p>
                <div class="card-header-icon">
                  <b-icon icon="sign-in"></b-icon>
                </div>
              </div>
              <div class="card-content">
                <form id="login-form" method="POST" accept-charset="UTF-8"
                      v-on:submit.prevent>
                  <b-field label="Nom d'utilisateur">
                    <b-input icon="user" autofocus required v-model="username">
                    </b-input>
                  </b-field>
                  <b-field label="Mot de passe">
                    <b-input type="password" icon="user-secret" required v-model="password">
                    </b-input>
                  </b-field>
                  <b-field grouped position="is-right">
                    <p class="control">
                    <button type="submit" class="button is-primary">C'est parti&nbsp;!</button>
                    </p>
                  </b-field>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: ''
    }
  }
}
</script>
