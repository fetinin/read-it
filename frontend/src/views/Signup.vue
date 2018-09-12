<template>
<div class="login-form">
    <form class="form-group" @submit.prevent="onLogin">
        <h2 class="header">Регистрация</h2>
        <p class="note">Войдите с помощью учетной записи в других сервисах</p>
        <div class="auth-services">
          <span v-for="auth in 3" :key="auth" class='auth-service'>
          <a href="https://oauth.vk.com/authorize?client_id=6684417&display=page&redirect_uri=http://localhost:5000/auth/vk&response_type=code&v=5.84">
          <img src="../assets/ghub-icon-w-64.png" alt="">
          </a>
        </span>
        </div>
        
        <hr>
        <label class="form-label" for="login">Логин</label>
        <input v-model="login" class="form-input" type="text" id="login" placeholder="AlanParrish26">
        <label class="form-label" for="password">Пароль</label>
        <input v-model='password' class="form-input" type="password" id="password" placeholder="jYOUmanji">
        <button class="btn btn-primary">Зарегистрироваться</button>
    </form>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {},
})
export default class Signup extends Vue {
  private login = '';
  private password = '';
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
  margin: auto;
}
.note {
  color: #acb3c2;
}
button {
  margin-top: 20px;
  position: relative;
  left: 50%;
  transform: translate(-50%);
}
.auth-service img {
  border-radius: 35px;
  background-color: #acb3c2;
}
.auth-service img:hover {
  border-radius: 35px;
  background-color: black;
}
</style>
