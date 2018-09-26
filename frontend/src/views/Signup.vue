<template>
<div class="login-form">
    <!-- TODO -->
    <!-- PLACE LOGO HERE -->
    <div class="form-group">
        <h2 class="header">Регистрация</h2>
        <p class="note text-center">Войдите с помощью учетной записи в других сервисах</p>
        <div class="auth-services">
          <span class='auth-service'>
          <a href="http://localhost:5000/auth/vk">
            <img src="@/assets/vk-logo.png" alt="">
          </a>
          </span>
          <span class='auth-service'>
            <a href="http://localhost:5000/auth/google">
              <img src="@/assets/google-logo.png" alt="">
            </a>
          </span>
          <span class='auth-service'>
            <a href="http://localhost:5000/auth/github">
              <img src="@/assets/ghub-logo.png" alt="">
            </a>
          </span>
        </div>
        <div class="divider text-center" data-content="или"></div>
        <div class="auth-services">
          <span class='auth-service'>
            <a href="http://localhost:5000/auth/guest">
              <img src="@/assets/guest-logo.png" alt="">
            </a>
          </span>
        </div>
        <p class="note text-center">Познакомьтесь с сервисом в роли гостя</p>
    </div>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {},
})
export default class Signup extends Vue {}
</script>

<style scoped>
.header {
  text-align: center;
  margin-bottom: 0;
}
.auth-services {
  display: flex;
  justify-content: space-evenly;
}
.login-form {
  margin: 0 auto 0 auto;
  align-self: center;
}
.note {
  color: #acb3c2;
}
.auth-service img {
  border-radius: 35px;
  background-color: #acb3c2;
  width: 64px;
}
.auth-service img:hover {
  border-radius: 35px;
  background-color: black;
}
</style>
