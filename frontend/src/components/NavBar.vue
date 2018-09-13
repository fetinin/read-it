<template>
<header class="navbar">
  <section class="navbar-section">
    <router-link class="btn btn-link" to='/books'>Книги</router-link>
    <router-link class="btn btn-link" to='/upload-book'>Добавить книгу</router-link>
  </section>
  <section class="navbar-center">ReadIT</section>
  <section class="navbar-section">
      <a @click.prevent="logout" href="#logout" class="btn btn-link">Выйти</a>
      <div class="user">
        <figure :class="['avatar', 'avatar-lg', {'no-bg': user.avatar}]" :data-initial="user.name[0].toUpperCase()">
          <img v-if="user.avatar" :src="'data:image/jpg;base64,' + user.avatar" alt="Avatar">
        </figure>
      </div>
  </section>
</header>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { User } from '@/types';
import { logout as logoutUser } from '@/authorization';

@Component
export default class NavBar extends Vue {
  get user(): User {
    return this.$store.state.user;
  }
  private logout() {
    logoutUser();
    this.$router.push({ name: 'signup' });
  }
}
</script>

<style scoped>
.no-bg {
  background: transparent;
}
.navbar {
  min-height: 48px;
}
div.user > * {
  margin-right: 10px;
}
</style>
