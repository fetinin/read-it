<template>
<div class="login-form">
    <div class="form-group">
        <h2 class="header">Регистрация</h2>
        <p class="note text-center">Войдите с помощью учетной записи в других сервисах</p>
        <div class="auth-services">
          <span class='auth-service'>
          <a :href="backendURL + '/auth/vk'">
            <img src="@/assets/vk-logo.png" alt="VKontakte">
          </a>
          </span>
          <span class='auth-service'>
            <a :href="backendURL + '/auth/google'">
              <img src="@/assets/google-logo.png" alt="Google">
            </a>
          </span>
          <span class='auth-service'>
            <a :href="backendURL + '/auth/github'">
              <img src="@/assets/ghub-logo.png" alt="Github" class="bg-dark">
            </a>
          </span>
        </div>
        <div class="divider text-center" data-content="или"></div>
        <div class="auth-services">
          <span class='auth-service'>
            <a :href="backendURL + '/auth/guest'">
              <img src="@/assets/guest-logo.png" alt="Guest" class="bg-dark">
            </a>
          </span>
        </div>
        <p class="note text-center">Познакомьтесь с сайтом в роли гостя</p>
    </div>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {},
})
export default class Signup extends Vue {
  private backendURL = process.env.VUE_APP_BACKEND_URL;
}
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
.bg-dark {
  background-color: hsla(221, 15%, 40%, 1);
}
.auth-service img {
  border-radius: 35px;
  width: 64px;
  box-shadow: 0px 1px 3px 0px black;
  opacity: 0.7;
}
.auth-service img:hover {
  border-radius: 35px;
  opacity: 1;
}
</style>
