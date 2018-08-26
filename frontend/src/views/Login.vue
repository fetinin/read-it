<template>
<div class="login-form">
    <form class="form-group" @submit.prevent="onLogin">
        <h2 class="header">Вход</h2>
        <p class="note">Войдите с помощью учетной записи в других сервисах</p>
        <label class="form-label" for="login">Логин</label>
        <input v-model="login" class="form-input" type="text" id="login" placeholder="AlanParrish26">
        <label class="form-label" for="password">Пароль</label>
        <input v-model='password' class="form-input" type="password" id="password" placeholder="jYOUmanji">
        <button class="btn btn-primary">Войти</button>
    </form>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {},
})
export default class Login extends Vue {
  private login = '';
  private password = '';

  private onLogin() {
    if (this.login === 'denis' && this.password === '1234567') {
      this.$router.push({ name: 'books' });
    } else {
      console.log('Wrong credentials!');
    }
  }
}
</script>

<style scoped>
.header {
  text-align: center;
  margin-bottom: 0;
}
.login-form {
  margin: auto;
}
.note {
  color: #acb3c2;
}
button {
  margin-top: 20px;
  margin-left: 35%;
}
</style>
